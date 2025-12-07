# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/60_About.py", label="About", icon="🧠")

### ------ Player Role ------

def PlayerHomePageNav():
    st.sidebar.page_link("pages/10_Player_home.py", label='Home', icon="🏠")
    
def ProfilePageNav():
    st.sidebar.page_link("pages/11_Player_profile.py", label='Profile', icon="👤")
    
def PlayerStatsNav():
    st.sidebar.page_link("pages/12_Player_stats.py", label='Stats', icon="📈")
    
def PlayerTeamNav():
    st.sidebar.page_link("pages/50_Team_page.py", label='Team', icon="👥")


def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "player":
            PlayerHomePageNav()
            PlayerTeamNav()
            ProfilePageNav()
            PlayerStatsNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
