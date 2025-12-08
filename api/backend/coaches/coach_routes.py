from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

coaches = Blueprint("coaches", __name__)

@coaches.route("/<int:coachID>", methods=["GET"])
def get_coach(coachID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT * FROM Coach c JOIN Team t ON c.teamID = t.teamID WHERE c.coachID = %s",
            (coachID,)
        )
        coach = cursor.fetchone()

        if not coach:
            return jsonify({"error": "Coach not found"}), 404

        cursor.close()
        return jsonify(coach), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

@coaches.route("/<int:coachID>/strategy", methods=["POST"])
def create_strategy(coachID):
    try:
        data = request.get_json()

        required = ["formation", "eventID", "result"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Validate coach
        cursor.execute("SELECT teamID FROM Coach WHERE coachID = %s", (coachID,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Coach not found"}), 404

        teamID = row["teamID"]

        # Validate event belongs to coach's team
        cursor.execute(
            "SELECT eventID FROM Event WHERE eventID = %s AND teamID = %s",
            (data["eventID"], teamID)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Event does not belong to coach's team"}), 400

        # INSERT strategy
        cursor.execute(
            "INSERT INTO Strategy (formation, coachID) VALUES (%s, %s)",
            (data["formation"], coachID)
        )
        strategy_id = cursor.lastrowid

        # LINK strategy to event with result
        cursor.execute(
            "INSERT INTO StrategyEvent (strategyID, eventID, result) VALUES (%s, %s, %s)",
            (strategy_id, data["eventID"], data["result"])
        )

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Strategy created successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

@coaches.route("/<int:coachID>/strategy", methods=["GET"])
def get_strategy_history(coachID):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT s.strategyID, s.formation, se.eventID, se.result,
                   e.title, e.dateTime, e.location
            FROM Strategy s
            JOIN StrategyEvent se ON s.strategyID = se.strategyID
            JOIN Event e ON e.eventID = se.eventID
            WHERE s.coachID = %s
            ORDER BY e.dateTime DESC;
        """

        cursor.execute(query, (coachID,))
        strategies = cursor.fetchall()
        cursor.close()

        return jsonify(strategies), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
