import streamlit as st
from streamlit_analytics import st_analytics
from scripts.scripts import *
import os

def main():
    st.title("Keywords & Genre Detection using Zoom Meeting or Any Video")
    st.write("This app downloads a YouTube video, transcribes it, extracts keywords, and predicts the genre.")

    option = st.selectbox("Choose an option", ("URL", "Upload"))
    if option == "URL":
        video_link = st.text_input("Enter the YouTube video link")
        num_seconds_video = st.number_input("Enter the number of seconds in the video", min_value=1)
        if st.button("Video to Text"):
            file_path = download_video(video_link)
            message = video_to_text(file_path, num_seconds_video)
            st.write(message)
            keywords()
            genre = identify_genre()
            st.write("Keywords and predicted genre are generated.")
    else:
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            file_path = os.path.join('data/input/', uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            num_seconds_video = st.number_input("Enter the number of seconds in the video", min_value=1)
            if st.button("Video to Text"):
                message = video_to_text(file_path, num_seconds_video)
                st.write(message)
                words = keywords()
                genre = identify_genre()
                st.write("Keywords and predicted genre are generated.")
                st.write("keywords: ", words)
                st.write("predicted genre: ", genre)

if __name__ == "__main__":
    main()

