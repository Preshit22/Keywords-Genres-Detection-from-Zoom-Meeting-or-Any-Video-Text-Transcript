import streamlit as st
from scripts.scripts import *
import os


st.set_page_config(layout="wide")
with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('''
<style>
.stApp [data-testid="stToolbar"]{
    display:none;
}
</style>
''', unsafe_allow_html=True)


st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<style>
.navbar {
  position: fixed;
  top: 50px; /* Adjust the top value to change the position */
  background-color: ##0a0a0a;
  padding: 0 20px;
}

.navbar-brand {
  color: white;
  font-size: 18px;
  padding: 0 10px;
}

.navbar-toggler {
  border: none;
  background-color: transparent;
}

.navbar-toggler .navbar-toggler-icon {
  color: white;
  font-size: 24px;
}

.navbar-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-link {
  color: white;
  padding: 10px 15px;
}
</style>
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #A8A8A8;">
  <a class="navbar-brand" href="http://localhost:8501/#video-processing-app" target="_blank">Vid Contextualizer</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#home">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#transcript" target="_blank">transcript</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#about" target="_blank">about us</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

st.markdown("""
<style>
h2 {
  display: none;
}
</style>
""", unsafe_allow_html=True)

st.header('This is a hidden title')    
st.markdown('##')
st.title('Video Contextualizer', anchor='home')
st.divider()
st.markdown('##')
st.subheader("This app downloads a YouTube video, transcribes it, extracts keywords, and predicts the genre.")
st.markdown('##')
col1, col2, col3 , col4, col5 = st.columns(5)

with col1:
    pass
with col2:
    pass
with col4:
    pass
with col5:
    pass
with col3 :
    center_button = st.button('Transcript and Contextualize the Video')
st.markdown('#')
st.markdown('###')
st.markdown('###')

def main():
    st.header('header')
    st.header('header')
    st.header('header')
    st.title('Transcript and Contextualize the Video', anchor='transcript')
    st.divider()
    video_link = st.empty()
    option = st.selectbox("Choose an option", ("Upload", "URL"))
    if option == "Upload":
        video_link.empty()
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            file_path = os.path.join('data/input/', uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            num_minutes_video = st.number_input("Enter the number of minutes in the video", min_value=1)
            num_seconds_video = num_minutes_video * 60 
            if st.button("Video to Text"):
                message = video_to_text(file_path, num_seconds_video)
                st.write(message)
                words = keywords()
                genre = identify_genre()
                st.write("Keywords and predicted genre are generated.")
                st.write("keywords: ", words)
                st.write("predicted genre: ", genre)
    else :
        video_link = st.text_input("Enter the YouTube video link")
        num_minutes_video = st.number_input("Enter the number of minutes in the video", min_value=1)
        num_seconds_video = num_minutes_video * 60 
        if st.button("Video to Text"):
            file_path = download_video(video_link)
            message = video_to_text(file_path, num_seconds_video)
            st.write(message)
            keywords()
            genre = identify_genre()
            st.write("Keywords and predicted genre are generated.")

    st.header('This is a hidden title')    
    st.markdown('##')
    st.markdown('##')
    st.markdown('##')
    st.title('about', anchor='about')
    st.divider()
    st.markdown('##')
    st.subheader("Om Patange.")
    st.subheader("Preshit Desai.")
    st.markdown('##')
    col1, col2, col3 , col4, col5 = st.columns(5)

if __name__ == "__main__":
    main()

