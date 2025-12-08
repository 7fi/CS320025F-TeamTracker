import logging
logger = logging.getLogger(__name__)
import requests
from datetime import date

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

teamInfo = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}")
teamInfo = teamInfo.json()

st.title(f"{teamInfo['teamName']} - Player Injuries")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["View Injuries", "Add New Injury", "Update/Delete Injury"])

# Get all players from the team
players = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/players")
players = players.json()

# TAB 1: View all injuries
with tab1:
    st.write("### All Team Injuries")

    # Collect all injuries by looping through all players injuries in the team
    all_injuries = []
    for player in players:
        try:
            injuries = requests.get(f"http://web-api:4000/players/{player['playerID']}/injuries")
            injuries = injuries.json()

            for injury in injuries:
                injury_row = {
                    'Injury ID': injury.get('injuryID', 'N/A'),
                    'Player ID': player.get('playerID', 'N/A'),
                    'Player Name': player.get('name', 'N/A'),
                    'Jersey #': player.get('jerseyNumber', 'N/A'),
                    'Position': player.get('position', 'N/A'),
                    'Injury Type': injury.get('type', 'N/A'),
                    'Injury Date': injury.get('date', 'N/A'),
                    'Recovery Date': injury.get('recoveryDate', 'N/A')
                }
                all_injuries.append(injury_row)
        except Exception as e:
            logger.error(f"Error fetching injuries for player {player['playerID']}: {e}")

    if all_injuries:
        st.dataframe(all_injuries, use_container_width=True, hide_index=True)
    else:
        st.write("No injuries found for this team")

# TAB 2: Add new injury
with tab2:
    st.write("### Add New Injury Report")

    # Create player dropdown
    player_options = {f"{p['name']} (#{p['jerseyNumber']})": p['playerID'] for p in players}
    selected_player_name = st.selectbox("Select Player:", list(player_options.keys()))
    selected_player_id = player_options[selected_player_name]

    # Injury form
    col1, col2 = st.columns(2)

    with col1:
        injury_type = st.text_input("Injury Type:", placeholder="e.g., Sprained Ankle, Concussion")
        injury_date = st.date_input("Injury Date:", value=date.today())

    with col2:
        recovery_date = st.date_input("Expected Recovery Date:", value=date.today())

    if st.button("Add Injury Report", type="primary"):
        if not injury_type:
            st.error("Please enter an injury type")
        else:
            try:
                response = requests.post(
                    f"http://web-api:4000/players/{selected_player_id}/injuries",
                    json={
                        "injuryType": injury_type,
                        "injuryDate": str(injury_date),
                        "recoveryDate": str(recovery_date)
                    }
                )

                if response.status_code == 201:
                    st.success("Injury report added successfully!")
                    st.rerun()
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to add injury: {str(e)}")

# TAB 3: Update or delete injury
with tab3:
    st.write("### Update or Delete Injury Report")

    if all_injuries:
        # Select injury to modify
        injury_options = {
            f"ID {inj['Injury ID']}: {inj['Player Name']} - {inj['Injury Type']} ({inj['Injury Date']})":
            {'injuryID': inj['Injury ID'], 'playerID': inj['Player ID']}
            for inj in all_injuries
        }

        selected_injury_name = st.selectbox("Select Injury:", list(injury_options.keys()))
        selected_injury = injury_options[selected_injury_name]

        # Find the full injury details
        injury_details = next((inj for inj in all_injuries if inj['Injury ID'] == selected_injury['injuryID']), None)

        if injury_details:
            st.write("---")
            st.write("**Current Details:**")
            st.write(f"- Player: {injury_details['Player Name']}")
            st.write(f"- Injury Type: {injury_details['Injury Type']}")
            st.write(f"- Injury Date: {injury_details['Injury Date']}")
            st.write(f"- Recovery Date: {injury_details['Recovery Date']}")
            st.write("---")

            # Two sections: Update and Delete
            col1, col2 = st.columns(2)

            with col1:
                st.write("#### Update Injury")

                new_injury_type = st.text_input("New Injury Type:", value=injury_details['Injury Type'])

                # Handle date conversion safely
                try:
                    injury_date_value = date.fromisoformat(str(injury_details['Injury Date']))
                except (ValueError, TypeError):
                    injury_date_value = date.today()

                try:
                    recovery_date_value = date.fromisoformat(str(injury_details['Recovery Date']))
                except (ValueError, TypeError):
                    recovery_date_value = date.today()

                new_injury_date = st.date_input("New Injury Date:", value=injury_date_value)
                new_recovery_date = st.date_input("New Recovery Date:", value=recovery_date_value)

                if st.button("Update Injury Report", type="primary"):
                    try:
                        response = requests.put(
                            f"http://web-api:4000/players/{selected_injury['playerID']}/injuries",
                            json={
                                "injuryID": selected_injury['injuryID'],
                                "injuryType": new_injury_type,
                                "injuryDate": str(new_injury_date),
                                "recoveryDate": str(new_recovery_date)
                            }
                        )

                        if response.status_code == 200:
                            st.success("Injury report updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Failed to update injury: {str(e)}")

            with col2:
                st.write("#### Delete Injury")
                st.write("Do NOT delete injuries just because the player recovered.")

                if st.button("Delete Injury Report", type="secondary"):
                    try:
                        response = requests.delete(
                            f"http://web-api:4000/players/{selected_injury['playerID']}/injuries",
                            json={"injuryID": selected_injury['injuryID']}
                        )

                        if response.status_code == 200:
                            st.success("Injury report deleted successfully")
                            st.rerun()
                        else:
                            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Failed to delete injury: {str(e)}")
    else:
        st.info("No injuries to update or delete. Add an injury first in the 'Add New Injury' tab.")
