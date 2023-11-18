from google.cloud import speech
from google.cloud import texttospeech

import os

# Connection with Google cloud
# Instantiates a clients

# Speech to text client
client = speech.SpeechClient.from_service_account_file('google-api-key.json')

# Text to speech client
# Reference: https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-api-key.json'
client2 = texttospeech.TextToSpeechClient()


# ##################################################################################
# Google speech to text part.
"""
Reference: https://cloud.google.com/speech-to-text/docs/sync-recognize#speech-sync-recognize-python
"""
def speech_to_text(input_audio):
    with open(input_audio, 'rb') as f:
        mp3_data = f.read()

    input_audio_file = speech.RecognitionAudio(content=mp3_data)
    config = speech.RecognitionConfig(
        sample_rate_hertz=24000,
        enable_automatic_punctuation=True,
        language_code='en-US'
    )
    response = client.recognize(
        config=config,
        audio=input_audio_file
    )
    json_string = speech.RecognizeResponse.to_json(response)
    print("S2T DONE with output: " + json_string)

    return json_string


# ##################################################################################

# Google text to speech part.
"""
Reference: https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python
"""
def text_to_speech(query_text):
    print("T2S START with: " + query_text)
    synthesis_input = texttospeech.SynthesisInput(text=query_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client2.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    with open(f"output_audio.mp3", "wb") as out:
        out.write(response.audio_content)

    print("T2S DONE...")
    return response.audio_content

