from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app
# Create a Blueprint for Event routes
events = Blueprint("events", __name__)

# Get all events
# Example: /events/
@events.route("/", methods=["GET"])
def get_all_events():
    try:
        cursor = db.get_db().cursor()

        # Get all events
        cursor.execute("SELECT * FROM Events")
        events = cursor.fetchall()
        cursor.close()

        return jsonify(events), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500