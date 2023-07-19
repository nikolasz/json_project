# Import the necessary libraries
import json
from typing import List, Dict, Optional

# Define the path to the JSON file
json_file_path = "conversations.json"

# Load the JSON data
with open(json_file_path, 'r') as f:
    data = json.load(f)


# Define the Message class
class Message:
    def __init__(self, id_: str, text: str, role: str, parent_message_id: Optional[str], children: List[str]):
        self.id_ = id_
        self.text = text
        self.role = role
        self.parent_message_id = parent_message_id
        self.children = children

# Define the Conversation class
class Conversation:
    def __init__(self, id_: str, title: str, create_time: int, messages: Dict[str, Message]):
        self.id_ = id_
        self.title = title
        self.create_time = create_time
        self.messages = messages

# Initialize an empty list to store the conversations
conversations = []

# Iterate over each dictionary in the data list
for d in data:
    # Extract the conversation fields
    id_ = d['id']
    title = d['title']
    create_time = d['create_time']

    # Initialize an empty dictionary to store the messages
    messages = {}

   # Iterate over each item in the 'mapping' field
    for message_id, message_data in d['mapping'].items():
    # Extract the message fields using the get method
        text = message_data.get('text')
        role = message_data.get('role')
        parent_message_id = message_data.get('parentMessageId')
        children = message_data.get('children', [])  # Default to an empty list if 'children' key does not exist

    # Create a Message object and add it to the messages dictionary
    message = Message(message_id, text, role, parent_message_id, children)
    messages[message_id] = message


    # Create a Message object and add it to the messages dictionary
    message = Message(message_id, text, role, parent_message_id, children)
    messages[message_id] = message

    # Create a Conversation object and add it to the conversations list
    conversation = Conversation(id_, title, create_time, messages)
    conversations.append(conversation)
