import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

teamInfo = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}")
teamInfo = teamInfo.json()

st.title(f"{teamInfo['teamName']} - Player Comments")

# Get all players from the team
players = requests.get(f"http://web-api:4000/teams/{st.session_state['teamID']}/players")
players = players.json()

st.write("### Select a Player")
st.write("Click on a player to view and add comments:")

# Display players as clickable buttons
for player in players:
    if st.button(
        f"#{player.get('jerseyNumber', 'N/A')} {player.get('name', 'N/A')} - {player.get('position', 'N/A')}",
        key=f"player_{player['playerID']}",
        use_container_width=True
    ):
        st.session_state['selected_player_for_comments'] = player['playerID']
        st.session_state['selected_player_name'] = player.get('name', 'Unknown Player')

if 'selected_player_for_comments' in st.session_state:
    st.write("---")

    selected_player_id = st.session_state['selected_player_for_comments']
    selected_player_name = st.session_state.get('selected_player_name', 'Unknown Player')

    st.write(f"## Comments for {selected_player_name}")

    # Fetch comments for the selected player
    try:
        comments_response = requests.get(f"http://web-api:4000/players/{selected_player_id}/comments")
        comments = comments_response.json()

        st.write("### Existing Comments")

        if comments:
            for comment in comments:
                col1, col2 = st.columns([4, 1])

                with col1:
                    with st.container():
                        st.write(f"**Comment ID:** {comment.get('commentID', 'N/A')}")
                        st.write(f"**Text:** {comment.get('text', 'N/A')}")
                        st.write(f"**Date/Time:** {comment.get('dateTime', 'N/A')}")
                        st.write(f"**Commenter ID:** {comment.get('commenterID', 'N/A')}")

                with col2:
                    if st.button("Delete", key=f"delete_comment_{comment.get('commentID')}", type="secondary"):
                        try:
                            response = requests.delete(
                                f"http://web-api:4000/players/{selected_player_id}/comments",
                                json={"commentID": comment.get('commentID')}
                            )

                            if response.status_code == 200:
                                st.success("Comment deleted successfully")
                                st.rerun()
                            else:
                                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"Failed to delete comment: {str(e)}")

                st.divider()
        else:
            st.info("No comments yet for this player.")

        st.write("### Add New Comment")

        comment_text = st.text_area(
            "Your Comment:",
            placeholder="Enter feedback...",
            height=150
        )

        if st.button("Submit Comment", type="primary"):
            if not comment_text or comment_text.strip() == "":
                st.error("Please enter a comment before submitting.")
            else:
                try:
                    response = requests.post(
                        f"http://web-api:4000/players/{selected_player_id}/comments",
                        json={
                            "text": comment_text,
                            "commenterID": st.session_state['userID']
                        }
                    )

                    if response.status_code == 201:
                        st.success("Comment added successfully")
                        st.rerun()
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Failed to add comment: {str(e)}")

    except Exception as e:
        st.error(f"Failed to load comments: {str(e)}")
else:
    st.info("Select a player above to view and add comments.")
