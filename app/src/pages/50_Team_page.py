import logging
logger = logging.getLogger(__name__)
import requests
from datetime import datetime, timezone

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

API_URL = "http://web-api:4000"

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

teamInfo = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}")
teamInfo = teamInfo.json()
logger.info(teamInfo)

st.title(teamInfo['teamName'])

players = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/players")
logger.info(st.session_state['teamID'])
players = players.json()
logger.info(players)

st.write("### Players")
for player in players:
  if st.button(f"#{player['jerseyNumber']} {player['name']} '{str(player['gradYear'])[-2:]} | {player['phoneNumber']}", type='tertiary'):
    st.session_state['selected_ID'] = player['playerID']
    st.switch_page('pages/11_Player_profile.py')
  
if st.session_state['role'] == 'admin':
  st.write("### Edit Players")
  
  teamID = st.session_state["teamID"]
  players = requests.get(f"http://web-api:4000/teams/{teamID}/players").json()

  for p in players:
    col1, col2 = st.columns(2)
    with col1:
      st.write(f"{p['name']}")

    with col2:
      if st.button(f"Edit {p['name']}", key=f"edit_{p['playerID']}"):
        st.session_state["editing"] = p
        
    if st.session_state['editing'] is not None and st.session_state.get("editing", {}).get("playerID") == p["playerID"]:

      new_name = st.text_input("Name", p["name"], key=f"name_{p['playerID']}")
      newPosition = st.text_input("Position", p["position"], key=f"pos_{['playerID']}")
      newPhoneNumber = st.text_input("Phone Number", p["phoneNumber"], key=f"num_{['playerID']}")
      newJerseyNumber = st.text_input("Jersey Number", p["jerseyNumber"], key=f"jersey_{['playerID']}")
      newGradYear = st.text_input("Grad Year", p["gradYear"], key=f"grad_{['playerID']}")


      if st.button("Save", key=f"save_{p['playerID']}"):
        payload = {
          "name": new_name,
          "position": newPosition,
          "phoneNumber": newPhoneNumber,
          "jerseyNumber": newJerseyNumber,
          "gradYear": newGradYear
        }

        r = requests.put(f"http://web-api:4000/players/{p['playerID']}", json=payload)
        response = r.json()
        
        logger.info(response)

        if r.status_code == 200:
          st.success("Updated Sucessfully!")
          st.session_state["editing"] = {}
          st.rerun()
        else:
          st.error("error")

      delete_col1, delete_col2 = st.columns([1, 3])
      with delete_col1:
        if st.button("Delete Player", key=f"delete_{p['playerID']}"):
          delete_url = f"http://web-api:4000/players/{p['playerID']}"

          delete_response = requests.delete(delete_url)

          if delete_response.status_code == 200:
            st.success(f"{p['name']} deleted.")
            st.session_state["editing"] = {}
            st.rerun()
          else:
            st.error("error")

coaches = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/coaches")
logger.info(st.session_state['teamID'])
coaches = coaches.json()
logger.info(coaches)

analysts = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/analysts")
logger.info(st.session_state['teamID'])
analysts = analysts.json()
logger.info(analysts)

st.write("### Coaches")

for coach in coaches:
  if st.button(f"{coach['name']} | {coach['phoneNumber']}", type='tertiary'):
    st.session_state['selected_ID'] = coach['coachID']
    st.switch_page('pages/21_Coach_profile.py')
    
for analyst in analysts:
  if st.button(f"{analyst['name']} | {analyst['phoneNumber']}", type='tertiary'):
    st.session_state['selected_ID'] = analyst['analystID']
    st.switch_page('pages/31_Analyst_profile.py')
    
    
def rsvpForEvent(eventID, value):
  data = {
    'playerID' : st.session_state['userID'],
  }

  try:
    if value:
      # Send POST request to API
      response = requests.post(API_URL + f"/events/rsvp/{eventID}", json=data)
    else: 
      response = requests.delete(API_URL + f"/events/rsvp/{eventID}", json=data)

    if response.status_code == 200:
        st.session_state.show_success_modal = True
        st.success("Sucessfully RSVP")
        st.rerun()
    else:
        st.error(
            f"Failed to rsvp: {response.json().get('error', 'Unknown error')}"
        )

  except requests.exceptions.RequestException as e:
      st.error(f"Error connecting to the API: {str(e)}")
      st.info("Please ensure the API server is running")
  pass
    
events = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/events")
events = events.json()
logger.info(events)

attendanceRecords = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/attendance")
attendanceRecords = attendanceRecords.json()
logger.info([e['playerID'] for e in attendanceRecords])

if(len(events) > 0):
  st.write(f"### {teamInfo['teamName']}'s next events: ")
  for event in events: 
    s = event['dateTime']
    dt = datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
    rsvpText = ""
    if st.session_state['role'] == 'player':
      rsvpStatus = st.session_state['userID'] in [e['playerID'] for e in attendanceRecords if e['eventID'] == event['eventID']]
      rsvpText = "✅" if rsvpStatus else "❌"
      rsvpText = "Going? " + rsvpText
      
    st.write(f"##### {event['title']}")
    st.write(f"**{event['location']}** on {dt.date()} at {dt.time()} {rsvpText}")
    
    if st.session_state['role'] == 'player':
      col1, col2, col3 = st.columns([0.1,.1,1])
      with col1:
        st.write("RSVP:")
      with col2:
        if st.button("Yes", key={"yes" + str(event['eventID'])}):
          rsvpForEvent(event['eventID'], True)

      with col3:
        if st.button("No",  key={"no" + str(event['eventID'])}):
          rsvpForEvent(event['eventID'], False)