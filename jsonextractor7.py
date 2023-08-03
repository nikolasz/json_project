import json
import re

# Load the JSON data
with open('conversations.json') as f:
    data = json.load(f)

def get_conversation_messages(conversation):
    messages = []
    current_node = conversation['current_node']
    while current_node is not None:
        node = conversation['mapping'][current_node]
        if (node['message'] and node['message']['content']
            and node['message']['content']['content_type'] == 'text'
            and len(node['message']['content']['parts']) > 0
            and len(node['message']['content']['parts'][0]) > 0
            and (node['message']['author']['role'] != 'system' or node['message']['metadata']['is_user_system_message'])):

            author = node['message']['author']['role']
            if author == 'assistant':
                author = 'ChatGPT'
            elif author == 'system' and node['message']['metadata']['is_user_system_message']:
                author = 'Custom user info'

            messages.append({'author': author, 'text': node['message']['content']['parts'][0]})

        current_node = node['parent']

    # Reverse the order of messages to match the original order
    messages.reverse()
    return messages

conversations = []
for conversation in data:
    messages = get_conversation_messages(conversation)
    conversations.append({
        'title': conversation['title'],
        'messages': messages,
    })

# Now `conversations` is a list of conversations, and you can manipulate it as you need.
# For example, let's print all conversations:
for conversation in conversations:
    print('Title:', conversation['title'])
    for message in conversation['messages']:
        print(f"{message['author']}: {message['text']}")


# Function to parse the messages and return any message that contains 'system message' (case-insensitive)
def parse_messages(conversations):
    system_messages = []
    for conversation in conversations:
        for message in conversation['messages']:
            if re.search(r'\bsystem message\b', message['text'], re.IGNORECASE):
                system_messages.append(message['text'])
    return system_messages

# Call the function and print the returned messages
system_messages = parse_messages(conversations)

for message in system_messages:
    print(message)
