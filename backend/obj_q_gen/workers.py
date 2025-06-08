from question_generation_main import QuestionGeneration
from typing import Dict, List, Any

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
    try:
        # Generate questions using your existing system
        qGen = QuestionGeneration(num_questions, num_options)
        questions_dict = qGen.generate_questions_dict(text_content)
        
        # Format the options from dict to list
        formatted_questions = {}
        for i in range(1, len(questions_dict) + 1):
            if i in questions_dict:
                # Convert options dict to list
                options_list = []
                for j in range(1, num_options + 1):
                    if j in questions_dict[i]['options']:
                        options_list.append(questions_dict[i]['options'][j])
                
                formatted_questions[i] = {
                    "question": questions_dict[i]['question'],
                    "answer": questions_dict[i]['answer'],
                    "options": options_list
                }
        
        return formatted_questions
        
    except Exception as e:
        raise Exception(f"Error in question generation: {str(e)}")

def questions_to_csv_format(questions_dict: Dict[int, Dict[str, Any]]) -> List[str]:
    """
    Convert questions dict to CSV-like format for export
    
    Returns:
        List of strings in format: "question,answer,choice1,choice2,choice3,choice4"
    """
    csv_lines = ["question,answer,choice1,choice2,choice3,choice4"]
    
    for question_num, question_data in questions_dict.items():
        line = f"{question_data['question']},{question_data['answer']}"
        
        # Add options
        for option in question_data['options']:
            line += f",{option}"
        
        # Pad with empty options if needed
        while line.count(',') < 5:  # question + answer + 4 options = 5 commas
            line += ","
            
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