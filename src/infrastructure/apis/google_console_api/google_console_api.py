from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.cloud import speech, texttospeech
from google.cloud.speech import RecognitionAudio, RecognitionConfig
from pydub import AudioSegment
from io import BytesIO
import os

class GoogleServicesClient:
    def __init__(self, ):
        credentials_json = os.path.join(os.getcwd(), 'parabolic-hook-419323-8c0a1d220cb6.json')
        
        self.credentials = service_account.Credentials.from_service_account_file(credentials_json)

        self.search_service = build('webmasters', 'v3', credentials=self.credentials)

        
        self.stt_client = speech.SpeechClient(credentials=self.credentials)

        
        self.tts_client = texttospeech.TextToSpeechClient(credentials=self.credentials)

    def get_site_info(self, site_url):
        """Fetches site information from Google Search Console."""
        try:
            response = self.search_service.sites().get(siteUrl=site_url).execute()
            return response
        except Exception as e:
            print(f"Error fetching site info: {e}")
            return None

    def get_search_analytics(self, site_url, start_date, end_date, dimensions=['query']):
        """Retrieves search analytics data for a site."""
        try:
            request = {
                'startDate': start_date,
                'endDate': end_date,
                'dimensions': dimensions
            }
            response = self.search_service.searchanalytics().query(siteUrl=site_url, body=request).execute()
            return response
        except Exception as e:
            print(f"Error fetching search analytics: {e}")
            return None

    def list_sitemaps(self, site_url):
        """Lists all sitemaps for a site."""
        try:
            response = self.search_service.sitemaps().list(siteUrl=site_url).execute()
            return response.get('sitemap', [])
        except Exception as e:
            print(f"Error listing sitemaps: {e}")
            return None

    def submit_sitemap(self, site_url, sitemap_url):
        """Submits a sitemap to Google Search Console."""
        try:
            response = self.search_service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
            return response
        except Exception as e:
            print(f"Error submitting sitemap: {e}")
            return None

    def inspect_url(self, site_url, url):
        """Inspects a URL using the URL Inspection API."""
        try:
            response = self.search_service.urlInspection().index().inspect(
                siteUrl=site_url, inspectionUrl=url
            ).execute()
            return response
        except Exception as e:
            print(f"Error inspecting URL: {e}")
            return None

    def list_crawl_errors(self, site_url):
        """Lists crawl errors for a site."""
        try:
            response = self.search_service.urlcrawlerrorssamples().list(siteUrl=site_url).execute()
            return response.get('urlCrawlErrorSample', [])
        except Exception as e:
            print(f"Error listing crawl errors: {e}")
            return None

    def get_mobile_usability(self, site_url):
        """Fetches mobile usability data for a site."""
        try:
            response = self.search_service.mobileUsability().query(siteUrl=site_url).execute()
            return response
        except Exception as e:
            print(f"Error fetching mobile usability data: {e}")
            return None

    def transcribe_audio(self, file, language_code="en-US"):
        """Transcribes audio from a file using Google Speech-to-Text."""
        try:
            audio_data = file.read()
            audio = AudioSegment.from_file(BytesIO(audio_data), format="wav")
            audio = audio.set_channels(1)

            mono_audio_io = BytesIO()
            audio.export(mono_audio_io, format="wav")
            mono_audio_io.seek(0)
            audio_content = mono_audio_io.read()

            recognition_audio = RecognitionAudio(content=audio_content)
            config = RecognitionConfig(
                encoding=RecognitionConfig.AudioEncoding.LINEAR16,
                language_code=language_code,
            )
            response = self.stt_client.recognize(config=config, audio=recognition_audio)
            return [result.alternatives[0].transcript for result in response.results]
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None

    def transcribe_streaming(self, audio_stream, language_code="en-US"):
        """Performs streaming transcription of audio data."""
        config = RecognitionConfig(
            encoding=RecognitionConfig.AudioEncoding.LINEAR16,
            language_code=language_code,
        )
        streaming_config = speech.StreamingRecognitionConfig(config=config)
        requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_stream)
        try:
            responses = self.stt_client.streaming_recognize(streaming_config, requests)
            return [result.alternatives[0].transcript for response in responses for result in response.results]
        except Exception as e:
            print(f"Error in streaming transcription: {e}")
            return None

    def synthesize_text(self, text, language_code="en-US", voice_type="NEUTRAL", audio_format="MP3"):
        """Synthesizes speech from text using Google Text-to-Speech."""
        synthesis_input = texttospeech.SynthesisInput(text=text)
        ssml_gender = getattr(
            texttospeech.SsmlVoiceGender,
            voice_type.upper(),
            texttospeech.SsmlVoiceGender.NEUTRAL
        )
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=ssml_gender
        )
        audio_encoding = getattr(
            texttospeech.AudioEncoding,
            audio_format.upper(),
            texttospeech.AudioEncoding.MP3
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=audio_encoding)
        try:
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            return response.audio_content
        except Exception as e:
            print(f"Error synthesizing text: {e}")
            return None
