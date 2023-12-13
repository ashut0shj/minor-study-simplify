import textrazor
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re

textrazor.api_key = 'ef8ad06ae34fc0689dd7e3add12566244763534d95cd5b9770c9ba14'
stemmer = PorterStemmer()

def preprocess_text(text):
    
    text = re.sub(r'["\'{}[\]()]', '', text)
    
    text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{4}\b', '', text)  
    text = re.sub(r'\b\d{1,2}:\d{2}(?:\s*[APMapm]{2})?\b', '', text) 
    
    return text

def generate_summary(text):
    
    text = preprocess_text(text)

    client = textrazor.TextRazor(extractors=["entities", "topics"])
    response = client.analyze(text)

    entities = [(entity.relevance_score, tuple(stemmer.stem(word) for word in word_tokenize(entity.matched_text) if len(word) > 4)) for entity in response.entities()]
    entities = list(set(entities))
    entities.sort(reverse=True)  
    top_entities = entities[:5]  

    sentences = text.split('.')

    unique_sentences_with_entities = set()
    for sentence in sentences:
        for _, entity_words in top_entities:
            if any(word in stemmer.stem(sentence) for word in entity_words):
                unique_sentences_with_entities.add(sentence.strip())


    summary = "Summary: " + ' '.join(unique_sentences_with_entities)


    summary = re.sub(r'\d+', '', summary)

    return summary
user_input_text = input("Enter the text to be summarized: ")
summary_result = generate_summary(user_input_text)
print(summary_result)