import json
from typing import List, Dict, Optional

# Define the path to the JSON file
json_file_path = "conversations.json"

# Load the JSON data
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Define the Message class
class Message:
    def __init__(self, id_: str, message: str, parent_message_id: Optional[str], children: List[str]):
        self.id_ = id_
        self.message = message
        self.parent_message_id = parent_message_id
        self.children_ids = children
        self.children = []  # This will hold the actual Message objects

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
        message = message_data.get('message')
        parent_message_id = message_data.get('parent')
        children_ids = message_data.get('children', [])  # Default to an empty list if 'children' key does not exist

        # Create a Message object and add it to the messages dictionary
        message = Message(message_id, message, parent_message_id, children_ids)
        messages[message_id] = message

    # After all the messages have been created, link the child messages to their parent messages
    for message in messages.values():
        message.children = [messages[child_id] for child_id in message.children_ids if child_id in messages]

    # Create a Conversation object and add it to the conversations list
    conversation = Conversation(id_, title, create_time, messages)
    conversations.append(conversation)

# Define the DFS function
def dfs(message_id, messages, visited):
    visited.add(message_id)
    message_text = ""
    message = messages[message_id]
    if message.message is not None:
        message_text += f"{message.message}\n"
    for child_id in message.children_ids:
        if child_id not in visited:
            message_text += dfs(child_id, messages, visited)
    return message_text

# Get the text of a conversation
def get_conversation_text(conversation):
    # Initialize an empty set to store the IDs of visited messages
    visited = set()

    # Initialize an empty string to store the conversation text
    conversation_text = ""

    # Perform a depth-first traversal of the conversation tree
    for message_id, message in conversation.messages.items():
        if message.parent_message_id is None:  # This is a root message
            conversation_text += dfs(message_id, conversation.messages, visited)

    return conversation_text

# Write a conversation to a text file
def write_conversation_to_file(conversation, file_path):
    # Get the text of the conversation
    conversation_text = get_conversation_text(conversation)

    # Write the text to the file
    with open(file_path, 'w') as f:
        f.write(conversation_text)

# Write the first 10 conversations to text files
for i, conversation in enumerate(conversations[:10]):
    file_path = f"conversation_{i+1}.txt"
    write_conversation_to_file(conversation, file_path)

# Write a conversation to a text file
def write_conversation_to_file(conversation, file_path):
    # Get the text of the conversation
    conversation_text = get_conversation_text(conversation)

    # Write the text to the file
    with open(file_path, 'w') as f:
        f.write(conversation_text)

# Write the first 10 conversations to text files
for i, conversation in enumerate(conversations[:10]):
    file_path = f"conversation_{i+1}.txt"
    write_conversation_to_file(conversation, file_path)
