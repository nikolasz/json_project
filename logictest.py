import json

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


from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# Combine all the text from the conversations
all_text = ' '.join(message['text'] for conversation in conversations for message in conversation['messages'])

# Convert the text to lower case
all_text = all_text.lower()

# Remove punctuation
all_text = re.sub(r'\W', ' ', all_text)

# Split the text into words and count each word
word_counts = Counter(all_text.split())

# Remove common stop words
stop_words = set(['the', 'and', 'is', 'it', 'to', 'in', 'that', 'of', 'for', 'on', 'you', 'with', 'as', 'are', 'this', 'was', 'or', 'be', 'at', 'not', 'by', 'from', 'but', 'an', 'which', 'if', 'we', 'can', 'has', 'more', 'will', 'about', 'up', 'also', 'there', 'out', 'so', 'your', 'all', 'have', 'their', 'they', 'one', 'has', 'just', 'what', 'some', 'other', 'like', 'these', 'how', 'than', 'its', 'time', 'into', 'only', 'could', 'new', 'them', 'people', 'may', 'any', 'last', 'see', 'us', 'off', 'first', 'world', 'year', 'do', 'years', 'two', 'where', 'make', 'our', 'other', 'way', 'over', 'because', 'now', 'him', 'most', 'made', 'after', 'before', 'use', 'just', 'being', 'then', 'back', 'our', 'through', 'while', 'much', 'those', 'should', 'well', 'even', 'between', 'these', 'down', 'my', 'something', 'against', 'each', 'day', 'get', 'go', 'number', 'no', 'work', 'however', 'part', 'take', 'place', 'made', 'live', 'where', 'after', 'back', 'little', 'only', 'round', 'man', 'year', 'came', 'show', 'every', 'good', 'me', 'give', 'our', 'under', 'i', 's', '4', 'a', '1', '2', 'model', '3', '5'])
for stop_word in stop_words:
    word_counts.pop(stop_word, None)

# Generate the word cloud
wordcloud = WordCloud(width=1200, height=800).generate_from_frequencies(word_counts)

# Display the word cloud
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bicubic', cmap='coolwarm')
plt.axis('off')
plt.show()
