import os
import json
import google.generativeai as genai
from typing import Tuple, List

genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyC2OHi_8f0J8nFvWUF0hFb81MwgD5A4xe0"))
model = genai.GenerativeModel('gemini-1.5-flash')

def save_debug_file(filename: str, content: str):
    """Save debug content to file"""
    os.makedirs('debug', exist_ok=True)
    with open(f'debug/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)

def get_keywords_gemini(text: str, save_debug_files: bool = True) -> Tuple[List[str], str]:
    """
    Extract important keywords and generate summary using Gemini API
    """
    prompt = f"""
    Please analyze the following text and provide:
    1. A list of 10-15 most important keywords/key phrases that represent the core concepts
    2. A comprehensive summary paragraph (200-300 words) that captures the main ideas and important details
    
    Format your response as JSON with the following structure:
    {{
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "summary": "Your comprehensive summary paragraph here..."
    }}
    
    Text to analyze:
    {text}
    """
    
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    
    if save_debug_files:
        save_debug_file('gemini_summarize_raw_response.txt', response_text)
    
    # Clean JSON formatting
    if response_text.startswith('```json'):
        response_text = response_text.replace('```json', '').replace('```', '').strip()
    elif response_text.startswith('```'):
        response_text = response_text.replace('```', '').strip()
    
    result = json.loads(response_text)
    keywords = result.get('keywords', [])
    summary = result.get('summary', '')
    
    # Limit keywords to 15
    keywords = keywords[:15] if len(keywords) > 15 else keywords
    
    if save_debug_files:
        debug_content = f"Keywords ({len(keywords)}):\n"
        debug_content += "\n".join([f"- {kw}" for kw in keywords])
        debug_content += f"\n\nSummary ({len(summary)} chars):\n{summary}"
        save_debug_file('gemini_summarize_processed.txt', debug_content)
    
    return keywords, summary

def test_summarization():
    """Test function for the summarization module"""
    test_text = """
    Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines 
    that can think and act like humans. Machine learning is a subset of AI that enables computers to learn 
    and improve from experience without being explicitly programmed. Deep learning, a subset of machine learning, 
    uses neural networks with multiple layers to analyze and learn from large amounts of data. These technologies 
    are revolutionizing various industries including healthcare, finance, transportation, and entertainment.
    """
    
    keywords, summary = get_keywords_gemini(test_text)
    print("Keywords:", keywords)
    print("\nSummary:", summary)

if __name__ == "__main__":
    test_summarization()