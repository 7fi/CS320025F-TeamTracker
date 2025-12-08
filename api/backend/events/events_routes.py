from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error

# Create a Blueprint for Event routes
events = Blueprint("events", __name__)

# Get all events
# Example: /events/
@events.route("/", methods=["GET"])
def get_all_events():
    try:
        cursor = db.get_db().cursor()

        # Get all events
        cursor.execute("SELECT * FROM Event")
        all_events = cursor.fetchall()
        cursor.close()

        return jsonify(all_events), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Get details of a specific event
# Example: /events/1/ 
@events.route("/<int:eventID>", methods=["GET"])
def get_event_by_id(eventID):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Event WHERE eventID = %s;", (eventID,))
        event = cursor.fetchone()
        cursor.close()

        if not event:
            return jsonify({"error": "Event not found"}), 404

        return jsonify(event), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Create a new event 
# Example: /events/ (POST)
@events.route("/", methods=["POST"])
def create_event():
    try:
        data = request.get_json()

        team_id  = data.get("teamID")
        dateTime = data.get("dateTime")   
        location = data.get("location")

        # simple validation
        if not all([team_id, dateTime, location]):
            return jsonify({"error": "teamID, dateTime, and location are required"}), 400

        cursor = db.get_db().cursor()
        insert_query = """
            INSERT INTO Event (teamID, dateTime, location)
            VALUES (%s, %s, %s);
        """
        cursor.execute(insert_query, (team_id, dateTime, location))
        db.get_db().commit()

        new_id = cursor.lastrowid
        cursor.close()

        return jsonify({"message": "Event created", "eventID": new_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Update an existing event
# Example: /events/1/ (PUT)
@events.route("/<int:eventID>", methods=["PUT"])
def update_event(eventID):
    try:
        data = request.get_json()

        team_id  = data.get("teamID")
        dateTime = data.get("dateTime")
        location = data.get("location")

        if not all([team_id, dateTime, location]):
            return jsonify({"error": "teamID, dateTime, and location are required"}), 400

        cursor = db.get_db().cursor()

        # check event exists
        cursor.execute("SELECT 1 FROM Event WHERE eventID = %s;", (eventID,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Event not found"}), 404

        update_query = """
            UPDATE Event
            SET teamID = %s,
                dateTime = %s,
                location = %s
            WHERE eventID = %s;
        """
        cursor.execute(update_query, (team_id, dateTime, location, eventID))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Event updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Delete an event
# Example: /events/1/ (DELETE)
@events.route("/<int:eventID>", methods=["DELETE"])
def delete_event(eventID):
    try:
        cursor = db.get_db().cursor()

        # check event exists
        cursor.execute("SELECT 1 FROM Event WHERE eventID = %s;", (eventID,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Event not found"}), 404

        cursor.execute("DELETE FROM Event WHERE eventID = %s;", (eventID,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Event deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# RSVP to an event
# Example: /events/1/rsvp (POST)
@events.route("/rsvp/<int:eventID>", methods=["POST"])
def rsvp_event(eventID):
    try:
        data = request.get_json()
        player_id = data.get("playerID")

        if not player_id:
            return jsonify({"error": "playerID is required"}), 400

        cursor = db.get_db().cursor()

        # Check event exists
        cursor.execute("SELECT 1 FROM Event WHERE eventID = %s;", (eventID,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Event not found"}), 404

        # Check player exists
        cursor.execute("SELECT 1 FROM Players WHERE playerID = %s;", (player_id,))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Player not found"}), 404

        # Insert into junction table
        # insert ignore to prevent duplicate rsvps
        cursor.execute("""
            INSERT IGNORE INTO PlayerEvent (eventID, playerID)
            VALUES (%s, %s);
        """, (eventID, player_id))

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "RSVP recorded"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Un-RSVP from an event
# Example: /events/1/rsvp (DELETE)
@events.route("/rsvp/<int:eventID>", methods=["DELETE"])
def un_rsvp_event(eventID):
    try:
        data = request.get_json()
        player_id = data.get("playerID")

        if not player_id:
            return jsonify({"error": "playerID is required"}), 400

        cursor = db.get_db().cursor()

        # Delete from junction table
        cursor.execute("""
            DELETE FROM PlayerEvent
            WHERE eventID = %s AND playerID = %s;
        """, (eventID, player_id))

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "RSVP removed"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Upcoming events for a player 
# Example: /events/player/1/ (GET)
@events.route("/player/<int:playerID>", methods=["GET"])
def get_next_events_for_player(playerID):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT e.*
            FROM Event e
            JOIN PlayerEvent pe ON e.eventID = pe.eventID
            WHERE pe.playerID = %s
              AND e.dateTime >= NOW()
            ORDER BY e.dateTime ASC;
        """

        cursor.execute(query, (playerID,))
        events = cursor.fetchall()
        cursor.close()

        return jsonify(events), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@events.route("/<int:eventID>/players", methods=["GET"])
def get_players_for_event(eventID):
    try:
        cursor = db.get_db().cursor()

        query = """
            SELECT p.playerID, p.name, p.jerseyNumber
            FROM PlayerEvent pe
            JOIN Players p ON p.playerID = pe.playerID
            WHERE pe.eventID = %s
        """

        cursor.execute(query, (eventID,))
        players = cursor.fetchall()
        cursor.close()

        return jsonify(players), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
