from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for NGO routes
teams = Blueprint("teams", __name__)


# Get team info by id
# Example: /teams/1/
@teams.route("/", methods=["GET"])
def get_all_teams():
    try:
        cursor = db.get_db().cursor()

        # Get all projects for the Team
        cursor.execute("SELECT teamID FROM Teams")
        teams = cursor.fetchall()
        cursor.close()

        return jsonify(teams), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get team info by id
# Example: /teams/1/
@teams.route("/<int:teamID>/", methods=["GET"])
def get_team_by_id(teamID):
    try:
        cursor = db.get_db().cursor()

        # Check if team exists
        cursor.execute("SELECT * FROM Teams WHERE teamID = %s", (teamID,))
        if not cursor.fetchone():
            return jsonify({"error": "Team not found"}), 404

        # Get all projects for the Team
        cursor.execute("SELECT * FROM Teams WHERE teamID = %s", (teamID,))
        teams = cursor.fetchall()
        cursor.close()

        return jsonify(teams), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
