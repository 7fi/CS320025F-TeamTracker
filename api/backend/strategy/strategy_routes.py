from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error

# Blueprint for strategy routes
strategy = Blueprint("strategy", __name__)

# Create a new strategy
# Example: /strategy/ (POST)
@strategy.route("/", methods=["POST"])
def create_strategy():
    try:
        data = request.get_json()

        formation = data.get("formation")
        coachID   = data.get("coachID")

        if not formation or not coachID:
            return jsonify({"error": "formation and coachID are required"}), 400

        cursor = db.get_db().cursor()
        cursor.execute(
            """
            INSERT INTO Strategy (formation, coachID)
            VALUES (%s, %s);
            """,
            (formation, coachID),
        )
        db.get_db().commit()

        new_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Strategy created", "strategyID": new_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Get strategy + associated results (StrategyEvent) 
# Example: /strategy/1/ (GET)
@strategy.route("/<int:stratID>", methods=["GET"])
def get_strategy(stratID):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        # Get the base strategy
        cursor.execute(
            "SELECT * FROM Strategy WHERE strategyID = %s;",
            (stratID,),
        )
        strat = cursor.fetchone()

        if not strat:
            cursor.close()
            return jsonify({"error": "Strategy not found"}), 404

        # Get results of using this strategy (games where it was used)
        cursor.execute(
            """
            SELECT se.eventID,
                   se.result,
                   e.dateTime,
                   e.location,
                   e.teamID
            FROM StrategyEvent se
            JOIN Event e ON se.eventID = e.eventID
            WHERE se.strategyID = %s
            ORDER BY e.dateTime DESC;
            """,
            (stratID,),
        )
        results = cursor.fetchall()
        cursor.close()

        # list of events and results associated with this strategy
        return jsonify(
            {
                "strategy": strat,
                "results": results,   
            }
        ), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Update strategy details AND optionally record game result 
# Example: /strategy/1/ (PUT)
@strategy.route("/<int:stratID>", methods=["PUT"])
def update_strategy(stratID):
    try:
        data = request.get_json()
        formation = data.get("formation")
        coachID   = data.get("coachID")
        eventID   = data.get("eventID")
        result    = data.get("result")

        cursor = db.get_db().cursor()

        # Make sure strategy exists
        cursor.execute(
            "SELECT 1 FROM Strategy WHERE strategyID = %s;",
            (stratID,),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Strategy not found"}), 404

        # Update strategy details if provided
        if formation or coachID:
            # create a simple update
            update_fields = []
            params = []

            if formation:
                update_fields.append("formation = %s")
                params.append(formation)
            if coachID:
                update_fields.append("coachID = %s")
                params.append(coachID)

            update_query = f"""
                UPDATE Strategy
                SET {", ".join(update_fields)}
                WHERE strategyID = %s;
            """
            params.append(stratID)
            cursor.execute(update_query, tuple(params))

        # 3) Optionally record a game result for this strategy
        # (if eventID and result are included in the body)
        if eventID and result:
            cursor.execute(
                """
                INSERT INTO StrategyEvent (strategyID, eventID, result)
                VALUES (%s, %s, %s);
                """,
                (stratID, eventID, result),
            )

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Strategy updated"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500