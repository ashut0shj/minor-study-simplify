import sys
import os
from typing import Dict, List, Any
import traceback

# Add the current directory to path to help with imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Try different import methods
try:
    from obj_q_gen.question_generation_main import QuestionGeneration
    print("Successfully imported QuestionGeneration from obj_q_gen")
except ImportError:
    try:
        from question_generation_main import QuestionGeneration
        print("Successfully imported QuestionGeneration directly")
    except ImportError as e:
        print(f"Failed to import QuestionGeneration: {e}")
        QuestionGeneration = None

def text_to_questions(text_content: str, num_questions: int = 5, num_options: int = 4) -> Dict[int, Dict[str, Any]]:
    """
    Convert text to questions with options
    
    Args:
        text_content: The input text to generate questions from
        num_questions: Number of questions to generate (default: 5)
        num_options: Number of options per question (default: 4)
    
    Returns:
        Dict with question data in format:
        {
            1: {
                "question": "Question text with blanks",
                "answer": "Correct answer",
                "options": ["option1", "option2", "option3", "option4"]
            },
            ...
        }
    """
    if QuestionGeneration is None:
        raise Exception("QuestionGeneration class not available - import failed")
        
    if not text_content or not text_content.strip():
        raise Exception("Empty text provided for question generation")
    
    try:
        print(f"Starting question generation with {num_questions} questions, {num_options} options each")
        print(f"Text length: {len(text_content)} characters")
        
        # Generate questions using your existing system
        qGen = QuestionGeneration(num_questions, num_options)
        questions_dict = qGen.generate_questions_dict(text_content)
        
        print(f"Raw questions_dict keys: {list(questions_dict.keys())}")
        print(f"Raw questions_dict length: {len(questions_dict)}")
        
        # Debug: Print the raw questions dict structure
        for i, (key, value) in enumerate(questions_dict.items()):
            if i < 2:  # Print first 2 for debugging
                print(f"Question {key}: {type(value)} - {list(value.keys()) if isinstance(value, dict) else value}")
        
        # Format the options from dict to list
        formatted_questions = {}
        for i in range(1, len(questions_dict) + 1):
            if i in questions_dict:
                question_data = questions_dict[i]
                
                # Ensure we have the required fields
                if 'question' not in question_data or 'answer' not in question_data:
                    print(f"Warning: Question {i} missing required fields")
                    continue
                
                # Convert options dict to list
                options_list = []
                if 'options' in question_data and isinstance(question_data['options'], dict):
                    for j in range(1, num_options + 1):
                        if j in question_data['options']:
                            options_list.append(question_data['options'][j])
                elif 'options' in question_data and isinstance(question_data['options'], list):
                    options_list = question_data['options'][:num_options]
                else:
                    print(f"Warning: Question {i} has no valid options")
                    # Create dummy options as fallback
                    options_list = [f"Option {j}" for j in range(1, num_options + 1)]
                
                formatted_questions[i] = {
                    "question": question_data['question'],
                    "answer": question_data['answer'],
                    "options": options_list
                }
        
        print(f"Successfully formatted {len(formatted_questions)} questions")
        return formatted_questions
        
    except Exception as e:
        print(f"Error in text_to_questions: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise Exception(f"Error in question generation: {str(e)}")

def questions_to_csv_format(questions_dict: Dict[int, Dict[str, Any]]) -> List[str]:
    """
    Convert questions dict to CSV-like format for export
    
    Returns:
        List of strings in format: "question,answer,choice1,choice2,choice3,choice4"
    """
    csv_lines = ["question,answer,choice1,choice2,choice3,choice4"]
    
    for question_num, question_data in questions_dict.items():
        # Escape commas in the text
        question_text = question_data['question'].replace(',', ';')
        answer_text = question_data['answer'].replace(',', ';')
        
        line = f'"{question_text}","{answer_text}"'
        
        # Add options
        for option in question_data['options']:
            option_text = option.replace(',', ';')
            line += f',"{option_text}"'
        
        # Pad with empty options if needed
        while line.count(',') < 5:  # question + answer + 4 options = 5 commas
            line += '""'
            
        csv_lines.append(line)
    
    return csv_lines

def save_questions_to_file(questions_dict: Dict[int, Dict[str, Any]], filepath: str = "questions.csv"):
    """
    Save questions to a CSV file (optional - for backward compatibility)
    """
    csv_lines = questions_to_csv_format(questions_dict)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        for line in csv_lines:
            file.write(line + '\n')
    
    return filepath

def test_question_generation():
    """
    Test function to verify question generation works
    """
    sample_text = """
    Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. 
    This process occurs in the chloroplasts of plant cells. Chloroplasts contain chlorophyll, which is the green pigment 
    that captures light energy. The light-dependent reactions occur in the thylakoids, while the light-independent 
    reactions (Calvin cycle) occur in the stroma. Photosynthesis is essential for life on Earth as it produces oxygen 
    and serves as the foundation of most food chains.
    """
    
    try:
        questions = text_to_questions(sample_text, 3, 4)
        print("Test successful!")
        print(f"Generated {len(questions)} questions:")
        for i, q_data in questions.items():
            print(f"\nQuestion {i}:")
            print(f"Q: {q_data['question']}")
            print(f"A: {q_data['answer']}")
            print(f"Options: {q_data['options']}")
        return questions
    except Exception as e:
        print(f"Test failed: {e}")
        return None

if __name__ == "__main__":
    test_question_generation()