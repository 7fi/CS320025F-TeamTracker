import logging
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
playerNames = ['Marc', 'Carter', 'Freddy']
coaches = ['Marc', 'Carter', 'Freddy']
analysts = []
admins = ['Admin']

for playerName in playerNames:
  if st.button(f"Act as {playerName}, a College Soccer Player", 
                type = 'primary', 
                use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'player'
    st.session_state['first_name'] = playerNames
    st.switch_page('pages/10_Player_home.py')

if st.button('Act as John, a Team Coach', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'coach'
    st.session_state['first_name'] = 'John'
    st.switch_page('pages/20_Coach_home.py')

if st.button('Act as Ben, a Team Analyst/Assistant Coach', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'analyst'
    st.session_state['first_name'] = 'Ben'
    st.switch_page('pages/30_Analyst_home.py')

for adminName in admins:
    if st.button(f'Act as {adminName} a Team Admin', 
                type = 'primary', 
                use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'admin'
        st.session_state['first_name'] = adminName
        st.switch_page('pages/40_Admin_home.py')