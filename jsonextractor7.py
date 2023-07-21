import json
from typing import List, Dict, Optional

json_file_path = "conversations.json"

with open(json_file_path, 'r') as f:
    data = json.load(f)


def get_schema(data):
    schema = {}
    for obj in data.values():
        if isinstance(obj, dict):
            schema[obj[0].keys()] = "dict"
            schema.update(get_schema(obj[0]))
        elif isinstance(obj, dict):
            schema.update(get_schema(obj))

    return schema

json_schema = get_schema(data)

print(json_schema)

"properties": {
                    "id": {
                        "type": "str"
                    },
                    "parentId": {
                        "type": "str"
                    },
                    "childId": {
                        "type": "str"
                    },
                    "content": {
                        "type": "str"


'''
conversations.json:
[{"title": "[title]", "create_time": EPOCHEPOCH.MILLIS, "update_time": 1682606050.0, "mapping": {"[redacted]": {"id": "[redacted]", "message": {"id": "[redacted]", "author": {"role": "system", "name": null, "metadata": {}}, "create_time": EPOCHEPOCH.MILLIS, "update_time": null, "content": {"content_type": "text", "parts": [""]}, "end_turn": true, "weight": 1.0, "metadata": {}, "recipient": "all"}, "parent": "[redacted]", "children": ["[redacted]"]}, "[redacted]": {"id": "[redacted]", "message": null, "parent": null, "children": ["[redacted]"]}, "[redacted]": {"id": "[redacted]", "message": {"id": "[redacted]", "author": {"role": "user", "name": null, "metadata": {}}, "create_time": EPOCHEPOCH.MILLIS, "update_time": null, "content": {"content_type": "text", "parts": ["<insert user message>"]}, "end_turn": null, "weight": 1.0, "metadata": {"timestamp_": "absolute", "message_type": null}, "recipient": "all"}, "parent": "[redacted]", "children": ["[redacted]"]}, "[redacted]": {"id": "[redacted]", "message": {"id": "[redacted]", "author": {"role": "assistant", "name": null, "metadata": {}}, "create_time": EPOCHEPOCH.MILLIS, "update_time": null, "content": {"content_type": "text", "parts": ["<insert ChatGPT message> ... skipping ahead ... "]}, "end_turn": true, "weight": 1.0, "metadata": {"message_type": null, "model_slug": "[redacted]", "finish_details": {"type": "stop", "stop": "<|im_end|>"}, "timestamp_": "absolute"}, "recipient": "all"}, "parent": "[redacted]", "children": []}}, "moderation_results": [], "current_node": "[redacted]", "plugin_ids": null, "id": "[redacted]"}]



'''


<html>
<head>
    <title>ChatGPT Data Export</title>
    <style>
        body {
            margin: 20px;
        }
        h4 {
            font-family: sans-serif;
            margin: 0;
        }
        #root {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .conversation {
            border: 1px solid black;
            padding: 20px;
            background-color: #f3f3f3;
        }
        .message {
            white-space: pre-wrap;
            margin: 20px 0;
        }
        .author {
            font-weight: bold;
            margin-bottom: 4px;
        }
        .author::first-letter {
            text-transform: uppercase;
        }
    </style>
    <script>
var jsonData = <insert data here>

function getConversationMessages(conversation) {
    var messages = [];
    var currentNode = conversation.current_node;
    while (currentNode != null) {
        var node = conversation.mapping[currentNode];
        if (node.message &&
            node.message.content &&
            node.message.content.content_type == "text"
            && node.message.content.parts.length > 0 &&
            node.message.content.parts[0].length > 0 &&
            node.message.author.role != "system") {
            author = node.message.author.role;
            if (author === "assistant") {
                author = "ChatGPT";
            }
            messages.push({ author, text: node.message.content.parts[0] });
        }
        currentNode = node.parent;
    }
    return messages.reverse();
}

// on load, add messages to the root div
window.onload = function() {
    var root = document.getElementById("root");
    for (var i = 0; i < jsonData.length; i++) {
        var conversation = jsonData[i];
        var messages = getConversationMessages(conversation);
        var div = document.createElement("div");
        div.className = "conversation";
        div.innerHTML = "<h4>" + conversation.title + "</h4>";
        for (var j = 0; j < messages.length; j++) {
            var message = document.createElement("pre");
            message.className = "message";
            message.innerHTML = `<div class="author">${messages[j].author}</div><div>${messages[j].text}</div>`;
            div.appendChild(message);
        }
        root.appendChild(div);
    }
}
    </script>
</head>
<body>
<div id="root">
</div>
</body>
</html>