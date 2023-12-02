# app.py
from flask import Flask, render_template, request, jsonify, Blueprint
import speech_recognition as sr 
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# import pickle
mp4_blueprint = Blueprint("mp4_blueprint", __name__, template_folder="templates", static_url_path='/static')

# app = Flask(__name__)

# num_seconds_video = 52 * 60
# print("The video is {} seconds".format(num_seconds_video))
# l = list(range(0, num_seconds_video + 1, 60))

# diz = {}
# for i in range(len(l) - 1):
#     try:
#         ffmpeg_extract_subclip("M.S.Dhoni.mp4", l[i] - 2 * (l[i] != 0), l[i + 1], targetname="chunks/cut{}.mp4".format(i + 1))
#         clip = mp.VideoFileClip(r"chunks/cut{}.mp4".format(i + 1)) 
#         clip.audio.write_audiofile(r"converted/converted{}.wav".format(i + 1))
#         r = sr.Recognizer()
#         audio = sr.AudioFile("converted/converted{}.wav".format(i + 1))
#         with audio as source:
#             r.adjust_for_ambient_noise(source)  
#             audio_file = r.record(source)
#         result = r.recognize_google(audio_file)
#         diz['chunk{}'.format(i + 1)] = result

#     except Exception as e:
#         print(f"Error processing chunk {i + 1}: {str(e)}")

# # Optionally, save the recognized text to a text file
# l_chunks = [diz['chunk{}'.format(i + 1)] for i in range(len(diz))]
# text = '\n'.join(l_chunks)

# with open('recognized.txt', mode='w') as file:
#     file.write("Recognized Speech:")
#     file.write("\n")
#     file.write(text)
#     print("Finally ready!")    





# # Load the recognized text from the pickle file
# pickle_file_path = "video_to_text_mp4.pkl"
# with open(pickle_file_path, 'wb') as pickle_file:
#     pickle.dump(diz, pickle_file)

# @mp4_blueprint.route('/videototextmp4')
# def home():
#     return render_template('index.html')

# @mp4_blueprint.route('/predict_keywords', methods=['POST'])
# def predict_keywords():
#     try:
#         data = request.get_json()
#         chunk_number = data.get('chunk_number', "")
        
#         if not chunk_number:
#             return jsonify({"error": "Invalid request. 'chunk_number' parameter is missing."}), 400

#         # Get recognized text for the specified chunk
#         recognized_text = diz.get(f"chunk{chunk_number}", "")

#         # Return the recognized text
#         return jsonify({"recognized_text": recognized_text})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)




def process_video_and_extract_keywords():
    # ... (rest of your code for processing the video and extracting keywords)

    # Replace the pickle loading with the actual code to extract keywords
    recognized_text_dict = {}  # Replace this with your actual logic to get recognized_text_dict

    return recognized_text_dict

# Uncomment the line below and run this script once to generate the recognized text dictionary
recognized_text_dict = process_video_and_extract_keywords()

@mp4_blueprint.route("/videototexturl")
def index():
    return render_template("index.html")

@mp4_blueprint.route("/predict_keywords", methods=["POST"])
def predict_keywords():
    try:
        data = request.get_json()
        chunk_number = data.get("chunk_number", "")
        
        if not chunk_number:
            return jsonify({"error": "Invalid request. 'chunk_number' parameter is missing."}), 400

        # Get recognized text for the specified chunk
        recognized_text = recognized_text_dict.get(f"chunk{chunk_number}", "")

        # Return the recognized text
        return jsonify({"recognized_text": recognized_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# if __name__ == "__main__":
#     mp4_blueprint.run(debug=True)