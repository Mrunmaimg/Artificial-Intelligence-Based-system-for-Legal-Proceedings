from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from sttmodel import SpeechTranslator

# Initialize Flask app with explicit template folder
app = Flask(__name__, 
            template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')))
CORS(app)

# Initialize the translator
translator = SpeechTranslator()

# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400

        # Save the uploaded file
        audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
        audio_file.save(audio_path)

        try:
            # Process the audio
            result = translator.process_audio(audio_path)
            return jsonify(result)
        finally:
            # Clean up the uploaded file
            if os.path.exists(audio_path):
                os.remove(audio_path)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 