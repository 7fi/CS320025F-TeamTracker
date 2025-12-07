import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

playerInfo = requests.get(f"http://web-api:4000/players/{st.session_state['playerID']}").json()
logger.log(playerInfo)


st.title(f"{st.session_state['first_name']}")
st.write('')
st.write('')
st.write('### Here is his Profile!')