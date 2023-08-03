import re
import json

# Load the new JSON file
with open('conversations.json', 'r') as f:
    json_content = f.read()

# Search for 'system' or 'System' in the raw HTML content
system_indices = [m.start() for m in re.finditer(r'\bsystem message\b', json_content, re.IGNORECASE)]

# Extract the sentences containing each occurrence of 'system' or 'System'
sentences = []

for index in system_indices:
    # Find the start and end of the 'system' or 'System' term
    term_start = index
    term_end = index + len('system')

    # Check if the term is a standalone word
    if ((term_start == 0 or not json_content[term_start - 1].isalnum()) and
        (term_end == len(json_content) or not json_content[term_end].isalnum())):
        # Find the start of the sentence
        sentence_start = json_content.rfind('.', 0, term_start)
        sentence_start = json_content.rfind('!', 0, term_start) if sentence_start == -1 else sentence_start
        sentence_start = json_content.rfind('?', 0, term_start) if sentence_start == -1 else sentence_start
        sentence_start += 2 if sentence_start != -1 else 0

        # Find the end of the sentence
        sentence_end = json_content.find('.', term_end)
        sentence_end = json_content.find('!', term_end) if sentence_end == -1 else sentence_end
        sentence_end = json_content.find('?', term_end) if sentence_end == -1 else sentence_end
        sentence_end = len(json_content) if sentence_end == -1 else sentence_end + 1

        # Extract and store the sentence
        sentences.append(json_content[sentence_start:sentence_end].strip())

for i, sentence in enumerate(sentences, 1):
    print(f"Snippet #{i}:")
    print(sentence)
    print("\n")



