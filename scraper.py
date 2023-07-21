from bs4 import BeautifulSoup
import re

# Load the HTML file
with open('chat.html', 'r') as f:
  html_content = f.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all paragraphs that contain 'system' or 'System'
paragraphs_with_system = [p for p in soup.find_all('p') if 'system' in p.text.lower()]

# Extract following paragraphs
following_paragraphs = []

for p in paragraphs_with_system:
    sibling = p.find_next_sibling()
    if sibling and sibling.name == 'p':
        following_paragraphs.append(sibling.text)

following_paragraphs
# Extract following text-containing elements
following_elements = []

for p in paragraphs_with_system:
    sibling = p.find_next_sibling()
    while sibling:
        if sibling.name in ['p', 'div', 'span'] and sibling.text.strip():
            following_elements.append(sibling.text)
            break
        sibling = sibling.find_next_sibling()

following_elements
import re

# Get the entire text content of the HTML
text_content = soup.get_text()

# Split the text into sentences
sentences = re.split(r'(?<=[.!?])\s+', text_content)

# Find sentences that contain 'system' or 'System' and take the subsequent sentences
following_sentences = []

for i in range(len(sentences) - 1):
    if 'system' in sentences[i].lower():
        following_sentences.append(sentences[i + 1])

following_sentences
# Search for 'system' or 'System' in the text content
system_indices = [m.start() for m in re.finditer(r'\bsystem\b', text_content, re.IGNORECASE)]

# Print the text surrounding each occurrence of 'system' or 'System'
surrounding_text = []

for index in system_indices:
    start = max(0, index - 50)
    end = min(len(text_content), index + 50)
    surrounding_text.append(text_content[start:end])

surrounding_text
