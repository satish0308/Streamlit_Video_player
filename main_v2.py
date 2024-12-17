import os
import zipfile
import tarfile
import py7zr
import streamlit as st
from pathlib import Path
from streamlit.components.v1 import html

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
    
    # If a directory is selected, browse it
    if selected_dir != 'None':
        new_path = os.path.join(directory_path, selected_dir)
        browse_directory(new_path)
    
    # Display files and allow selecting video
    video_files = [f for f in files if f.lower().endswith(('mp4', 'mkv', 'avi', 'mov', 'webm', 'ts'))]
    notebook_files = [f for f in files if f.lower().endswith('ipynb')]  # Jupyter notebook files

    if video_files or notebook_files:
        selected_file_type = st.radio("Choose to view a video or Jupyter notebook", ['Video', 'Notebook'], key=directory_path)

        if selected_file_type == 'Video' and video_files:
            selected_video = st.selectbox("Select a video", video_files)
            if selected_video:
                video_path = os.path.join(directory_path, selected_video)
                st.video(video_path)
        
        elif selected_file_type == 'Notebook' and notebook_files:
            selected_notebook = st.selectbox("Select a Jupyter Notebook", notebook_files)
            if selected_notebook:
                notebook_path = os.path.join(directory_path, selected_notebook)
                st.markdown(f"### {selected_notebook} - Jupyter Notebook")
                # Render notebook content (Convert to HTML)
                with open(notebook_path, "r") as file:
                    notebook_content = file.read()
                # Display notebook content in Streamlit (could be enhanced by using Jupyter rendering)
                html(notebook_content, height=800)

    # Check for zip files and offer extraction
    zip_files = [f for f in files if f.lower().endswith(('zip', 'tar', '7z'))]
    for zip_file in zip_files:
        zip_path = os.path.join(directory_path, zip_file)
        if st.button(f"Extract {zip_file}"):
            extract_to = os.path.join(directory_path, zip_file.split('.')[0])
            os.makedirs(extract_to, exist_ok=True)
            if extract_zip(zip_path, extract_to):
                st.success(f"Extracted {zip_file} successfully!")
                # Refresh the directory view after extraction
                browse_directory(extract_to)

# Main Streamlit UI
def main():
    st.title("Course Video and Notebook Browser")

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
