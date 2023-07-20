import os
import tiktoken

# Get the tokenizer corresponding to a specific model in the OpenAI API:
tokenizer = tiktoken.encoding_for_model("gpt-4")

# Directory path
dir_path = os.getcwd()

# List all files in directory
files = os.listdir(dir_path)

# Loop through all txt files
for file in files:
    if file.endswith((('.txt', '.md', '.json', 'py'))):
        file_path = os.path.join(dir_path, file)

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        tokens = tokenizer.encode(text, disallowed_special=())

        print(f"{file}: {len(tokens)}")
