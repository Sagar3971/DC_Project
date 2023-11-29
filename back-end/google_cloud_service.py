from google.cloud import speech
from google.cloud import texttospeech
import json
from google.cloud import dialogflow

# Connection with Google cloud
# Instantiates a clients

# Speech to text client
# client = speech.SpeechClient.from_service_account_file('google-api-key.json')

# Text to speech client
# Reference: https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-api-key.json'
# client2 = texttospeech.TextToSpeechClient()


# ##################################################################################
# Google speech to text part.
"""
Reference: https://cloud.google.com/speech-to-text/docs/sync-recognize#speech-sync-recognize-python
"""


def speech_to_text(input_audio, client, sample_rate_hertz):
    with open(input_audio, 'rb') as f:
        mp3_data = f.read()

    input_audio_file = speech.RecognitionAudio(content=mp3_data)
    config = speech.RecognitionConfig(
        sample_rate_hertz=sample_rate_hertz,
        enable_automatic_punctuation=True,
        language_code='en-US'
    )
    response = client.recognize(
        config=config,
        audio=input_audio_file
    )
    json_string = speech.RecognizeResponse.to_json(response)
    response_dict = json.loads(json_string)
    query = response_dict['results'][0]['alternatives'][0]['transcript']
    print("S2T DONE with output: " + query)

    return query


# ##################################################################################

# Google text to speech part.
"""
Reference: https://cloud.google.com/text-to-speech/docs/libraries#client-libraries-install-python
"""


def text_to_speech(query_reply, client):
    print("T2S START with: " + query_reply)
    synthesis_input = texttospeech.SynthesisInput(text=query_reply)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    # with open(f"output_{index}.mp3", "wb") as out:
    #     out.write(response.audio_content)

    print("T2S DONE...")
    return response.audio_content


################################################################################

# Google dailogflow part
def query_dialogeflow(project_id, session_id, text, language_code, client):
    session = client.session_path(project_id, session_id)
    print("Session: " + session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    print("TEXT INPUT: ")
    print(text_input)
    query_input = dialogflow.QueryInput(text=text_input)
    print("QUERY INPUT: ")
    print(query_input)
    df_response = client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    print("DF RESPONSE: ")
    print(df_response)
    query_reply = format(df_response.query_result.fulfillment_text)
    print("DF DONE with output: " + query_reply)

    return query_reply
