from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import moviepy.editor as mp
import pytesseract  # You may need to install pytesseract with "pip install pytesseract"

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'VTT'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_video_to_text(video_path, recognized_text_path):
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(recognized_text_path.replace('.txt', '.wav'))

        # Convert the video audio to text using pytesseract (OCR)
        audio_text = pytesseract.image_to_string(recognized_text_path.replace('.txt', '.wav'))

        # Save the recognized text to a file
        with open(recognized_text_path, 'w', encoding='utf-8') as text_file:
            text_file.write(audio_text)
        
        # Clean up intermediate audio file
        os.remove(recognized_text_path.replace('.txt', '.wav'))

    except Exception as e:
        print(f"Error converting video to text: {e}")

@app.route('/upload')
def index():
    return render_template('templatess/upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        recognized_text_path = os.path.join(app.config['UPLOAD_FOLDER'], 'recognized.txt')

        convert_video_to_text(video_path, recognized_text_path)

        # After processing, you can extract keywords from the recognized text
        keywords = extract_keywords(recognized_text_path)
        return render_template('result.html', keywords=keywords)

    return render_template('error.html', error="Invalid file format")

if __name__ == '__main__':
    app.run(debug=True)
