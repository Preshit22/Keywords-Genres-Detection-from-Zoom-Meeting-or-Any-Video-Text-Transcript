import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pytube import YouTube
import pickle

# Replace this with the video link or file path you want to process
video_source = "https://www.youtube.com/watch?v=_LMiUOYDxzE"

# Function to download or process the video based on the source
def process_video(video_source):
    if video_source.startswith("http"):
        # Download the video using pytube
        yt = YouTube(video_source)
        downloaded_stream = yt.streams.get_highest_resolution()
        output_filename = "downloaded_video"  # No extension needed
        downloaded_stream.download(output_path=".", filename=output_filename)
        return output_filename
    elif os.path.exists(video_source):
        # Use a local video file
        return video_source
    else:
        raise ValueError("Invalid video source.")

# Get the video file to process
video_file = process_video(video_source)

# Process the downloaded video
num_seconds_video = 52 * 60
print("The video is {} seconds".format(num_seconds_video))
l = list(range(0, num_seconds_video + 1, 60))

diz = {}
for i in range(len(l) - 1):
    try:
        output_filename = "chunks/cut{}.mp4".format(i + 1)
        clip = VideoFileClip(video_file).subclip(l[i] - 2 * (l[i] != 0), l[i + 1])
        clip.write_videofile(output_filename)
        
        audio_filename = "converted/converted{}.wav".format(i + 1)
        clip.audio.write_audiofile(audio_filename)
        
        r = sr.Recognizer()
        audio = sr.AudioFile(audio_filename)
        with audio as source:
            r.adjust_for_ambient_noise(source)
            audio_file = r.record(source)
        result = r.recognize_google(audio_file)
        diz['chunk{}'.format(i + 1)] = result
    except Exception as e:
        print(f"Error processing chunk{i + 1}: {str(e)}")

# Save the dictionary to a pickle file
pickle_file_path = "video_to_textexe4.pkl"
with open(pickle_file_path, 'wb') as pickle_file:
    pickle.dump(diz, pickle_file)

# Optionally, save the recognized text to a text file
text = '\n'.join([diz['chunk{}'.format(i + 1)] for i in range(len(diz))])
with open('recognized.txt', mode='w') as file:
    file.write("Recognized Speech:")
    file.write("\n")
    file.write(text)
    print("Finally ready!")
