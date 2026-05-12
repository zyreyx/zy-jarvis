import sounddevice as sd
import queue
import webrtcvad
import requests
import wave
import io
import time

## Select Microphone
global model
global response_text
#global sample_rate 
#global block_size 
global device_list
#sample_rate = None
#block_size = None
device_list = []
response_text = None
model = "Systran/faster-whisper-small"

def select_microphone():
    for i, device in enumerate(sd.query_devices()):
        if device['max_input_channels'] > 0:
           print(f"{i}: {device['name']}")
           device_list.append((i, device['name'], device["default_samplerate"]))
    
        
    microphone = int(input(
        f"Please choose the microphone you want to use and"
        f" input the indentifying number: "
        ))
    for index, name, default_samplerate in device_list: 
        if index == microphone:
            #global sample_rate
            #global block_size 
            print(f"You have selected microphone: {name}")
            #sample_rate = int(default_samplerate)
            #block_size = int(sample_rate * 0.03)
            #print(sample_rate)
    
    return(microphone)


## Convert Audio To Wav

def to_wav(audio_bytes):
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # int16 = 2 bytes
        wf.setframerate(16000)
        wf.writeframes(audio_bytes)
    wav_buffer.seek(0)
    return wav_buffer


## Transcribe Audio
def transcribe(audio):
    global model
    global response_text
    response_text = None
    wav_audio = to_wav(audio)

    files = {
    'file': ('audio.wav', wav_audio, 'audio/wav'),
    'model': (None, model)
}
    response = requests.post(url = "http://localhost:8000/v1/audio/transcriptions", files=files)
    data = response.json()
    recog_text = data.get("text","")
    lower_text = recog_text.lower()
    wake_word = "jarvis"
    if wake_word.lower() in lower_text:
        after = lower_text.partition(wake_word.lower())[2].lstrip(", .")
        response_text = after
        print(f"Wake word: {wake_word} detected")
        print(response_text)
    else: 
        if recog_text != None or "":
            print(recog_text)
    return response_text
    
     



## Get Microphone Input 

def record_audio(microphone, audio_queue, stop_event): 
    vad = webrtcvad.Vad()
    vad.set_mode(3)
    silence_counter = 0
    buffer = []

    while True:
        if stop_event.is_set():
            break
        with sd.RawInputStream(samplerate=16000, channels=1, dtype='int16', device=microphone, blocksize=480) as stream:
            while True:
                chunk, overflowed = stream.read(480)
                is_speech = vad.is_speech(bytes(chunk), sample_rate=16000)
                
                if is_speech:
                    buffer.append(chunk)
                    silence_counter = 0
                else:
                    if len(buffer) > 3: 
                        silence_counter += 1
                if silence_counter > 30:
                    print("stopped recording")
                    break
                    
                
        audio_queue.put(b''.join(buffer))
        silence_counter = 0
        buffer = []

   
        