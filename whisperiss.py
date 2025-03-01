import whisper
import pyaudio 
import wave 
import os
import speech_recognition as sr
from os import system
import sys
import time
import pyttsx3

engine = pyttsx3.init()

STOP_KEYWORD = "stop"
model = whisper.load_model("base")
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

def listening():
   
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)  
    frames = []
    r = sr.Recognizer()
        
    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    output_file = "recorded_audio.wav"
    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    model = whisper.load_model("tiny")
    results = model.transcribe("recorded_audio.wav")
    res=results['text']
    speak(res)
    return res

def speak(text):
    if sys.platform=='darwin':
        ALLOWED_CHARS=set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.,?!-_$: ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

