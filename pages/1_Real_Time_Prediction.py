from navigation import make_sidebar
import streamlit as st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time
make_sidebar()
# st.set_page_config(page_title='Prediction')
st.markdown('<h3 style="color:green;">Mark Attendance</h3>', unsafe_allow_html=True)




# Retrive the data from Redis Database
with st.spinner('Retriving Data from Db..'):
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)

st.success('Data sucessfully retrived from database')

# time
waitTime = 3# time in sec
setTime = time.time() 
realtimepred = face_rec.RealTimePred()# real time prediction class

# Real Time Prediction
#streamlit webrtc

#callback function
def video_frame_callback(frame):
    global setTime
    img = frame.to_ndarray(format="bgr24")# is 3 dimentsion numpy array
    #operation that you can perform on the array
    pred_img =realtimepred.face_prediction(img,redis_face_db,
                                        'facial_feature',['Name','Role'],thresh=0.5)
    
    timenow = time.time()
    difftime =timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time() #reset time
        print('Save data to database')
    
    return av.VideoFrame.from_ndarray(pred_img, format="bgr24") 


webrtc_streamer(key="RealTimePrediction", video_frame_callback=video_frame_callback,
rtc_configuration={"iceServers": [{"urls": ["stun:stun.xten.com:3478"]}]},            
)

hide_streamlit_style= """
<style>
#MainMenu {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style,unsafe_allow_html=True)