from ai import get_ai_response_groq
from stt import transcribe, record_audio, select_microphone
import queue
import threading
from tts import tts
from tools import search
from memory import load_conversations, save_conversation, list_conversations, create_conversation


## MICROPHONE SELECTION
# microphone = None
    
# if microphone is None:
#     microphone = select_microphone()
# audio_queue = queue.Queue()

## MAIN LOOP
# stop_event = threading.Event()
# thread = threading.Thread(target=record_audio, args=(microphone, audio_queue, stop_event))
# thread.start()

last_text = None
conversation = None

if conversation is None:
            name = input(f"{list_conversations()} \n Choose a conversation (type the name before .json, if the file doesn't exist a new conversation will be created): ")
            conversation = load_conversations(name)
      
      
try:
    while True:
        # audio = audio_queue.get()
        # text = transcribe(audio)
        text = input("Text: ")
        if text and text != last_text:
          last_text = text
          print("Sending to AI...")
          response, conversation = get_ai_response_groq(text, conversation)
          print("Got response:", response) 
          save_conversation(name, conversation)
          tts(response) 
          print("tts")
except KeyboardInterrupt:
    print("Shutting down...")
    # stop_event.set()
    # thread.join()


        