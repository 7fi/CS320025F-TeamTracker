from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

coaches = Blueprint("coaches", __name__)

@coaches.route("/<int:coachID>", methods=["GET"])
def get_coach(coachID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Coach c JOIN Team t ON c.teamID = t.teamID WHERE c.coachID = %s", (coachID,))
        player = cursor.fetchone()

        if not player:
            return jsonify({"error": "Player not found"}), 404

        cursor.close()
        return jsonify(player), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500