import streamlit as st
import subprocess
import sys
import cv2
import test
from PIL import Image
import zipfile

st.header("3D APP")
uploaded_video = st.file_uploader("Choose video", type=["mp4", "mov"])
frame_skip = 300 # display every 300 frames

def start_capture():
    subprocess.run([f"{sys.executable}", "test.py"])


def run_cap():
    cap_button = st.button("RUN 3D GENERATION") # Give button a variable name
    if cap_button: # Make button a condition.
        start_capture()
        st.text("PROGRAM Successfully")


if uploaded_video is not None: # run only when user uploads video
    vid = uploaded_video.name
    with open(vid, mode='wb') as f:
        f.write(uploaded_video.read()) # save video to disk

    st.markdown(f"""
    ### Files
    - {vid}
    """,
    unsafe_allow_html=True) # display file name

    vidcap = cv2.VideoCapture(vid) # load video from disk
    cur_frame = 0
    success = True
    run_cap() 
    while success:
        success, frame = vidcap.read() # get next frame from video
        if cur_frame % frame_skip == 0: # only analyze every n=300 frames
            print('frame: {}'.format(cur_frame)) 
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame) # convert opencv frame (with type()==numpy) into PIL Image
            st.image(pil_img)
        cur_frame += 1
    # store my data in zip/json
    #with zipfile.ZipFile("file.zip", 'w') as zip:
    #      zip.writestr("Data.json", jsonString)
    zipfile.ZipFile('file.zip', mode='w').write("readme.txt")

    # Parse made zip file to streamlit button
    with open("file.zip", "rb") as fp:
              btn = st.download_button(
                  label="Download 3D OBJ ZIP",
                  data=fp,
                  file_name="file.zip",
                  mime="application/octet-stream"
                  )   
       
