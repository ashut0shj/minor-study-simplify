import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize
from typing import List, Tuple
import os
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


def get_keywords(text: str, num_keywords=5) -> Tuple[List[str], List[str]]:

    text = preprocess_text(text)

    sentences = sent_tokenize(re.sub(r'\s+', ' ', text.strip()))

    max_words = 4 if len(text.split()) < 1000 else 5

    filtered_text = " ".join([word for word in text.split() if word.lower() not in custom_stopwords and not any(c.isdigit() for c in word)])

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([filtered_text])

    feature_names = vectorizer.get_feature_names_out()

    important_words = [feature_names[i] for i in tfidf_matrix.toarray()[0].argsort()[-max_words:][::-1] if
                       len(feature_names[i]) > 3 and not any(c.isdigit() for c in feature_names[i])]

    keyword_sentences = []

    for keyword in important_words:
        sentences_with_keyword = [sentence for sentence in sentences if keyword in sentence]

        if sentences_with_keyword:
            keyword_sentences.extend(sentences_with_keyword)

    unique_sentences = list(set(keyword_sentences))
    paragraph = " ".join(unique_sentences)

    return important_words, paragraph


if __name__ == "__main__":
    input_text = input("Enter the text: ")
    os.system('clear')
    important_words, paragraph = get_keywords(input_text)
    if important_words:
        print("Important words:")
        for word in important_words:
            print(f"'{word}'")

    if paragraph:
        print("\nUnique sentences containing important keywords in a single paragraph:")
        os.system('clear')
        with open(r'summ.txt','w+') as file:
            file.write(paragraph)

        print(paragraph)
    else:
        print("No unique sentences found.")
