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

playerNames = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/players")
logger.info(st.session_state['teamID'])
logger.info(playerNames)
playerNames = playerNames.json()
  
playerNames = [p['name'] for p in playerNames]

for playerName in playerNames:
  if st.button(f"Act as {playerName}, a College Soccer Player", 
                type = 'primary', 
                use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'player'
    st.session_state['first_name'] = playerNames
    st.switch_page('pages/10_Player_home.py')



coachNames = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/players")
logger.info(st.session_state['teamID'])
logger.info(coachNames)
coachNames = coachNames.json()
  
coachNames = [p['name'] for p in coachNames]

for coachName in coachNames:
  if st.button(f'Act as {coachName}, a Team Coach', 
              type = 'primary', 
              use_container_width=True):
      st.session_state['authenticated'] = True
      st.session_state['role'] = 'coach'
      st.session_state['first_name'] = coachName
      st.switch_page('pages/20_Coach_home.py')


analysts = []


if st.button('Act as Ben, a Team Analyst/Assistant Coach', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'analyst'
    st.session_state['first_name'] = 'Ben'
    st.switch_page('pages/30_Analyst_home.py')

admins = ['Admin']


for adminName in admins:
    if st.button(f'Act as {adminName} a Team Admin', 
                type = 'primary', 
                use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'admin'
        st.session_state['first_name'] = adminName
        st.switch_page('pages/40_Admin_home.py')