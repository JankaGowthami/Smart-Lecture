from flask import Flask, render_template, request, jsonify
import os
from subprocess import run
from summarize import summarize_text_from_file

app = Flask(_name_)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    # Run the speech-to-text script
    run(["python", "speech_to_text.py"])
    if os.path.exists("transcription.txt"):
        with open("transcription.txt", "r") as file:
            transcription = file.read()
        return jsonify({"transcription": transcription})
    return jsonify({"error": "Transcription failed!"})

@app.route("/summarize", methods=["POST"])
def summarize():
    summary = summarize_text_from_file("transcription.txt")
    if summary:
        return jsonify({"summary": summary})
    return jsonify({"error": "Summarization failed!"})

if _name_ == "_main_":
    app.run(debug=True)