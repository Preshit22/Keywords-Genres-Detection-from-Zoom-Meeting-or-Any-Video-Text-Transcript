import speech_recognition as sr 
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pickle

num_seconds_video = 52 * 60
print("The video is {} seconds".format(num_seconds_video))
l = list(range(0, num_seconds_video + 1, 60))

diz = {}
for i in range(len(l) - 1):
    try:
        # ffmpeg_extract_subclip("M.S.Dhoni.mp4", l[i] - 2 * (l[i] != 0), l[i + 1], targetname="chunks/cut{}.mp4".format(i + 1))
        # ffmpeg_extract_subclip("M.S.Dhoni.mp4", max(0, l[i] - 2 * (l[i] != 0)), l[i + 1], targetname="chunks/cut{}.mp4".format(i + 1))
        start_time = max(0, l[i] - 2 * (l[i] != 0))
        ffmpeg_extract_subclip("video data/M.S.Dhoni.mp4", start_time, l[i + 1], targetname="chunks/cut{}.mp4".format(i + 1))
        
        clip = mp.VideoFileClip(r"chunks/cut{}.mp4".format(i + 1)) 
        clip.audio.write_audiofile(r"converted/converted{}.wav".format(i + 1))
        r = sr.Recognizer()
        audio = sr.AudioFile("converted/converted{}.wav".format(i + 1))
        with audio as source:
            r.adjust_for_ambient_noise(source)  
            audio_file = r.record(source)
        result = r.recognize_google(audio_file)
        diz['chunk{}'.format(i + 1)] = result

    except Exception as e:
        print(f"Error processing chunk {i + 1}: {str(e)}")

# # Save the dictionary to a pickle file
# pickle_file_path = "video_to_text_mp4.pkl"
# with open(pickle_file_path, 'wb') as pickle_file:
#     pickle.dump(diz, pickle_file)

# Optionally, save the recognized text to a text file
l_chunks = [diz['chunk{}'.format(i + 1)] for i in range(len(diz))]
text = '\n'.join(l_chunks)

with open('recognized.txt', mode='w') as file:
    file.write("Recognized Speech:")
    file.write("\n")
    file.write(text)
    print("Finally ready!")




 