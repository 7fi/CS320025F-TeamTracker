from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

players = Blueprint("players", __name__)

# Get details of a specific player
@players.route("/<int:playerID>", methods=["GET"])
def get_player(playerID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Players p JOIN Team t ON p.teamID = t.teamID WHERE p.playerID = %s", (playerID,))
        player = cursor.fetchone()

        if not player:
            return jsonify({"error": "Player not found"}), 404

        cursor.close()
        return jsonify(player), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Create a new player
@players.route("/", methods=["POST"])
def create_player():
    try:
        data = request.get_json()

        required_fields = ["name", "teamID", "position", "jerseyNumber","phoneNumber", "gradYear"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
        INSERT INTO Players (name, teamID, position, jerseyNumber, phoneNumber, gradYear)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["name"],
                data["teamID"],
                data["position"],
                data["jerseyNumber"],
                data["phoneNumber"],
                data["gradYear"],
            ),
        )
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Player created successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Update an existing player's information
@players.route("/<int:playerID>", methods=["PUT"])
def update_player(playerID):
    try:
        data = request.get_json()

        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            return jsonify({"error": "Player not found"}), 404

        fields = []
        values = []
        for field in ["name", "position", "phoneNumber","gradYear", "jerseyNumber"]:
            if field in data:
                fields.append(f"{field} = %s")
                values.append(data[field])

        if not fields:
            return jsonify({"error": "No fields to update"}), 400

        values.append(playerID)
        query = f"UPDATE Players SET {', '.join(fields)} WHERE playerID = %s"
        cursor.execute(query, tuple(values))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Player updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
    

# Delete an existing player
@players.route("/<int:playerID>", methods=["DELETE"])
def delete_player(playerID):
    try:
        cursor = db.get_db().cursor()

        # Make sure the player exists
        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            return jsonify({"error": "Player not found"}), 404

        # Delete player's injuries (foreign key dependencies)
        cursor.execute("DELETE FROM Injury WHERE playerID = %s", (playerID,))

        # Delete player's comments (foreign key dependencies)
        cursor.execute("DELETE FROM Comment WHERE targetID = %s", (playerID,))

        # Delete the player
        cursor.execute("DELETE FROM Players WHERE playerID = %s", (playerID,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Player deleted successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    
# Gets comments for a specific player
@players.route("/<int:playerID>/comments", methods=["GET"])
def get_player_comments(playerID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            return jsonify({"error": "Player not found"}), 404

        cursor.execute(
            "SELECT * FROM Comment WHERE targetID = %s", (playerID,)
        )
        comments = cursor.fetchall()
        cursor.close()

        return jsonify(comments), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Add a comment for a specific player
@players.route("/<int:playerID>/comments", methods=["POST"])
def add_player_comment(playerID):
    try:
        data = request.get_json()

        required_fields = ["text", "commenterID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            return jsonify({"error": "Player not found"}), 404

        query = """
        INSERT INTO Comment (text, dateTime, commenterID, targetID)
        VALUES (%s, NOW(), %s, %s)
        """
        cursor.execute(query, (data["text"], data["commenterID"], playerID))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Comment added successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Delete a comment for a specific player
@players.route("/<int:playerID>/comments", methods=["DELETE"])
def delete_player_comment(playerID):
    try:
        data = request.get_json()

        if "commentID" not in data:
            return jsonify({"error": "Missing required field: commentID"}), 400

        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            return jsonify({"error": "Player not found"}), 404

        cursor.execute(
            "SELECT * FROM Comment WHERE commentID = %s AND targetID = %s",
            (data["commentID"], playerID),
        )
        if not cursor.fetchone():
            return jsonify({"error": "Comment not found"}), 404

        cursor.execute(
            "DELETE FROM Comment WHERE commentID = %s AND targetID = %s",
            (data["commentID"], playerID),
        )
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Comment deleted successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Return list of all injuries for a specific player
@players.route("/<int:playerID>/injuries", methods=["GET"])
def get_player_injuries(playerID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            return jsonify({"error": "Player not found"}), 404

        cursor.execute(
            "SELECT * FROM Injury WHERE playerID = %s", (playerID,)
        )
        injuries = cursor.fetchall()
        cursor.close()

        return jsonify(injuries), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Add new injury report for a specific player
@players.route("/<int:playerID>/injuries", methods=["POST"])
def add_player_injury(playerID):
    try:
        data = request.get_json()

        required_fields = ["injuryType", "injuryDate", "recoveryDate"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            return jsonify({"error": "Player not found"}), 404

        query = """
        INSERT INTO Injury (playerID, type, date, recoveryDate)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                playerID,
                data["injuryType"],
                data["injuryDate"],
                data["recoveryDate"],
            ),
        )
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Injury report added successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Update details of existing injury report for a specific player
@players.route("/<int:playerID>/injuries", methods=["PUT"])
def update_player_injury(playerID):
    try:
        data = request.get_json()

        if "injuryID" not in data:
            return jsonify({"error": "Missing required field: injuryID"}), 400

        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            return jsonify({"error": "Player not found"}), 404

        cursor.execute(
            "SELECT * FROM Injury WHERE injuryID = %s AND playerID = %s",
            (data["injuryID"], playerID),
        )
        if not cursor.fetchone():
            return jsonify({"error": "Injury report not found"}), 404

        fields = []
        values = []
        field_mapping = {"injuryType": "type", "injuryDate": "date", "recoveryDate": "recoveryDate"}

        for field in ["injuryType", "injuryDate", "recoveryDate"]:
            if field in data:
                db_field = field_mapping[field]
                fields.append(f"{db_field} = %s")
                values.append(data[field])

        if not fields:
            return jsonify({"error": "No fields to update"}), 400

        values.append(data["injuryID"])
        values.append(playerID)
        query = f"UPDATE Injury SET {', '.join(fields)} WHERE injuryID = %s AND playerID = %s"
        cursor.execute(query, tuple(values))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Injury report updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Delete injury report for a specific player (only used when injuury accidently added)
@players.route("/<int:playerID>/injuries", methods=["DELETE"])
def delete_player_injury(playerID):
    try:
        data = request.get_json()

        if "injuryID" not in data:
            return jsonify({"error": "Missing required field: injuryID"}), 400

        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Players WHERE playerID = %s", (playerID,))
        if not cursor.fetchone():
            return jsonify({"error": "Player not found"}), 404

        cursor.execute(
            "SELECT * FROM Injury WHERE injuryID = %s AND playerID = %s",
            (data["injuryID"], playerID),
        )
        if not cursor.fetchone():
            return jsonify({"error": "Injury report not found"}), 404

        cursor.execute(
            "DELETE FROM Injury WHERE injuryID = %s AND playerID = %s",
            (data["injuryID"], playerID),
        )
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Injury report deleted successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500