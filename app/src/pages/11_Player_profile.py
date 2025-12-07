import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

playerInfo = requests.get(f"http://web-api:4000/players/{st.session_state['selected_playerID']}")
playerInfo = playerInfo.json()
# logger.info(playerInfo)

if st.session_state['selected_playerID'] != st.session_state['playerID']:
  if st.button("*This is not your profile. Click to view your profile*", type='tertiary'):
    st.session_state['selected_playerID'] = st.session_state['playerID']
    st.switch_page('pages/11_Player_profile.py')
    

st.title(f"#{playerInfo['jerseyNumber']} {playerInfo['name']} {playerInfo['gradYear']}")

st.write('')
st.write(f"{playerInfo['position']} on {playerInfo['teamName']}")
st.write(playerInfo['phoneNumber'])