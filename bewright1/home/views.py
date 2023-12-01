from django.shortcuts import render
import os
import json
from django.http import HttpResponse
# from .chatbot_logic import get_bot_response
from django.http import JsonResponse
from google.cloud import speech
from google.cloud import texttospeech
import io
import sounddevice as sd
from google.cloud import speech_v1p1beta1 as speech
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.cloud import dialogflow


# Create your views here.
def index(request):
    return render(request,'index.html')

def vegetables(request):
    return render(request, 'vegetables.html')

def about(request):
    return render(request, 'about.html')

def shop(request):
    return render(request, 'shop.html')

def contact(request):
    return render(request, 'contact.html')

def chatbot(request):
    return render(request, 'chatbot.html')

@csrf_exempt
def transcribe_microphone(request):
    if request.method == 'POST':
        try:
            # Record audio from the microphone for 5 seconds
            audio_data = record_audio(duration=5)

            # Transcribe the recorded audio to text
            transcription = transcribe_audio(audio_data)
            print(f"Transcription: {transcription}")

            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'static/secretkey/shopper.json'
            session_client = dialogflow.SessionsClient()
            text = transcription
            print(text)
            language_code = "en-US"
            session_id = "abcdefg123456"
            project_id = "shopper-chatbot-for-dc-vbey"
            session = session_client.session_path(project_id, session_id)

            text_input = dialogflow.TextInput(text=text, language_code=language_code)

            query_input = dialogflow.QueryInput(text=text_input)

            response = session_client.detect_intent(
                request={"session": session, "query_input": query_input}
            )

            bot_reply = format(response.query_result.fulfillment_text)
            print(bot_reply)

            return JsonResponse({'status': 'success', 'transcription': transcription,'bot_reply':bot_reply})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def record_audio(duration=5, sample_rate=16000):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return audio_data.flatten()

def transcribe_audio(audio_data, language_code="en-US"):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'static/secretkey/key.json'
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_data.tobytes())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)
    transcriptions = [result.alternatives[0].transcript for result in response.results]
    return ' '.join(transcriptions)




