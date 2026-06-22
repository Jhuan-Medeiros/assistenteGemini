import os
import time
import ctypes
import speech_recognition as sr
from google import genai
from gtts import gTTS

chaveApiGoogle = "chave_api"
client = genai.Client(api_key=chaveApiGoogle)

def silenciar_alsa():
    try:
        asound = ctypes.CDLL("libasound.so.2")
        asound.snd_lib_error_set_handler(None)
    except:
        pass

def falar(texto):
    print(f"Gemini falando o text: {texto}")
    tts = gTTS(text=texto, lang="pt", tld="com.br")
    tts.save("resposta.mp3")
    os.system("mpg123 -o alsa resposta.mp3 > /dev/null 2>&1")

def ouvir():
    silenciar_alsa()
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 300

    with sr.Microphone() as source:
        print("Ajustando o ruido por 1 segundo")
        print("Microfone captando, gemini disponível")
        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=15)
            print("Áudio capturado, gerando resposta")
            comando = r.recognize_google(audio, language='pt-BR')
            print(f"Gemini entendeu: {comando}")
            return comando.lower()
        except sr.RequestError:
            print("Sem conexão com rede")
            return ""
        except Exception as e:
            return ""
    
if __name__ == "__main__":
    falar("Sistema iniciado")
    while(True):
        fala_usuario = ouvir()
        if "snake" in fala_usuario:
            pergunta = fala_usuario.replace("snake", "").strip()
            if pergunta:
                try:
                    resposta = client.models.generate_content(model="gemini-3.5-flash", contents=pergunta)
                    falar(resposta.text)
                except Exception as e:
                    print(f"Houve um erro na API: {e}")
                    falar("Houve um erro ao conectar com o novo servidor")
            time.sleep(0.1)