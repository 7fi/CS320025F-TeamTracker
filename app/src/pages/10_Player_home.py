import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks
from datetime import datetime, timezone

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}!")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View my stats', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Player_stats.py')

if st.button('View my profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Player_profile.py')

if st.button('View my team', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/50_Team_page.py')


events = requests.get(f"http://web-api:4000/events/player/{st.session_state['playerID']}")
events = events.json()
logger.info(events)

if(len(events) > 0):
  st.write("### Your next events: ")
  for event in events: 
    s = event['dateTime']
    dt = datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
    st.write(f"##### {event['title']}")
    st.write(f"**{event['location']}** on {dt.date()} at {dt.time()}")