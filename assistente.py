import os
import time
import speech_recognition as sr
import google.generativeai as genai
from gtts import gTTS
import ctypes

chave_api = "API"

genai.configure(api_key=chave_api)
modelo = genai.GenerativeModel("gemini-1.5-flash")

def fala(texto):
    print(f"Gemini: {texto}")
    tts = gTTS(text=texto, lang="pt", tld="com.br")

    tts.save("resposta.mp3")
    os.system("mpg123 resposta.mp3 > /dev/null 2>&1")

def silenciar_alsa():
    try:
        asound = ctypes.CDLL("libasound.so.2")
        asound.snd_lib_error_set_handler(None)
    except:
        pass

def ouvir():
    silenciar_alsa()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Aguardando palavra de ativação...")
        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=7)
            comando = r.recognize_google(audio, language="pt-BR")
            return comando.lower()
        except Exception:
            return ""
        
if __name__ == "__main__":
    fala("Sistema de voz iniciado")
    while True:
        falaUsuario = ouvir()
        if "gemini" in falaUsuario:
            pergunta = falaUsuario
            pergunta = falaUsuario.replace("gemini", "").strip()
            if pergunta:
                try:
                    resposta = modelo.generate_content(pergunta)
                    resposta_texto = resposta.text
                    fala(resposta_texto)
                except Exception as e:
                    print(f"Erro na API: {e}")
                    fala("Houve um erro ao conectar com o servidor do Gemini.")
                time.sleep(0.1)

    