import json
import os

def init_thread_storage():
    if not os.path.exists('thread_ids.json'):
        with open('thread_ids.json', 'w') as file:
            json.dump({}, file)  # Initialize the file with an empty dictionary

def save_thread_id(user_id, thread_id):
    with open('thread_ids.json', 'r+') as file:
        data = json.load(file)
        data[user_id] = thread_id
        file.seek(0)
        file.truncate()  # Clear the file before writing the updated data
        json.dump(data, file, indent=4)

def get_thread_id(user_id):
    with open('thread_ids.json', 'r') as file:
        data = json.load(file)
        return data.get(user_id)