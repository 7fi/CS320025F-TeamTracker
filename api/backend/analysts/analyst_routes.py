from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

analysts = Blueprint("analysts", __name__)

@analysts.route("/<int:analystID>", methods=["GET"])
def get_coach(analystID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Analyst c JOIN Team t ON c.teamID = t.teamID WHERE c.analystID = %s", (analystID,))
        player = cursor.fetchone()

        if not player:
            return jsonify({"error": "Player not found"}), 404

        cursor.close()
        return jsonify(player), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500