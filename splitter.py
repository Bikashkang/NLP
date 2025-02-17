!pip install indic-nlp-library
!pip install openpyxl

import pandas as pd
import re
from indicnlp.tokenize import sentence_tokenize

# Define file paths
input_file = "/content/source.txt"
output_file = "/content/split.xlsx"

# Read the Hindi text file
with open(input_file, "r", encoding="utf-8") as file:
    text = file.read()

# Clean up text: Remove extra spaces, special characters if needed
text = re.sub(r'\s+', ' ', text).strip()

# Sentence segmentation and punctuation-based splitting
sentences = []
initial_sentences = sentence_tokenize.sentence_split(text, lang="hi")

split_chars = r'[|।?!]'  # Define punctuation characters to split on


for sent in initial_sentences:
    parts = re.split(f'({split_chars}+)', sent)  # Split AND capture the delimiters

    # Reconstruct sentences by alternating text and punctuation
    for i in range(0, len(parts), 2):
        sentence = parts[i].strip()  # Get the text part
        if sentence:  # Add if text is not empty
            if i + 1 < len(parts):  # Check if there is a delimiter after the text
                sentence += parts[i + 1].strip()  # Append the delimiter
            sentences.append(sentence)


# Filter sentences with word limits (6 to 50 words)
filtered_sentences = []
for sentence in sentences:
    if 6 <= len(sentence.split()) <= 60:
        filtered_sentences.append(sentence)

# Convert to DataFrame and save to Excel
df = pd.DataFrame({"Sentence": filtered_sentences})
df.to_excel(output_file, index=False, engine='openpyxl')  # Use engine='openpyxl'

print(f"Processed sentences saved to {output_file}")
