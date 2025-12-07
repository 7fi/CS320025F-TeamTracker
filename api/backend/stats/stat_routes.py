from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for NGO routes
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