import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.write('#### HI! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

# TODO: get names from api

st.session_state["editing"] = {}

players = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/players")
logger.info(st.session_state['teamID'])
logger.info(players)
players = players.json()

player_options = {p["name"]: p for p in players}

selected_name = st.selectbox(
    "Choose a player to act as:",
    list(player_options.keys()),
    index=None,
    placeholder="Select a player..."
)

if st.button("Select Player", type="primary", use_container_width=True):
    if selected_name is None:
        st.warning("Please select a player.")
    else:
        player = player_options[selected_name]

        st.session_state['authenticated'] = True
        st.session_state['role'] = 'player'
        st.session_state['userID'] = player["playerID"]
        st.session_state['selected_ID'] = player["playerID"]
        st.session_state['first_name'] = player["name"]

        st.switch_page("pages/10_Player_home.py")


coaches = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/coaches")
logger.info(st.session_state['teamID'])
logger.info(coaches)
coaches = coaches.json()

coach_options = {p["name"]: p for p in coaches}

selected_name = st.selectbox(
    "Choose a coach to act as:",
    list(coach_options.keys()),
    index=None,
    placeholder="Select a coach..."
)

if st.button("Select Coach", type="primary", use_container_width=True):
    if selected_name is None:
        st.warning("Please select a coach.")
    else:
        coach = coach_options[selected_name]

        st.session_state['authenticated'] = True
        st.session_state['role'] = 'coach'
        st.session_state['userID'] = coach['coachID']
        st.session_state['selected_ID'] = coach['coachID']
        st.session_state['first_name'] = coach['name']
        st.switch_page('pages/20_Coach_home.py')

analysts = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/analysts")
logger.info(st.session_state['teamID'])
logger.info(analysts)
analysts = analysts.json()

analyst_options = {p["name"]: p for p in analysts}

selected_name = st.selectbox(
    "Choose a analyst to act as:",
    list(analyst_options.keys()),
    index=None,
    placeholder="Select a analyst..."
)

if st.button("Select Analyst", type="primary", use_container_width=True):
    if selected_name is None:
        st.warning("Please select a analyst.")
    else:
        analyst = analyst_options[selected_name]

        st.session_state['authenticated'] = True
        st.session_state['role'] = 'analyst'
        st.session_state['userID'] = analyst['analystID']
        st.session_state['selected_ID'] = analyst['analystID']
        st.session_state['first_name'] = analyst['name']
        st.switch_page('pages/30_Analyst_home.py')

admins = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/admins")
logger.info(st.session_state['teamID'])
logger.info(admins)
admins = admins.json()

admin_options = {p["name"]: p for p in admins}

selected_name = st.selectbox(
    "Choose a admin to act as:",
    list(admin_options.keys()),
    index=None,
    placeholder="Select a admin..."
)

if st.button("Select Admin", type="primary", use_container_width=True):
    if selected_name is None:
        st.warning("Please select a admin.")
    else:
        admin = admin_options[selected_name]

        st.session_state['authenticated'] = True
        st.session_state['role'] = 'admin'
        st.session_state['userID'] = admin['adminID']
        st.session_state['selected_ID'] = admin['adminID']
        st.session_state['first_name'] = admin['name']
        st.switch_page('pages/40_Admin_home.py')