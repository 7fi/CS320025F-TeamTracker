import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

API = "http://web-api:4000"
SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}!")
st.write("")
st.write("### Create a Strategy")

coachID = st.session_state["userID"]
teamID = st.session_state["teamID"]

events = requests.get(f"{API}/teams/{teamID}/events").json()

event_map = {f"{e['title']} — {e['dateTime']}": e["eventID"] for e in events}

selected_event_label = st.selectbox("Choose Event:", list(event_map.keys()))
selected_event_id = event_map[selected_event_label]

with st.form("strategyForm"):
    formation = st.text_input("Formation (e.g., 4-3-3, 3-5-2):")
    result = st.selectbox("Result:", ["WIN", "LOSS", "DRAW"])

    submitted = st.form_submit_button("Save Strategy")

    if submitted:
        payload = {
            "formation": formation,
            "eventID": selected_event_id,
            "result": result
        }

        r = requests.post(f"{API}/coaches/{coachID}/strategy", json=payload)

        if r.status_code == 201:
            st.success("Strategy saved!")
            st.rerun()
        else:
            st.error("Failed: " + r.text)

st.write("## Past Strategies")

resp = requests.get(f"{API}/coaches/{coachID}/strategy")

if resp.status_code == 200:
    strategies = resp.json()

    for s in strategies:
        st.write(f"### {s['title']} ({s['dateTime']})")
        st.write(f"- **Formation:** {s['formation']}")
        st.write(f"- **Result:** {s['result']}")
        st.write("---")
else:
    st.error("Could not load strategies")
