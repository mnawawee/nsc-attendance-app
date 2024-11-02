import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def make_sidebar():
    # Custom CSS for sidebar button styling
    sidebar_style = """
    <style>
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
    st.markdown(sidebar_style, unsafe_allow_html=True)

    with st.sidebar:
        st.image('NCS.png', width=90)
        st.markdown('<h1 style="color:green; text-align:left;">NCS Attendance Tracker</h1>', unsafe_allow_html=True)
      
        # Add a horizontal divider
        st.divider()
        
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/2_Registration_form.py", label="Manage User", icon="🕵️")
            st.page_link("pages/1_Real_Time_Prediction.py", label="Manage Attendance", icon="🚶")
            st.page_link("pages/3_Report.py", label="Manage Report", icon="🎫")

            st.write("")
            st.write("")

            # Style the Log out button
            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")
            st.markdown(hide_menu, unsafe_allow_html=True)

def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("streamlit_app.py")
