import whisper

model = whisper.load_model("base")

def speech_to_text(path):
    result = model.transcribe(path)
    return result["text"]
