from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for NGO routes
teams = Blueprint("teams", __name__)


# Get all NGOs with optional filtering by country, focus area, and founding year
# Example: /ngo/ngos?country=United%20States&focus_area=Environmental%20Conservation
@teams.route("/", methods=["GET"])
def get_all_ngos():
    try:
        current_app.logger.info('Starting get_all_ngos request')
        cursor = db.get_db().cursor()

        # Note: Query parameters are added after the main part of the URL.c
        # Here is an example:
        # http://localhost:4000/ngo/ngos?founding_year=1971
        # founding_year is the query param.

        # Get query parameters for filtering
        country = request.args.get("country")
        focus_area = request.args.get("focus_area")
        founding_year = request.args.get("founding_year")

        current_app.logger.debug(f'Query parameters - country: {country}, focus_area: {focus_area}, founding_year: {founding_year}')

        # Prepare the Base query
        query = "SELECT * FROM WorldNGOs WHERE 1=1"
        params = []

        # Add filters if provided
        if country:
            query += " AND Country = %s"
            params.append(country)
        if focus_area:
            query += " AND Focus_Area = %s"
            params.append(focus_area)
        if founding_year:
            query += " AND Founding_Year = %s"
            params.append(founding_year)

        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        ngos = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f'Successfully retrieved {len(ngos)} NGOs')
        return jsonify(ngos), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_ngos: {str(e)}')
        return jsonify({"error": str(e)}), 500
