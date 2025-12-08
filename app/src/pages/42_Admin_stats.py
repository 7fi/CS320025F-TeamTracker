import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Sidebar
SideBarLinks()

API = 'http://web-api:4000'

teamInfo = requests.get(f"{API}/teams/{st.session_state['teamID']}").json()
teamID = st.session_state['teamID']

st.title(f"{teamInfo['teamName']} - Player Statistics")

events = requests.get(f"{API}/teams/{teamID}/events").json()

if len(events) == 0:
    st.warning("No events found.")
    st.stop()

event_options = {f"{e['title']} — {e['dateTime']}": e["eventID"] for e in events}

st.subheader("Add Player Stats")

selected_event_label = st.selectbox("Select Event", list(event_options.keys()))
selected_event_id = event_options[selected_event_label]

# Load players in this event
player_event_resp = requests.get(f"{API}/events/{selected_event_id}/players")
if player_event_resp.status_code != 200:
    st.error("Could not load players for this event.")
    st.stop()

event_players = player_event_resp.json()
player_map = {p["name"]: p["playerID"] for p in event_players}

selected_player_name = st.selectbox("Select Player", list(player_map.keys()))
selected_player_id = player_map[selected_player_name]

stat_type = st.selectbox(
    "Stat Type",
    ["Goal", "Assist", "Save", "Shot", "Foul", "Yellow card", "Red card"]
)

if st.button("Add Stat"):
    payload = {
        "statType": stat_type,
        "eventID": selected_event_id,
        "playerID": selected_player_id
    }

    r = requests.post(f"{API}/stats/", json=payload)

    if r.status_code == 201:
        st.success(f"Added stat: {selected_player_name} → {stat_type}")
        st.rerun()
    else:
        st.error(f"Failed to save stat: {r.text}")

st.write("---")

st.subheader("Total Player Statistics")

# Load all team players
players = requests.get(f"{API}/teams/{teamID}/players").json()

player_data = []

for player in players:
    try:
        stats = requests.get(f"{API}/stats/{player['playerID']}").json()

        stat_counts = {}
        for stat_event in stats:
            stat_type = stat_event['statType']
            stat_counts[stat_type] = stat_counts.get(stat_type, 0) + 1

        row = {
            'Jersey #': player.get('jerseyNumber'),
            'Name': player.get('name'),
            'Position': player.get('position')
        }

        for stat_name, count in stat_counts.items():
            row[stat_name] = count

        player_data.append(row)

    except Exception as e:
        logger.error(f"Failed to load stats for player {player['playerID']}: {e}")

if player_data:
    st.write("### Filter by Position")
    positions = ['All'] + sorted({p.get('Position') for p in player_data if p.get('Position')})

    selected_pos = st.selectbox("", positions)

    if selected_pos != "All":
        filtered_data = [p for p in player_data if p.get('Position') == selected_pos]
    else:
        filtered_data = player_data

    st.dataframe(filtered_data, use_container_width=True, hide_index=True)
else:
    st.info("No players found.")
