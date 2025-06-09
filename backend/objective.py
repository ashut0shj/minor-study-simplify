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

def generate_objective_questions_gemini(
    text: str, 
    num_questions: int = 5, 
    num_options: int = 4
) -> Dict[int, Dict[str, Any]]:
    """
    Generate objective (multiple choice) questions using Gemini API
    """
    prompt = f"""
    Based on the following text, generate {num_questions} multiple choice questions. Each question should have {num_options} options with only one correct answer.
    
    Requirements:
    - Questions should test factual knowledge and comprehension
    - Options should be plausible but only one should be correct
    - Avoid obvious or trick questions
    - Cover different parts of the content
    - Make incorrect options reasonable but clearly wrong
    
    Format your response as JSON with the following structure:
    {{
        "questions": [
            {{
                "question": "Your question here?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "explanation": "Brief explanation of why this is correct"
            }}
        ]
    }}
    
    Text content:
    {text}
    """
    
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    
    save_debug_file('gemini_objective_raw_response.txt', response_text)
    
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
        options = qa_data.get('options', [])
        correct_answer = qa_data.get('correct_answer', '')
        explanation = qa_data.get('explanation', '')
        
        # Ensure we have the right number of options
        while len(options) < num_options:
            options.append(f"Option {len(options) + 1}")
        options = options[:num_options]
        
        # If correct_answer is not in options, use the first option
        if correct_answer not in options and options:
            correct_answer = options[0]
        
        formatted_questions[i] = {
            "question": question,
            "options": options,
            "answer": correct_answer,
            "explanation": explanation
        }
    
    # Save debug information
    debug_content = f"Generated {len(formatted_questions)} objective questions:\n"
    debug_content += f"Options per question: {num_options}\n"
    debug_content += "=" * 50 + "\n"
    
    for i, q_data in formatted_questions.items():
        debug_content += f"Q{i}: {q_data['question']}\n"
        debug_content += f"Options: {q_data['options']}\n"
        debug_content += f"Correct: {q_data['answer']}\n"
        if q_data.get('explanation'):
            debug_content += f"Explanation: {q_data['explanation']}\n"
        debug_content += "-" * 30 + "\n"
        
    save_debug_file('gemini_objective_processed.txt', debug_content)
    
    return formatted_questions

def test_objective_questions():
    """Test function for objective questions generation"""
    test_text = """
    The water cycle is a continuous process that describes the movement of water on, above, and below 
    the surface of the Earth. The main processes include evaporation, condensation, precipitation, and 
    collection. Water evaporates from oceans, lakes, and rivers, rises into the atmosphere, condenses 
    into clouds, and falls back to Earth as precipitation in the form of rain, snow, or hail.
    """
    
    questions = generate_objective_questions_gemini(
        text=test_text,
        num_questions=3,
        num_options=4
    )
    
    for i, q_data in questions.items():
        print(f"Q{i}: {q_data['question']}")
        for j, option in enumerate(q_data['options'], 1):
            marker = "✓" if option == q_data['answer'] else " "
            print(f"  {j}) {option} {marker}")
        print(f"Correct: {q_data['answer']}\n")

if __name__ == "__main__":
    test_objective_questions()