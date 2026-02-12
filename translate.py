import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_text(text):

    prompt = f"""
Translate this English sentence to Hindi and Punjabi.

{text}

Format:
Hindi:
Punjabi:
"""

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )

    out = res.choices[0].message.content

    hindi = out.split("Punjabi:")[0].replace("Hindi:","").strip()
    punjabi = out.split("Punjabi:")[1].strip()

    return hindi,punjabi
