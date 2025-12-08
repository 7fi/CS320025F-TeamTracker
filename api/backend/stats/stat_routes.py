from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

stats = Blueprint("stats", __name__)


# Get details of a specific player
@stats.route("/<int:playerID>", methods=["GET"])
def get_player_stats(playerID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""SELECT statType, dateTime, eventID 
        FROM StatEvent
        WHERE playerID = %s
        ORDER BY dateTime DESC;""", (playerID,))
        player = cursor.fetchall()
        
        cursor.close()
        return jsonify(player), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

@stats.route("/", methods=["POST"])
def add_stat():
    try:
        data = request.get_json()

        required = ["statType", "eventID", "playerID"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO StatEvent (dateTime, statType, eventID, playerID)
            VALUES (NOW(), %s, %s, %s)
        """
        cursor.execute(query, (data["statType"], data["eventID"], data["playerID"]))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Stat added successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

@stats.route("/event/<int:eventID>", methods=["GET"])
def get_stats_for_event(eventID):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT s.statID, s.dateTime, s.statType,
                   p.name, p.playerID
            FROM StatEvent s
            JOIN Players p ON s.playerID = p.playerID
            WHERE s.eventID = %s
            ORDER BY s.dateTime ASC
        """

        cursor.execute(query, (eventID,))
        stats = cursor.fetchall()
        cursor.close()

        return jsonify(stats), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500