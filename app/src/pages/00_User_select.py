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

if st.button("Act as Mark, a College Soccer Player", 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'player'
    st.session_state['first_name'] = 'Mark'
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

if st.button('Act as a Team Admin', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'admin'
    st.session_state['first_name'] = 'Admin'
    st.switch_page('pages/40_Admin_home.py')