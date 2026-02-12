from gtts import gTTS

def text_to_speech(text):

    if not text.strip():
        return

    gTTS(text=text, lang="hi").save("output.mp3")
