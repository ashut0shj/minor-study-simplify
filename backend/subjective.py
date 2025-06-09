import os
import json
import google.generativeai as genai
from typing import Dict, Any

genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyC2OHi_8f0J8nFvWUF0hFb81MwgD5A4xe0"))
model = genai.GenerativeModel('gemini-1.5-flash')

def save_debug_file(filename: str, content: str):
    """Save debug content to file"""
    os.makedirs('debug', exist_ok=True)
    with open(f'debug/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)

def generate_subjective_questions_gemini(
    text: str, 
    num_questions: int = 10, 
    answer_style: str = "all", 
    use_evaluator: bool = True
) -> Dict[int, Dict[str, Any]]:
    """
    Generate subjective questions using Gemini API
    """
    style_instructions = {
        "short": "Provide concise answers (1-2 sentences each)",
        "detailed": "Provide comprehensive answers (3-5 sentences each)",
        "all": "Mix of short and detailed answers as appropriate for each question"
    }
    
    style_instruction = style_instructions.get(answer_style, style_instructions["all"])
    
    prompt = f"""
    Based on the following text, generate {num_questions} thoughtful subjective questions that test understanding, analysis, and critical thinking. 
    
    Requirements:
    - Questions should cover different aspects of the content
    - Include a mix of: comprehension, analysis, evaluation, and application questions
    - {style_instruction}
    - Questions should be clear and well-structured
    - Avoid yes/no questions
    
    Format your response as JSON with the following structure:
    {{
        "questions": [
            {{
                "question": "Your question here?",
                "answer": "Detailed answer here",
                "type": "subjective",
                "difficulty": "easy|medium|hard"
            }}
        ]
    }}
    
    Text content:
    {text}
    """
    
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    
    save_debug_file('gemini_subjective_raw_response.txt', response_text)
    
    # Clean JSON formatting
    if response_text.startswith('```json'):
        response_text = response_text.replace('```json', '').replace('```', '').strip()
    elif response_text.startswith('```'):
        response_text = response_text.replace('```', '').strip()
    
    result = json.loads(response_text)
    questions_list = result.get('questions', [])
    
    # Format questions according to original API structure
    formatted_questions = {}
    for i, qa_data in enumerate(questions_list[:num_questions], 1):
        question = qa_data.get('question', f'Question {i}')
        answer = qa_data.get('answer', 'Answer')
        difficulty = qa_data.get('difficulty', 'medium')
        
        formatted_questions[i] = {
            "question": question,
            "answer": answer,
            "options": [],  # Empty for subjective questions
            "type": "subjective",
            "difficulty": difficulty
        }
    
    # Save debug information
    debug_content = f"Generated {len(formatted_questions)} subjective questions:\n"
    debug_content += f"Style: {answer_style}\n"
    debug_content += f"Use Evaluator: {use_evaluator}\n"
    debug_content += "=" * 50 + "\n"
    
    for i, q_data in formatted_questions.items():
        debug_content += f"Q{i} ({q_data.get('difficulty', 'N/A')}): {q_data['question']}\n"
        debug_content += f"A: {q_data['answer']}\n"
        debug_content += "-" * 30 + "\n"
        
    save_debug_file('gemini_subjective_processed.txt', debug_content)
    
    return formatted_questions

def test_subjective_questions():
    """Test function for subjective questions generation"""
    test_text = """
    Climate change refers to long-term shifts in global or regional climate patterns. It is primarily 
    attributed to human activities, particularly the emission of greenhouse gases from burning fossil fuels. 
    The effects include rising temperatures, melting ice caps, sea level rise, and extreme weather events. 
    Mitigation strategies include renewable energy adoption, carbon pricing, and international cooperation 
    through agreements like the Paris Climate Accord.
    """
    
    questions = generate_subjective_questions_gemini(
        text=test_text,
        num_questions=5,
        answer_style="detailed",
        use_evaluator=True
    )
    
    for i, q_data in questions.items():
        print(f"Q{i}: {q_data['question']}")
        print(f"A{i}: {q_data['answer']}\n")

if __name__ == "__main__":
    test_subjective_questions()