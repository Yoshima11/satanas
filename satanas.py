import os
import speech_recognition as sr 
from vosk import Model, KaldiRecognizer
import pyttsx3
import json


class VoskRecognizer(sr.Recognizer):
    def __init__(self, model_path):
        super().__init__()
        if not os.path.exists(model_path):
            raise ValueError(f"Modelo Vosk no encontrado en {model_path}")
        self.model = Model(model_path)

    def recognize_vosk(self, audio_data, language="es-ES"):
        recognizer = KaldiRecognizer(self.model, audio_data.sample_rate)
        recognizer.SetWords(True)

        wav_data = audio_data.get_wav_data()
        if recognizer.AcceptWaveform(wav_data):
            result = json.loads(recognizer.Result())
            return result.get("text", "")
        else:
            partial_result = json.loads(recognizer.PartialResult())
            return partial_result.get("partial", "")

model_path = "vosk-model-small-es-0.42"
vosk_recognizer = VoskRecognizer(model_path)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"Voz {index}: {voice.name} ({voice.id})")
engine.setProperty("voice", voices[35].id)

def bot_talk(text):
    print (f"Respuesta: {text}")
    engine.say(text)
    engine.runAndWait()

def exec_command(text):
    text = text.lower()

    if "hola" in text:
        print("hola, ¿Cómo estas?")
        bot_talk("¡Hola!, ¿Cómo estas?")
    elif "hora" in text:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        print(f"La hora actual es {now}.")
        bot_talk(f"La hora actual es {now}.")
    elif "salir" in text:
        print("Saliendo...")
        bot_talk("Saliendo.")
        return True
    else:
        print(f"Comando no reconocido: {text}")
        bot_talk(f"Comando no reconocido: {text}")
    return False

def mic_rec():
    with sr.Microphone() as source:
        while True:
            print("Di algo!...")
            audio = vosk_recognizer.listen(source)
            try:
                text = vosk_recognizer.recognize_vosk(audio)
                if text:
                    print("Has dicho: ", text)
                    if exec_command(text):
                        break
            except sr.UnknownValueError:
                print("No se pudo entender el audio")
            except sr.RequestError as e:
                print(f"Error al solicitar el resultado; {e}")

if __name__ == "__main__":
    mic_rec()

