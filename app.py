import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Load dataset
def load_data():
    file_path = "file_backup_data.csv"  # Ensure this file is available in the working directory
    return pd.read_csv(file_path)

data = load_data()

# Backup function
def backup_files(data, backup_folder="backup_folder"):
    os.makedirs(backup_folder, exist_ok=True)
    not_backed_up = data[data['backup_status'] == 'Not-Backed-Up']
    not_backed_up['backup_status'] = 'Backed-Up'
    not_backed_up['backup_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data.update(not_backed_up)
    return not_backed_up

# Streamlit App
st.title("Automated Data Backup & Monitoring Dashboard")

# Show dataset overview
st.header("Dataset Overview")
st.write("This dataset contains file backup statuses across different servers.")
st.dataframe(data)

# Check distribution of files per server
st.header("File Distribution by Server")
server_distribution = data['server_location'].value_counts()
st.bar_chart(server_distribution)

# Show not backed-up files
st.header("Files Not Yet Backed Up")
not_backed_up_files = data[data['backup_status'] == 'Not-Backed-Up']
st.dataframe(not_backed_up_files)

# Backup operation
st.header("Perform Backup")
if st.button("Start Backup"):
    backup_folder = "backup_folder"
    backed_up_files = backup_files(data, backup_folder=backup_folder)

    # Save updated dataset
    updated_file_path = "updated_backup_data.csv"
    data.to_csv(updated_file_path, index=False)

    # Save backup report
    backup_report_path = "backup_report.csv"
    backed_up_files.to_csv(backup_report_path, index=False)

    st.success(f"Backup completed! {len(backed_up_files)} files have been backed up.")

    # Provide download links
    st.download_button(
        label="Download Backup Report",
        data=backed_up_files.to_csv(index=False).encode('utf-8'),
        file_name="backup_report.csv",
        mime="text/csv"
    )

    st.download_button(
        label="Download Updated Dataset",
        data=data.to_csv(index=False).encode('utf-8'),
        file_name="updated_backup_data.csv",
        mime="text/csv"
    )

# Summary stats
st.header("Summary Statistics")
num_files = len(data)
num_backed_up = len(data[data['backup_status'] == 'Backed-Up'])
num_not_backed_up = len(data[data['backup_status'] == 'Not-Backed-Up'])
st.write(f"**Total Files:** {num_files}")
st.write(f"**Files Backed Up:** {num_backed_up}")
st.write(f"**Files Not Backed Up:** {num_not_backed_up}")

# Monitor recent activity
st.header("Recent Activity")
recent_activity = data.sort_values(by='last_modified', ascending=False).head(10)
st.dataframe(recent_activity)
