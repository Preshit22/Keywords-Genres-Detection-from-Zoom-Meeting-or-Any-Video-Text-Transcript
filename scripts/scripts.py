import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import speech_recognition as sr 
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube
import requests

def download_video(video_link: str) -> str:
    """Download a YouTube video and return its file path."""
    yt = YouTube(video_link)
    yt_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    downloaded_filename = yt_stream.default_filename
    output_directory = "data/input/"
    yt_stream.download(output_path=output_directory, filename=downloaded_filename)
    file_path = output_directory + downloaded_filename
    return file_path

def video_to_text(file_path: str, num_seconds_video: int) -> str:
    l = list(range(0, num_seconds_video + 1, 60))
    diz = {}
    for i in range(len(l) - 1):
        ffmpeg_extract_subclip(file_path, max(0, l[i] - 2 * (l[i] != 0)), l[i + 1], targetname="data/segments_video/cut{}.mp4".format(i + 1))
        clip = mp.VideoFileClip(r"data/segments_video/cut{}.mp4".format(i + 1)) 
        clip.audio.write_audiofile(r"data/segments_audio/converted{}.wav".format(i + 1))
        r = sr.Recognizer()
        with sr.AudioFile("data/segments_audio/converted{}.wav".format(i + 1)) as source:
            audio_file = r.record(source)
        diz['chunk{}'.format(i + 1)] = r.recognize_google(audio_file)
    text = '\n'.join([diz['chunk{}'.format(i + 1)] for i in range(len(diz))])
    with open('data/transcriptions/recognized.txt', mode='w') as file:
        file.write("RecognizedSpeech:\n")
        file.write(text)
    return "Video processing completed. The transcriptions have been saved to 'data/transcriptions/recognized.txt'."

def keywords():
    def process(txt):
        txt = txt.lower() 
        txt = re.sub(r"<.*?>", " ", txt)  
        txt = re.sub(r"[^a-zA-Z]", " ", txt)  
        txt = nltk.word_tokenize(txt)  
        txt = [word for word in txt if word not in stopwords.words('english')]  
        txt = [word for word in txt if len(word) >= 3]  
        return " ".join(txt)

    with open('data/transcriptions/recognized.txt', 'r', encoding='utf-8') as file:
        texts = [process(file.read())]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
    tfidf_threshold = 0.2
    relevant_keywords = tfidf_df.columns[tfidf_df.max() > tfidf_threshold]

    with open('data/transcriptions/keywords.txt', 'w') as file:
        for keyword in relevant_keywords:
            file.write(keyword + '\n')

def identify_genre():
    API_KEY = "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"
    url = "https://api.openai.com/v1/engines/davinci/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # Read keywords from a fixed file path
    with open('data/transcriptions/keywords.txt', 'r', encoding='utf-8') as file:
        keywords = [line.strip() for line in file if line.strip()]
    
    data = {"prompt": f"{', '.join(keywords)} categorize the genre for above keywords. give in one word genre:?", "max_tokens": 100}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    choices = response.json().get("choices", [])
    if choices:
        genre = choices[0]["text"].split()[0].strip()
        return genre
    else:
        return "Genre prediction not available."
