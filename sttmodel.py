import whisper
from deep_translator import GoogleTranslator
import os

class SpeechTranslator:
    def __init__(self):
        print("Loading Whisper model...")
        self.model = whisper.load_model("tiny")
        print("Model loaded successfully!")

    def process_audio(self, audio_path):
        try:
            # Check if file exists
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            # Step 1: Transcribe with Whisper
            print(f"Transcribing: {audio_path}")
            result = self.model.transcribe(audio_path)
            transcription = result["text"]
            detected_language = result["language"]
            print(f"Transcription completed in {detected_language}")

            # Step 2: Translate to English if not already in English
            translator = GoogleTranslator(source=detected_language, target='en')
            english_text = translator.translate(text=transcription)
            print("Translation completed")

            return {
                "success": True,
                "transcription": transcription,
                "translation": english_text,
                "detected_language": detected_language
            }

        except Exception as e:
            print(f"Error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
