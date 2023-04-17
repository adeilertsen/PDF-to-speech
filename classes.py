import os
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cohesive-armor-381212-0b44764aae31.json"
client = texttospeech.TextToSpeechClient()
def pdf_to_mp3(text_input, voice_name, language):

    synthesis_input = texttospeech.SynthesisInput(text=text_input)
    current_voice = texttospeech.VoiceSelectionParams(language_code=language, name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # ----------GETTING A SAMPLE OF EVERY VOICE IN EVERY LANGUAGE---------
    #
    # languages = ["da-DK", "en-GB", "nb-NO", "sv-SE"]
    # for lang in languages:
    #    voices = client.list_voices(language_code="lang")
    #    for voice in voices.voices:
    #        current_voice = texttospeech.VoiceSelectionParams(language_code="lang",
    #                                                              name=voice.name)
    #        response = client.synthesize_speech(input=synthesis_input, voice=current_voice, audio_config=audio_config)
    #        with open(f"{voice.name}.mp3", "wb") as out:
    #            out.write(response.audio_content)
    #

    response = client.synthesize_speech(input=synthesis_input, voice=current_voice, audio_config=audio_config)
    with open("static/download/output.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file 'output.mp3'")
    return response


def voice_samples(voices_list, lang):
    voice_sample = []
    for voice in voices_list:
        sample_text = ""
        if lang == "en-GB":
            sample_text = "Hi, do you want this voice?"
        elif lang == "no-NO":
            sample_text = "Hei, vil du ha denne stemmen?"
        elif lang == "sv-SE":
            sample_text = "hej, vill du ha den här rösten?"
        sample = pdf_to_mp3(sample_text, voice.name, lang, 1)
        voice_sample.append(sample)
    return voice_sample


def get_voices(language):
    voices = client.list_voices(language_code=language)
    selected_voices = []
    num = 0
    for voice in voices.voices:
        splitted_voice_name = voice.name.split("-")
        if num == 4:
            break
        elif splitted_voice_name[2] == "Wavenet":
            selected_voices.append(voice)
            num += 1
            print(voice)
    return selected_voices

def pdf_to_text(filename):
    with open(filename, 'rb') as f:
        pdf = PdfReader(f)
        text = ""
        for page in pdf.pages:
            text = text + page.extract_text()
        return text
