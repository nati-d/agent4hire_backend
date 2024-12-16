import google.auth
from googleapiclient.discovery import build
from google.cloud import speech, texttospeech


def get_google_search_service():
    credentials, project = google.auth.default()
    return build('searchconsole', 'v1', credentials=credentials)

def get_stt_client():
    return speech.SpeechClient()

def load_audio_file(file_path):
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()
    return content

def get_tts_client():
    return texttospeech.TextToSpeechClient()

def create_audio_config(audio_format='MP3'):
    format_mapping = {
        'MP3': texttospeech.AudioEncoding.MP3,
        'LINEAR16': texttospeech.AudioEncoding.LINEAR16
    }
    return texttospeech.AudioConfig(
        audio_encoding=format_mapping.get(audio_format, texttospeech.AudioEncoding.MP3)
    )