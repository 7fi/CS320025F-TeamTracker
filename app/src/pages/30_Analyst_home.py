import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Analyst {st.session_state['first_name']}!")
st.write('')

if st.button('View Team Statistics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Analyst_team_stats.py')

if st.button('View Team Injuries',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_Analyst_team_injuries.py')

if st.button('View / Add Comments to Players',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/34_Analyst_comment.py')
