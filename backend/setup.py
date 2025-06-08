#!/usr/bin/env python3
"""
Setup script to download required models for the question generation system
Run this once after installing requirements
"""

import nltk
import spacy
import gensim.downloader as api
import subprocess
import sys

def download_nltk_data():
    """Download required NLTK data"""
    print("Downloading NLTK data...")
    try:
        nltk.download('punkt')
        nltk.download('stopwords')
        print("✓ NLTK data downloaded successfully")
    except Exception as e:
        print(f"✗ Error downloading NLTK data: {e}")

def download_spacy_model():
    """Download spaCy English model"""
    print("Downloading spaCy English model...")
    try:
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_md"], check=True)
        print("✓ spaCy model downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error downloading spaCy model: {e}")
        print("Try running manually: python -m spacy download en_core_web_md")

def download_gensim_model():
    """Download GloVe model for word embeddings"""
    print("Downloading GloVe model (this may take a while)...")
    try:
        # This will download and cache the model
        model = api.load("glove-wiki-gigaword-100")
        print("✓ GloVe model downloaded successfully")
    except Exception as e:
        print(f"✗ Error downloading GloVe model: {e}")

def main():
    print("Setting up models for Study Material Processor...")
    print("This may take several minutes...")
    
    download_nltk_data()
    download_spacy_model()  
    download_gensim_model()
    
    print("\n🎉 Setup complete! You can now run the FastAPI server.")
    print("Run: python main.py")

if __name__ == "__main__":
    main()