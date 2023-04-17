from flask import Flask, render_template, request, redirect
from PyPDF2 import PdfReader
from classes import *


ENGLISH = {
    "language": "en-GB",
    "voices": ["en-GB-Wavenet-A", "en-GB-Wavenet-B", "en-GB-Wavenet-C", "en-GB-Wavenet-D"],
    "samples": ["Language/en-GB-Wavenet-A.mp3", "Language/en-GB-Wavenet-B.mp3",
                "Language/en-GB-Wavenet-C.mp3", "Language/en-GB-Wavenet-D.mp3"],
    "gender": ["female", "male", "female", "male"]
}
NORWEGIAN = {
    "language": "nb-NO",
    "voices": ["nb-NO-Wavenet-A", "nb-NO-Wavenet-B", "nb-NO-Wavenet-C", "nb-NO-Wavenet-D"],
    "samples": ["Language/nb-NO-Wavenet-A.mp3", "Language/nb-NO-Wavenet-B.mp3",
                "Language/nb-NO-Wavenet-C.mp3", "Language/nb-NO-Wavenet-D.mp3"],
    "gender": ["female", "male", "female", "male"]
}
SWEDISH = {
    "language": "sv-SE",
    "voices": ["sv-SE-Wavenet-A", "sv-SE-Wavenet-B", "sv-SE-Wavenet-C", "sv-SE-Wavenet-D"],
    "samples": ["Language/sv-SE-Wavenet-A.mp3", "Language/sv-SE-Wavenet-B.mp3",
                "Language/sv-SE-Wavenet-C.mp3", "Language/sv-SE-Wavenet-D.mp3"],
    "gender": ["female", "female", "male", "female"]
}

app = Flask(__name__)
language = ""
selected_voice = ""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/voice/<lang>", methods=["GET", "POST"])
def voice(lang):
    global language
    data = {}
    if lang == "en-GB":
        data = ENGLISH
    elif lang == "nb-NO":
        data = NORWEGIAN
    elif lang == "sv-SE":
        data = SWEDISH
    language = lang
    return render_template("voice.html", data=data)


@app.route("/input/<voice>", methods=["GET", "POST"])
def input(voice):
    global language
    global selected_voice
    if selected_voice == "":
        selected_voice = voice

    if request.method == "POST":
        file = request.files['file']
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text = text + page.extract_text()
        print(text)
        print(language)
        print(selected_voice)
        pdf_to_mp3(text, selected_voice, language)
        return redirect("/download")
    return render_template("input.html")


@app.route("/download")
def download():
    return render_template("download.html")


if __name__ == "__main__":
    app.run()
