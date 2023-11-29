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

# Configure the speech recognition client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'static/secretkey/key.json'

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

@csrf_exempt
def transcribe_microphone(request):
    if request.method == 'POST':
        try:
            # Record audio from the microphone for 5 seconds
            audio_data = record_audio(duration=5)

            # Transcribe the recorded audio to text
            transcription = transcribe_audio(audio_data)

            return JsonResponse({'status': 'success', 'transcription': transcription})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def record_audio(duration=5, sample_rate=16000):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return audio_data.flatten()

def transcribe_audio(audio_data, language_code="en-US"):
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

# def get_bot_response(user_input):
#     # Simple rule-based responses
#     if "hello" in user_input.lower():
#         return "Hi there!"
#     elif "how are you" in user_input.lower():
#         return "I'm just a computer program, but thanks for asking!"
#     elif "bye" in user_input.lower():
#         return "Goodbye! Have a great day."
#     else:
#         return "I'm sorry, I didn't understand that."

def chatbot(request):
    return render(request, 'chatbot.html')

# def get_bot_response_view(request):
#     print("hello get_bot_response_view")
#     transcript = request.POST.get('transcript', '')
#     # user_input = user_audio()
#     if transcript.strip():  # Check if the transcript is not empty after stripping whitespace
#         bot_response = get_bot_response(transcript)
#         return JsonResponse({'bot_response': bot_response})
#     else:
#         return JsonResponse({'bot_response': 'No valid transcript provided'})
