from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

# Load the data and create the DataFrame
with open('conversations.json') as f:
    data = json.load(f)

data_list = []
for conversation in data:
    for message_id, message_node in conversation['mapping'].items():
        message_data = extract_message_data(conversation['id'], message_node)
        if message_data is not None:
            data_list.append(message_data)

df = pd.DataFrame(data_list)

# Group by conversation_id
conversations = {conv_id: conv_df.sort_values(by='create_time') for conv_id, conv_df in df.groupby('conversation_id')}

@app.route('/')
def index():
    # List all conversation IDs
    return render_template('index.html', conversations=conversations)

@app.route('/conversation/<conversation_id>')
def conversation(conversation_id):
    # Get the specific conversation
    conversation = conversations[conversation_id]
    return render_template('conversation.html', conversation=conversation)

if __name__ == '__main__':
    app.run(debug=True)


System Message:
        User Profile: {...}
        Additiona Instructions: {...}

