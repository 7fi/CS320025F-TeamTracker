from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for NGO routes
teams = Blueprint("teams", __name__)

# Get team info by id
# Example: /teams/
@teams.route("/", methods=["GET"])
def get_all_teams():
    try:
        cursor = db.get_db().cursor()

        # Get all for the Team
        cursor.execute("SELECT teamID, teamName FROM Team")
        teams = cursor.fetchall()
        cursor.close()

        return jsonify(teams), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get team info by id
# Example: /teams/1/
@teams.route("/<int:teamID>", methods=["GET"])
def get_team_by_id(teamID):
    try:
        cursor = db.get_db().cursor()

        # Check if team exists
        cursor.execute("SELECT * FROM Team WHERE teamID = %s", (teamID,))
        if not cursor.fetchone():
            return jsonify({"error": "Team not found"}), 404

        # Get all projects for the Team
        cursor.execute("SELECT * FROM Team WHERE teamID = %s", (teamID,))
        teams = cursor.fetchone()
        cursor.close()

        return jsonify(teams), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Get all players on a team
# Example: /teams/1/
@teams.route("/<int:teamID>/players", methods=["GET"])
def get_all_team_players(teamID):
    try:
        cursor = db.get_db().cursor()

        # Check if team exists
        cursor.execute("SELECT * FROM Team WHERE teamID = %s;", (teamID,))
        if not cursor.fetchone():
            return jsonify({"error": "Team not found"}), 404

        # Get all projects for the Team
        cursor.execute("SELECT * FROM Players WHERE teamID = %s;", (teamID,))
        players = cursor.fetchall()
        cursor.close()

        return jsonify(players), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Get all coaches on a team
# Example: /teams/1/
@teams.route("/<int:teamID>/coaches", methods=["GET"])
def get_all_team_coaches(teamID):
    try:
        cursor = db.get_db().cursor()

        # Check if team exists
        cursor.execute("SELECT * FROM Team WHERE teamID = %s;", (teamID,))
        if not cursor.fetchone():
            return jsonify({"error": "Team not found"}), 404

        # Get all projects for the Team
        cursor.execute("SELECT * FROM Coach WHERE teamID = %s;", (teamID,))
        players = cursor.fetchall()
        cursor.close()

        return jsonify(players), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Get all analysts on a team
# Example: /teams/1/
@teams.route("/<int:teamID>/analysts", methods=["GET"])
def get_all_team_analysts(teamID):
    try:
        cursor = db.get_db().cursor()

        # Check if team exists
        cursor.execute("SELECT * FROM Team WHERE teamID = %s;", (teamID,))
        if not cursor.fetchone():
            return jsonify({"error": "Team not found"}), 404

        # Get all projects for the Team
        cursor.execute("SELECT * FROM Analyst p WHERE teamID = %s;", (teamID,))
        analysts = cursor.fetchall()
        cursor.close()

        return jsonify(analysts), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
      
      
# Get all admins on a team
# Example: /teams/1/
@teams.route("/<int:teamID>/admins", methods=["GET"])
def get_all_team_admins(teamID):
    try:
        cursor = db.get_db().cursor()

        # Check if team exists
        cursor.execute("SELECT * FROM Team WHERE teamID = %s;", (teamID,))
        if not cursor.fetchone():
            return jsonify({"error": "Team not found"}), 404

        # Get all projects for the Team
        cursor.execute("SELECT * FROM Admin WHERE teamID = %s;", (teamID,))
        admins = cursor.fetchall()
        cursor.close()

        return jsonify(admins), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
      
      
# Get all events of a team
# Example: /teams/1/
@teams.route("/<int:teamID>/events", methods=["GET"])
def get_all_team_events(teamID):
    try:
        cursor = db.get_db().cursor()

        # Check if team exists
        cursor.execute("SELECT * FROM Team WHERE teamID = %s;", (teamID,))
        if not cursor.fetchone():
            return jsonify({"error": "Team not found"}), 404

        # Get all projects for the Team
        cursor.execute("SELECT * FROM Event WHERE teamID = %s;", (teamID,))
        events = cursor.fetchall()
        cursor.close()

        return jsonify(events), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500