import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

# Get team information
teamInfo = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}")
teamInfo = teamInfo.json()
logger.info(teamInfo)

st.title(f"{teamInfo['teamName']} - Player Statistics")

# Get all players from the team
players = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/players")
players = players.json()
logger.info(f"Players: {players}")

# Prepare data for the table
player_data = []

for player in players:
    # Get statistics for each player
    try:
        stats = requests.get(f"http://web-api:4000/stats/{player['playerID']}")
        stats_json = stats.json()

        # Aggregate statistics by type
        stat_counts = {}
        for stat_event in stats_json:
            stat_type = stat_event['statType']
            stat_counts[stat_type] = stat_counts.get(stat_type, 0) + 1

        # Create a row for this player
        player_row = {
            'Jersey #': player.get('jerseyNumber', 'N/A'),
            'Name': player.get('name', 'N/A'),
            'Position': player.get('position', 'N/A') 
        }

        # Add individual stat types as columns
        for stat_type, count in stat_counts.items():
            player_row[stat_type] = count

        player_data.append(player_row)
    except Exception as e:
        logger.error(f"Error fetching stats for player {player['playerID']}: {e}")
        # Add player without stats
        player_row = {
            'Jersey #': player.get('jerseyNumber', 'N/A'),
            'Name': player.get('name', 'N/A'),
            'Position': player.get('position', 'N/A')
        }
        player_data.append(player_row)

# Process and display data
if player_data:
    # Get unique positions for filtering
    all_positions = set()
    for player in player_data:
        pos = player.get('Position')
        if pos and pos != 'N/A':
            all_positions.add(pos)

    positions = ['All'] + sorted(list(all_positions))

    # Add position filter
    st.write("### Filter")
    selected_position = st.selectbox('Filter by Position:', positions)

    # Filter by position
    if selected_position != 'All':
        filtered_data = [p for p in player_data if p.get('Position') == selected_position]
    else:
        filtered_data = player_data

    st.write("### Player Statistics")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"Showing {len(filtered_data)} player(s)")
    with col2:
        csv_content = ""   # Convert to CSV manually for download
        if filtered_data:
            headers = list(filtered_data[0].keys())
            csv_content = ",".join(headers) + "\n"
            for row in filtered_data:
                csv_content += ",".join(str(row.get(h, "")) for h in headers) + "\n"

        st.download_button(
            label="Download CSV",
            data=csv_content,
            file_name=f"{teamInfo['teamName']}_player_stats.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Display the table - st.dataframe accepts list of dicts directly
    st.dataframe(filtered_data, use_container_width=True, hide_index=True)
else:
    st.write("No players found on this team.")
