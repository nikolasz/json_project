import json
from typing import List, Dict, Optional
import pandas as pd

json_file_path = "conversations.json"

with open(json_file_path, 'r') as f:
    data = json.load(f)

class Message:
    def __init__(self, id_: str, message: str, parent_message_id: Optional[str], children: List[str]):
        self.id_ = id_
        self.message = message
        self.parent_message_id = parent_message_id
        self.children_ids = children
        self.children = []  # This will hold the actual Message objects

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

# Test to see how many conversations there are
print(len(conversations))

# Write the first 10 conversations to text files
for i, conversation in enumerate(conversations[:10]):
    file_path = f"conversation_{i+1}.txt"
    write_conversation_to_file(conversation, file_path)
    pass

# Revised function to extract data from message node
def extract_message_data(conversation_id, message_node):
    if message_node['message'] is None:
        return None
    else:
        if message_node['message']['content'] is not None and 'parts' in message_node['message']['content']:
            content = message_node['message']['content']['parts']
            if isinstance(content, list) and content:
                # Check if the first element of 'parts' is a dictionary
                if isinstance(content[0], dict):
                    content = content[0]['content']
                else:
                    # If the first element of 'parts' is not a dictionary, join all elements of 'parts' into a single string
                    content = " ".join(content)
        else:
            content = message_node['message']['content']
        return {
            'conversation_id': conversation_id,
            'message_id': message_node['id'],
            'parent_id': message_node['parent'],
            'author_role': message_node['message']['author']['role'],
            'create_time': message_node['message']['create_time'],
            'content': content,
        }

# List to hold data for all messages
data_list = []

# Extract data for each message
for conversation in data:
    for message_id, message_node in conversation['mapping'].items():
        message_data = extract_message_data(conversation['id'], message_node)
        if message_data is not None:
            data_list.append(message_data)

# Create a DataFrame
def create_dataframe(data_list):
    df = pd.DataFrame(data_list)
    return df
print(df.head())

# Create a dictionary of DataFrames for each conversation
conversations = {conv_id: conv_df.sort_values(by='create_time') for conv_id, conv_df in df.groupby('conversation_id')}

for conversation_id, conversation_df in conversations.items():
    print(f"Conversation ID: {conversation_id}\n")
    for idx, row in conversation_df.iterrows():
        print(f"{row['create_time']} - {row['author_role']}: {row['content']}\n")
    print("\n\n")


'''
# TODO
Separation of Concerns: Your current script does a lot of things: it defines the Message and Conversation classes, parses the JSON file, traverses the conversation tree, and writes the output to text files. You might want to consider separating these responsibilities into different modules or functions. This can make your code easier to understand, maintain, and extend. For example, the JSON parsing and the DFS traversal could be done in separate functions.

Code Documentation: Your code would benefit from more comments explaining what each part does, especially for the DFS traversal and the Message and Conversation classes. This would make it easier for others to understand and contribute to your code.

Error Handling: Currently, the script doesn't have much error handling. What happens if the JSON file is malformed, or if a conversation doesn't have a mapping field? Adding some error checking and handling can make your script more robust.

Testing: Consider adding tests to ensure that your script works as expected, especially if you plan to extend or modify it in the future.

Alternative Data Structures: While text files are a good start, they might not be the best format for complex, nested conversations. You might want to consider alternative data structures or formats that can preserve the tree structure of the conversations, such as XML or even a database, as you mentioned.
'''
