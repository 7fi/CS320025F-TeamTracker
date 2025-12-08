import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    This is a app to help track sports teams and manage their day-to-day activities. 
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
