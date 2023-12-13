import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize
from typing import List, Tuple

custom_stopwords = ["of", "that", "an", "than", "then", "be", "as", "can", "could", "the", "to", "and", "but", "or",
                    "for", "nor", "so", "yet", "is", "am", "are", "was", "were", "has", "have", "had", "in", "on", "at",
                    "by", "with", "about", "under", "between", "before", "after", "during", "through", "above", "below",
                    "beside", "among", "near", "over", "from", "without", "however", "plus", "next", "up", "thus",
                    "therefore", "this", "these", "those", "also", "furthermore", "moreover", "likewise", "meanwhile",
                    "nonetheless", "otherwise", "similarly", "he", "his", "him", "they", "it", "not"]  # Add more words if needed


def preprocess_text(text):

    text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{4}\b', '', text)  # Remove dates
    text = re.sub(r'\b\d{1,2}:\d{2}(?:\s*[APMapm]{2})?\b', '', text)  # Remove times

    return text


def get_keywords(text: str, num_keywords=5) -> dict:

    text = preprocess_text(text)

    sentences = sent_tokenize(re.sub(r'\s+', ' ', text.strip()))

    max_words = 5

    filtered_text = " ".join([word for word in text.split() if word.lower() not in custom_stopwords and not any(c.isdigit() for c in word)])

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([filtered_text])

    feature_names = vectorizer.get_feature_names_out()

    important_words = [feature_names[i] for i in tfidf_matrix.toarray()[0].argsort()[-max_words:][::-1] if
                       len(feature_names[i]) > 3 and not any(c.isdigit() for c in feature_names[i])]

    keyword_sentences = {}

    for keyword in important_words:

        sentences_with_keyword = list(set([sentence for sentence in sentences if keyword in sentence]))

        if sentences_with_keyword:
            keyword_sentences[keyword] = sentences_with_keyword

    return keyword_sentences


if __name__ == "__main__":
    with open(r'trans.txt','r+') as file:
        input_text = file.read()
    keyword_sentences = get_keywords(input_text)

    print(keyword_sentences)
    if keyword_sentences:
        print("Keyword - Sentences:")
        for keyword, sentences in keyword_sentences.items():
            print(f"\n'{keyword}':")
            for sentence in sentences:
                print(f"  - {sentence}")z
    else:
        print("No keywords found.")