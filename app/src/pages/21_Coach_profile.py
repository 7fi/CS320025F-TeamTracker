import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

coachInfo = requests.get(f"http://web-api:4000/coaches/{st.session_state['selected_ID']}")
coachInfo = coachInfo.json()
logger.info(coachInfo)

if st.session_state['role'] == 'coach' and st.session_state['selected_ID'] != st.session_state['userID']:
  if st.button("*This is not your profile. Click to view your profile*", type='tertiary'):
    st.session_state['selected_ID'] = st.session_state['userID']
    st.switch_page('pages/11_Player_profile.py')
    

st.title(f"Coach {coachInfo['name']}")

st.write('')
st.write(f"{coachInfo['teamName']}")
st.write(coachInfo['email'])
st.write(coachInfo['phoneNumber'])