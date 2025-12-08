import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from datetime import datetime, time, date
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

API = "http://web-api:4000"
SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}!")
st.write("")
st.write("### Create a Team Event (Admin)")

adminID = st.session_state["userID"]
teamID = st.session_state["teamID"]

# Create Event Form
with st.form("eventForm"):
    title = st.text_input("Event Title:", placeholder="e.g., Practice vs. Team A, Film Session")
    location = st.text_input("Location:", placeholder="e.g., Main Field, Gym, Film Room")

    col1, col2 = st.columns(2)
    with col1:
        event_date = st.date_input("Event Date:", value=date.today())

    with col2:
        event_time = st.time_input("Event Time:", value=time(18, 0))  

    submitted = st.form_submit_button("Create Event")

    if submitted:
        if not title or not location:
            st.error("Please fill in both title and location.")
        else:
            # Combine date and time into a single datetime string
            event_datetime = datetime.combine(event_date, event_time).isoformat(sep=" ")

            payload = {
                "title": title,
                "location": location,
                "dateTime": event_datetime
            }

            try:
                # backend accepts POST /teams/{teamID}/events to create an event for a team
                r = requests.post(f"{API}/teams/{teamID}/events", json=payload)

                if r.status_code == 201:
                    st.success("Event created successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create event: " + r.text)
            except Exception as e:
                logger.error(f"Error creating event: {e}")
                st.error(f"Error creating event: {e}")

# Past Events for this Team
st.write("## Existing Events")

try:
    resp = requests.get(f"{API}/teams/{teamID}/events")
    if resp.status_code == 200:
        events = resp.json()

        if events:
            for e in events:
                st.write(f"### {e.get('title', 'Untitled Event')} ({e.get('dateTime', 'No time set')})")
                st.write(f"- **Location:** {e.get('location', 'Unknown')}")
                st.write("---")
        else:
            st.info("No events created yet for this team.")
    else:
        st.error("Could not load events: " + resp.text)
except Exception as e:
    logger.error(f"Error fetching events: {e}")
    st.error(f"Error loading events: {e}")
