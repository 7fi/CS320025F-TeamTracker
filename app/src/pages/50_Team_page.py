import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

teamInfo = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}")
teamInfo = teamInfo.json()
logger.info(teamInfo)

st.title(teamInfo['teamName'])

players = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/players")
logger.info(st.session_state['teamID'])
players = players.json()
logger.info(players)

st.write("### Players")
for player in players:
  if st.button(f"#{player['jerseyNumber']} {player['name']} | {player['gradYear']} | {player['phoneNumber']}", type='tertiary'):
    st.session_state['selected_ID'] = player['playerID']
    st.switch_page('pages/11_Player_profile.py')
    

coaches = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/coaches")
logger.info(st.session_state['teamID'])
coaches = coaches.json()
logger.info(coaches)

analysts = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/analysts")
logger.info(st.session_state['teamID'])
analysts = analysts.json()
logger.info(analysts)

st.write("### Coaches")

for coach in coaches:
  if st.button(f"{coach['name']} | {coach['phoneNumber']}", type='tertiary'):
    st.session_state['selected_ID'] = coach['coachID']
    st.switch_page('pages/21_Coach_profile.py')
    
for analyst in analysts:
  if st.button(f"{analyst['name']} | {analyst['phoneNumber']}", type='tertiary'):
    st.session_state['selected_ID'] = analyst['analystID']
    st.switch_page('pages/31_Analyst_profile.py')