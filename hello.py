import textrazor
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re

textrazor.api_key = 'ef8ad06ae34fc0689dd7e3add12566244763534d95cd5b9770c9ba14'
stemmer = PorterStemmer()

def preprocess_text(text):
    # Remove unwanted characters and symbols
    text = re.sub(r'["\'{}[\]()]', '', text)
    
    # Remove dates and times using regular expressions
    text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{4}\b', '', text)  # Remove dates
    text = re.sub(r'\b\d{1,2}:\d{2}(?:\s*[APMapm]{2})?\b', '', text)  # Remove times
    
    return text

def generate_summary(text):
    # Preprocess the input text
    text = preprocess_text(text)

    client = textrazor.TextRazor(extractors=["entities", "topics"])
    response = client.analyze(text)

    # Extracting relevant information with stemming and length filter
    entities = [(entity.relevance_score, tuple(stemmer.stem(word) for word in word_tokenize(entity.matched_text) if len(word) > 4)) for entity in response.entities()]
    entities = list(set(entities))  # Remove duplicate entities after stemming and length filtering
    entities.sort(reverse=True)  # Sorting entities by relevance score in descending order
    top_entities = entities[:10]  # Selecting the top 10 entities

    # Tokenize the input text into sentences
    sentences = text.split('.')

    # Extracting unique sentences containing top entities
    unique_sentences_with_entities = set()
    for sentence in sentences:
        for _, entity_words in top_entities:
            if any(word in stemmer.stem(sentence) for word in entity_words):
                unique_sentences_with_entities.add(sentence.strip())

    # Constructing the summary paragraph
    summary = "Summary: " + ' '.join(unique_sentences_with_entities)

    # Remove numbers and digits from the summary
    summary = re.sub(r'\d+', '', summary)

    return summary

# Take user input for the text to be summarized
user_input_text = input("Enter the text to be summarized: ")
summary_result = generate_summary(user_input_text)
print(summary_result)
