from navigation import make_sidebar
import streamlit as st
from Home import face_rec
import cv2
import time
import numpy as np
from PIL import Image

make_sidebar()

st.markdown('<h3 style="color:green;">Mark Attendance</h3>', unsafe_allow_html=True)

# Retrieve the data from Redis Database
with st.spinner('Retrieving Data from Db...'):
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)

st.success('Data successfully retrieved from database')

# Time settings
waitTime = 3  # Time in seconds
setTime = time.time()
realtimepred = face_rec.RealTimePred()  # Real-time prediction class

# Streamlit UI Components
stframe = st.empty()
start_button = st.button("Start Attendance Marking")
stop_button = st.button("Stop Attendance Marking")

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

if start_button:
    st.session_state["attendance_running"] = True

if stop_button:
    st.session_state["attendance_running"] = False

# Process video stream
if "attendance_running" not in st.session_state:
    st.session_state["attendance_running"] = False

while st.session_state["attendance_running"]:
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to capture video")
        break

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform face recognition and prediction
    pred_img = realtimepred.face_prediction(
        img, redis_face_db, 'facial_feature', ['Name', 'Role'], thresh=0.5
    )

    # Save logs to Redis every waitTime seconds
    timenow = time.time()
    if (timenow - setTime) >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time()  # Reset time
        print('Saved data to database')

    # Display the processed image in Streamlit
    stframe.image(Image.fromarray(pred_img), use_container_width=True)

cap.release()
cv2.destroyAllWindows()

# Hide Streamlit's default main menu
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
