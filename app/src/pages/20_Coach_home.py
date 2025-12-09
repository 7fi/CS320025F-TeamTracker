import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Coach {st.session_state['first_name']}!")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View my profile',  
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Coach_profile.py') ## redirection to coach profile
  
if st.button('View my team', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/50_Team_page.py') ## redirection to team page

if st.button('View Team Statistics',
             type='primary',
             use_container_width=True):
     st.switch_page('pages/32_Analyst_team_stats.py') ## redirection to team statistics page

if st.button('View strategies', 
                 type='primary',
                 use_container_width=True):
  st.switch_page('pages/22_Coach_strategy.py') ## redirection to strategies page

