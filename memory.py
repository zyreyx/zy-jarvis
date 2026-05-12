from pathlib import Path 
import os
import json





def create_conversation(name):
    path = Path("conversations")
    create_path = Path("conversations") / f"{name}.json"
    if create_path.exists():
        print(f"Conversation: {name} already exists.")
        return(f"Conversation: {name} already exists.")
    else:
        with open(create_path, "w") as f:
            json.dump([], f)

def load_conversations(name):
    path = Path("conversations")
    load_path = Path(path) / f"{name}.json"
    if load_path.exists():
        with open(load_path, "r") as f:
            return(json.load(f))
    else: 
        create_conversation(name)
        return []
          

def save_conversation(name,messages):
    path = Path("conversations")
    save_path = Path(path) / f"{name}.json"
    if save_path.exists():
        with open(save_path, "w") as f:
            json.dump(messages, f)
    else: 
        print("Save conversation path does not exist")
        return("Save conversation path does not exist") 

def delete_conversation(name):
    path = Path("conversations")
    delete_path = Path(path) / f"{name}.json"
    if delete_path.exists():
        os.remove(delete_path)
    else:
        print("Delete path does not exist")
        return("Delete path does not exist")


def list_conversations():
    path = Path("conversations")
    if path.exists():
        return(os.listdir(path))
    else:
        return("Detrimental error, converstion folder does not exist")
    