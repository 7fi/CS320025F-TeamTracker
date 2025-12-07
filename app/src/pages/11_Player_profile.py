import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

playerInfo = requests.get(f"http://web-api:4000/players/{st.session_state['playerID']}")
playerInfo = playerInfo.json()
logger.info(playerInfo)


st.title(f"#{playerInfo['jerseyNumber']} {playerInfo['name']} {playerInfo['gradYear']}")
st.write('')
st.write(f"{playerInfo['position']} on {playerInfo['teamName']}")
st.write(playerInfo['phoneNumber'])