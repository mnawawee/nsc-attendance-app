import streamlit as st
from time import sleep
from navigation import make_sidebar

make_sidebar()

# Centering the title with custom color
center_title_style = """
    <style>
    .title {
        color: green;
        font-size: 25px;
        text-align: center;
    }
    /* Custom styles for the button */
    div.stButton > button {
        background-color: green !important; /* Force green even when clicked */
        color: white !important;
        border-radius: 10px !important;
        border: 2px solid green !important;
        transition: background-color 0.3s !important;
    }

    div.stButton > button:hover {
        background-color: darkgreen !important; /* Dark green on hover */
    }

    div.stButton > button:active {
        background-color: green !important; /* Keep green when clicked */
        border: 2px solid green !important;
    }

    div.stButton > button:focus {
        outline: none !important; /* Remove outline */
    }
    </style>
"""

# Insert the CSS for the title and button
st.markdown(center_title_style, unsafe_allow_html=True)

# Create two empty columns for centering
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Create a title with custom color
    st.markdown('<h1 class="title">Welcome to NCS Attendance Tracker. </h1>', unsafe_allow_html=True)  # Center title

# User inputs
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Button and login logic
if st.button("Log in", type="primary"):
    if username == "ICT" and password == "@NCS_A123":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/2_Registration_form.py")
    else:
        st.error("Incorrect username or password")

# Hide Streamlit's default main menu
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
