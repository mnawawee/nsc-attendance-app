from navigation import make_sidebar
import streamlit as st
from Home import face_rec
import pandas as pd
make_sidebar()
# Configure the Streamlit app
# st.set_page_config(page_title='Reporting', layout='wide')
st.markdown('<h3 style="color:green;">Generate Report</h3>', unsafe_allow_html=True)
# st.subheader('Reporting')

# Function to load logs from Redis
name = 'attendance:logs'
def load_logs(name, end=-1):
    logs_list = face_rec.r.lrange(name, start=0, end=end)  # Extract all data from Redis database
    return logs_list

# Tabs to show the information
tab1, tab2, tab3 = st.tabs(['Registered Data', 'Logs', 'Attendance Report'])

with tab1:
    if st.button('Refresh Data'):
        # Retrieve the data from Redis Database
        with st.spinner('Retrieving Data from Redis Db...'):
            redis_face_db = face_rec.retrive_data(name='academy:register')
            st.dataframe(redis_face_db[['Name', 'Role']])

with tab2:
    if st.button('Refresh Logs'):
        st.write(load_logs(name=name))

with tab3:
    st.markdown('<h3 style="color:green;">Attendance Report</h3>', unsafe_allow_html=True)
    # st.subheader('')

    # Step 1: Convert logs data from list of bytes into list of strings
    logs_list = load_logs(name=name)

    # Convert bytes to strings
    convert_byte_to_string = lambda x: x.decode('utf-8')
    logs_list_string = list(map(convert_byte_to_string, logs_list))
    # Split the strings into a nested list
    split_string = lambda x: x.split('@')
    logs_nested_list = list(map(split_string, logs_list_string))

    # Step 2: Create a DataFrame from the nested list
    logs_df = pd.DataFrame(logs_nested_list, columns=['Name', 'Role', 'Timestamp'])

    # Convert the 'Timestamp' column to datetime
    logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])

    # Extract the date from the 'Timestamp' column
    logs_df['Date'] = logs_df['Timestamp'].dt.date

    # Step 3: Calculate in-time and out-time
    report_df = logs_df.groupby(by=['Date', 'Name', 'Role']).agg(
        in_time=pd.NamedAgg('Timestamp', 'min'),  # In time
        out_time=pd.NamedAgg('Timestamp', 'max')  # Out time
    ).reset_index()

    # Convert in_time and out_time to datetime
    report_df['in_time'] = pd.to_datetime(report_df['in_time'])
    report_df['out_time'] = pd.to_datetime(report_df['out_time'])

    # Calculate duration
    report_df['Duration'] = report_df['out_time'] - report_df['in_time']

    # Step 4: Mark present or absent
    all_dates = report_df['Date'].unique()
    name_role = report_df[['Name', 'Role']].drop_duplicates().values.tolist()

    date_name_role_zip = []
    for dt in all_dates:
        for name, role in name_role:
            date_name_role_zip.append([dt, name, role])

    date_name_role_zip_df = pd.DataFrame(date_name_role_zip, columns=['Date', 'Name', 'Role'])

    # Merge with report_df to ensure all combinations are present
    date_name_role_zip_df = pd.merge(date_name_role_zip_df, report_df, how='left', on=['Date', 'Name', 'Role'])

    # Calculate duration in hours
    date_name_role_zip_df['Duration_seconds'] = date_name_role_zip_df['Duration'].dt.seconds
    date_name_role_zip_df['Duration_hours'] = date_name_role_zip_df['Duration_seconds'] / (60 * 60)

    # Status marker function
    def status_marker(x):
        if pd.Series(x).isnull().all():
            return 'Absent'
        elif x >= 0 and x < 1:
            return 'Absent (Less than 1 hr)'
        elif x >= 1 and x < 4:
            return 'Half day (Less than 4 hrs)'
        elif x >= 4 and x < 6:
            return 'Half day'
        elif x >= 6:
            return 'Present'

    date_name_role_zip_df['Status'] = date_name_role_zip_df['Duration_hours'].apply(status_marker)

    # Display the final DataFrame
    st.dataframe(date_name_role_zip_df)

hide_streamlit_style= """
<style>
#MainMenu {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style,unsafe_allow_html=True)