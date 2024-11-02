import streamlit as st
import redis
import numpy as np
import pandas as pd
# from streamlit_calendar import calendar

# Set up the page configuration
# st.set_page_config(page_title='NCS Admin Dashboard', layout='wide')

# Custom CSS for styling
st.markdown("""
    <style>
        .main-header {
            font-size: 2em;
            font-weight: bold;
            color: #4CAF50;
        }
        .sub-header {
            font-size: 1.5em;
            font-weight: bold;
            color: #4CAF50;
            margin-top: 20px;
        }
        .metric-container {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }
        .calendar-container {
            margin-top: 20px;
            width: 100%;
            display: flex;
            justify-content: center; /* Centers the calendar horizontally */
        }
        .calendar-container .stCalendar {
            width: 100%;
            max-width: 1200px; /* Adjust this value as needed */
        }
        .dataframe-container {
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Display the logo
# st.image('NCS.png', width=100)

# # Display the main header
# st.markdown('<div class="main-header">NCS Attendance System</div>', unsafe_allow_html=True)

# Display the spinner while loading models and connecting to the database
with st.spinner("Loading Models and Connecting to Database..."):
    import face_rec

# Indicate successful loading and connection
# st.success('Models loaded successfully')
# st.success('Database successfully connected')

# Connect to Redis database
hostname = 'redis-19064.c10.us-east-1-4.ec2.redns.redis-cloud.com'
portNum = 19064
password ='zyMJ3Qc07ykhj3BuCKaiBV4s7b1maDSm'

r = redis.StrictRedis(host=hostname, port=portNum, password=password)

# Function to retrieve attendance logs from Redis
def get_attendance_logs():
    logs = r.lrange('attendance:logs', 0, -1)
    attendance_df = pd.DataFrame([log.decode().split('@') for log in logs], columns=['Name', 'Role', 'Timestamp'])
    return attendance_df

# Retrieve attendance logs
attendance_df = get_attendance_logs()

# Calculate the total number of people present and absent
total_present = len(attendance_df[attendance_df['Role'] != 'Unknown'])
total_absent = len(attendance_df[attendance_df['Role'] == 'Unknown'])

# Display cards showing total number of people present and absent
# st.markdown('<div class="metric-container">', unsafe_allow_html=True)
# col1, col2 = st.columns(2)
# with col1:
#     st.metric(label="Total Present", value=total_present)
# with col2:
#     st.metric(label="Total Absent", value=total_absent)
# st.markdown('</div>', unsafe_allow_html=True)

# # Add the calendar
# st.markdown('<div class="sub-header">Attendance Calendar</div>', unsafe_allow_html=True)
# st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
# # cal = calendar()  # Display the calendar
# st.markdown('</div>', unsafe_allow_html=True)

hide_streamlit_style= """
<style>
#MainMenu {visibility: hidden}

</style>
"""

st.markdown(hide_streamlit_style,unsafe_allow_html=True)