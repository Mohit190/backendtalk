from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import whisper
from gtts import gTTS
from deep_translator import GoogleTranslator
import base64
import os

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

print("Loading Whisper...")
model = whisper.load_model("base")

audio_chunks = []


@socketio.on("audio")
def receive_audio(data):
    audio_chunks.append(bytes(data))


@socketio.on("stop")
def stop_audio():
    global audio_chunks

    with open("input.wav", "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)

    audio_chunks = []

    # Speech → Text
    result = model.transcribe("input.wav")
    english = result["text"]

    # Translate
    hindi = GoogleTranslator(source="en", target="hi").translate(english)
    punjabi = GoogleTranslator(source="en", target="pa").translate(english)

    # Hindi TTS
    tts = gTTS(hindi, lang="hi")
    tts.save("hindi.mp3")

    # Convert audio to base64
    with open("hindi.mp3", "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode()

    socketio.emit("result", {
        "english": english,
        "hindi": hindi,
        "punjabi": punjabi,
        "audio": "data:audio/mp3;base64," + audio_base64
    })


if __name__ == "__main__":
    print("Starting server...")
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
