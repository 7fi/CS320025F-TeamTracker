import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Statistics of {st.session_state['first_name']}!")
st.write('')

stats = requests.get(f"http://web-api:4000/stats/{st.session_state['playerID']}")
stats = stats.json()
logger.info(stats)

for statEvent in stats:
  st.write(f"**{statEvent['statType']}** at {statEvent['dateTime']}")