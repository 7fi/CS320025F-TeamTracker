import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.write("Team page")

players = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/players")
logger.info(st.session_state['teamID'])
players = players.json()
logger.info(players)

# players = [{'\#' : p['jerseyNumber'], 'Name': p['name'], 'Grad Year': p['gradYear'], 'Phone' : p['phoneNumber']} for p in players]

# st.table(players)

for player in players:
  if st.button(f"#{player['jerseyNumber']} {player['name']} | {player['gradYear']} | {player['phoneNumber']}", type='tertiary'):
    st.session_state['selected_playerID'] = player['playerID']
    st.switch_page('pages/11_Player_profile.py')