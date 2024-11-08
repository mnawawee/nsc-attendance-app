import streamlit as st
from navigation import make_sidebar
from Home import face_rec
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

make_sidebar()

# Custom CSS to style the button and prevent color change
st.markdown("""
    <style>
    div.stButton > button {
        background-color: green !important; /* Force green even when clicked */
        color: white !important;
        border-radius: 10px !important;
        border: 2px solid green !important;
        transition: background-color 0.3s !important;
    }
    
    div.stButton > button:hover {
        background-color: darkgreen !important; /* Stay green but darker on hover */
    }
    
    div.stButton > button:active {
        background-color: green !important; /* Keep green when clicked */
        border: 2px solid green !important;
    }
    
    div.stButton > button:focus {
        outline: none !important; /* Remove outline */
    }
    </style>
    """, unsafe_allow_html=True)

# Title in green
st.markdown('<h3 style="color:green;">Enroll User</h3>', unsafe_allow_html=True)

# Initialize the registration form object from face_rec
registration_form = face_rec.RegistrationForm()

# Step 1: Collect person name and unit
person_name = st.text_input(label='Official Name', placeholder='e.g. MY Nawawi')
role = st.selectbox(
    label='Select Unit', 
    placeholder='Choose Unit',
    options=(
        'Choose Unit',
        'Software',
        'Geospatial',
        'Risk Management',
        'NII',
        'Business Process',
        'Networking',
        'Cyber Security',
        'Server and Cloud',
        'Data Harmonization',
        'Project Management'
    )
)

# Step 2: Collect facial embedding via webcam
def video_callback_func(frame):
    img = frame.to_ndarray(format="bgr24")  # Convert frame to BGR format
    reg_img, embedding = registration_form.get_embedding(img)
    
    # Save embedding if available
    if embedding is not None:
        with open('face_embedding.txt', mode='ab') as f:
            np.savetxt(f, embedding)
    
    return av.VideoFrame.from_ndarray(reg_img, format='bgr24')

# Stream video from webcam
webrtc_streamer(
    key='registration',
    video_frame_callback=video_callback_func,
    rtc_configuration={
        "iceServers": [
             { "urls": "stun:stun.l.google.com:19302" }
               # STUN server
          
        ]
    }
)

# Step 3: Save data to database
if st.button('Submit'):
    if person_name == '':
        st.error('Please enter your name: Name cannot be empty')
    else:
        # Save data using registration form's save function
        return_val = registration_form.save_data_in_databes_db(person_name, role)
        
        # Handle success and errors
        if return_val == True:
            st.success(f"{person_name} registered successfully!")
        elif return_val == 'file_false':
            st.error('Please upload your face image')

# Hide Streamlit's default main menu
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
