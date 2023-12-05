from django.shortcuts import render
import os
from google.cloud import speech
from google.cloud import texttospeech
import numpy as np
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.cloud import dialogflow
import base64


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
            audio_data = record_audio(duration=5)
            transcription = transcribe_audio(audio_data)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'static/secretkey/shopper.json'
            session_client = dialogflow.SessionsClient()
            text = transcription
            language_code = "en-IN"
            session_id = "abcdefg123456"
            project_id = "shopper-chatbot-for-dc-vbey"
            session = session_client.session_path(project_id, session_id)
            text_input = dialogflow.TextInput(text=text, language_code=language_code)
            query_input = dialogflow.QueryInput(text=text_input)
            response = session_client.detect_intent(
                request={"session": session, "query_input": query_input}
            )
            bot_reply = format(response.query_result.fulfillment_text)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "static/secretkey/text_to_speech.json"
            client = texttospeech.TextToSpeechClient()
            text_output = bot_reply
            synthesis_input = texttospeech.SynthesisInput(text=text_output)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-IN",
                name="en-IN-Wavenet-D",
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16
            )
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            audio_content = response.audio_content
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            return JsonResponse({'status': 'success', 'transcription': transcription,'bot_reply': bot_reply,'audio_base64': audio_base64})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def record_audio(duration=5, sample_rate=16000):
    # audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    # sd.wait()
    # return audio_data.flatten()
    p = pyaudio.PyAudio()

    # Set up the audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=int(duration * sample_rate))

    print("Recording...")

    # Read audio data from the stream
    audio_data = stream.read(int(duration * sample_rate))

    print("Finished recording.")

    # Convert binary data to NumPy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Close the audio stream and PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

    return audio_array


def transcribe_audio(audio_data, language_code="en-IN"):
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




