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
import os
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

def download_nltk_data():
    """Download required NLTK data"""
    print("Downloading NLTK data...")
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    print("✓ NLTK data downloaded")

def download_spacy_models():
    """Download spaCy English models"""
    print("Downloading spaCy models...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_md"], check=True)
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
    print("✓ spaCy models downloaded")

def install_sentencepiece():
    """Install SentencePiece"""
    print("Installing SentencePiece...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "sentencepiece"], check=True)
        print("✓ SentencePiece installed")
    except:
        print("⚠ Could not install SentencePiece, trying alternative model")

def download_transformers_models():
    """Download transformers models"""
    print("Downloading transformers models...")
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification
    
    try:
        # Try the original model first
        AutoTokenizer.from_pretrained("iarfmoose/t5-base-question-generator", use_fast=False)
        AutoModelForSeq2SeqLM.from_pretrained("iarfmoose/t5-base-question-generator")
        print("✓ Question generator model downloaded")
    except:
        # Use alternative model
        print("Using alternative question generator model...")
        AutoTokenizer.from_pretrained("valhalla/t5-small-qa-qg-hl", use_fast=False)
        AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-small-qa-qg-hl")
        print("✓ Alternative question generator model downloaded")
    
    # QA evaluator
    AutoTokenizer.from_pretrained("iarfmoose/bert-base-cased-qa-evaluator")
    AutoModelForSequenceClassification.from_pretrained("iarfmoose/bert-base-cased-qa-evaluator")
    
    print("✓ Transformers models downloaded")

def download_glove_model():
    """Download GloVe model"""
    print("Downloading GloVe model...")
    api.load("glove-wiki-gigaword-100")
    print("✓ GloVe model downloaded")

def main():
    print("Setting up models for Study Material Processor...")
    
    try:
        download_nltk_data()
        download_spacy_models()
        install_sentencepiece()
        download_transformers_models()
        download_glove_model()
        
        print("\n🎉 Setup complete! All models downloaded successfully.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have installed: pip install torch transformers spacy nltk gensim sentencepiece")

if __name__ == "__main__":
    main()