import textrazor
import os

# Set your TextRazor API key
textrazor.api_key = '0c74699f63a2ed1f5e10ed2b17fbb78dfeedc6d1f11ed6a1e8e5a7d0'

def get_sentences_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Use TextRazor to analyze the text
    response = textrazor.TextRazor().analyze(text)
    # Extract sentences from the response
    sentences = [sentence['text'] for sentence in response.sentences()]
    return sentences

if __name__ == "__main__":
    file_path = 'text.txt'

    if os.path.exists(file_path):
        sentences = get_sentences_from_file(file_path)
        
        for i, sentence in enumerate(sentences, start=1):
            print(f"Sentence {i}: {sentence}")
    else:
        print("File not found.")
