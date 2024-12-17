import os
import zipfile
import tarfile
import py7zr
import streamlit as st
from pathlib import Path
import socket
from smtp_email_connect_v2 import send_email

# Function to extract zip, tar, and 7zip files
def extract_zip(zip_path, extract_to):
    if zipfile.is_zipfile(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif tarfile.is_tarfile(zip_path):
        with tarfile.open(zip_path, 'r') as tar_ref:
            tar_ref.extractall(extract_to)
    elif zip_path.endswith(".7z"):
        with py7zr.SevenZipFile(zip_path, mode='r') as archive:
            archive.extractall(path=extract_to)
    else:
        st.error(f"Unsupported file type: {zip_path}")
        return False
    return True

# Function to browse folders and videos
def browse_directory(directory_path):
    # Get list of all files and directories
    files_and_dirs = os.listdir(directory_path)
    dirs = [d for d in files_and_dirs if os.path.isdir(os.path.join(directory_path, d))]
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(directory_path, f))]

    # Display directories and allow navigation
    selected_dir = st.selectbox("Select a folder", ['None'] + dirs)
    
    if selected_dir != 'None':
        new_path = os.path.join(directory_path, selected_dir)
        browse_directory(new_path)
    
    # Display files, allow selecting video
    video_files = [f for f in files if f.lower().endswith(('mp4', 'mkv', 'avi', 'mov', 'webm','ts'))]
    if video_files:
        selected_video = st.selectbox("Select a video", video_files)
        if selected_video:
            video_path = os.path.join(directory_path, selected_video)
            st.video(video_path)
        
    # Check for zip files and offer extraction
    zip_files = [f for f in files if f.lower().endswith(('zip', 'tar', '7z'))]
    for zip_file in zip_files:
        zip_path = os.path.join(directory_path, zip_file)
        if st.button(f"Extract {zip_file}"):
            extract_to = os.path.join(directory_path, zip_file.split('.')[0])
            os.makedirs(extract_to, exist_ok=True)
            if extract_zip(zip_path, extract_to):
                st.success(f"Extracted {zip_file} successfully!")
                browse_directory(extract_to)
def get_local_ip():
    # Get the local machine name
    hostname = socket.gethostname()
    # Get the local IP address using the hostname
    local_ip = socket.gethostbyname(hostname)
    return local_ip


# Main Streamlit UI
def main():
    st.title("Course Video Browser")
    st.write(f"get_local_ip {get_local_ip()}")
    send_email(
        subject="Streamlit app Started Running",
        body=f"App is started Running at port :: {get_local_ip()} /n Enjoy Your Day",
        to_email="asdasda@gmail.com"
    )
    # Allow user to select directory
    uploaded_dir = st.text_input("Enter directory path", "/path/to/your/courses")

    if uploaded_dir:
        uploaded_dir = Path(uploaded_dir).expanduser()
        if uploaded_dir.exists() and uploaded_dir.is_dir():
            browse_directory(uploaded_dir)
        else:
            st.error(f"The directory {uploaded_dir} does not exist.")
    else:
        st.error("Please enter a valid directory path.")




# Run the Streamlit app
if __name__ == "__main__":
    main()
