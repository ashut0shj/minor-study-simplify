from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from typing import Dict, Any
from transcript import Transcriber, runner
from offline import get_keywords
from sub_q_gen.questiongenerator import QuestionGenerator
from obj_q_gen.workers import text_to_questions

app = FastAPI(title="Study Material Processor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs('debug', exist_ok=True)

def save_debug_file(filename: str, content: str):
    with open(f'debug/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)

@app.get("/")
async def root():
    return {"message": "Study Material Processor API"}

@app.post("/transcribe")
async def transcribe_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "image/jpeg", "image/png", "image/jpg"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file.content_type} not supported. Supported: PDF, PPT, Images"
        )
    
    media_type = file.content_type.split("/")
    file_extension = media_type[1] if media_type[1] != "vnd.openxmlformats-officedocument.presentationml.presentation" else "pptx"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    transcriber = Transcriber(temp_file_path)
    transcript = runner(transcriber, media_type)
    
    if isinstance(transcript, list):
        transcript = ' '.join(transcript)
    
    save_debug_file('latest_transcript.txt', transcript)
    os.unlink(temp_file_path)
    
    return {
        "success": True,
        "transcript": transcript,
        "file_type": file.content_type,
        "message": "File transcribed successfully"
    }

@app.post("/summarize")
async def summarize_text(data: Dict[str, str]) -> Dict[str, Any]:
    text = data.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided for summarization")
    
    important_words, summary_paragraph = get_keywords(text, save_debug_files=True)
    
    return {
        "success": True,
        "important_words": important_words,
        "summary": summary_paragraph,
        "message": "Text summarized successfully"
    }

@app.post("/generate-subjective-questions")
async def generate_subjective_questions(data: Dict[str, Any]) -> Dict[str, Any]:
    text = data.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided for question generation")
    
    num_questions = data.get("num_questions", 10)
    answer_style = data.get("answer_style", "all")
    use_evaluator = data.get("use_evaluator", True)
    
    save_debug_file('subjective_input.txt', 
                   f"Questions: {num_questions}\nStyle: {answer_style}\nEvaluator: {use_evaluator}\n"
                   f"{'='*50}\n{text}")
    
    qg = QuestionGenerator()
    qa_list = qg.generate(
        article=text,
        use_evaluator=use_evaluator,
        num_questions=num_questions,
        answer_style=answer_style
    )
    
    formatted_questions = {}
    for i, qa_pair in enumerate(qa_list, 1):
        question = qa_pair['question']
        answer = qa_pair['answer']
        
        if isinstance(answer, list):
            options = [option['answer'] for option in answer]
            correct_answer = next((opt['answer'] for opt in answer if opt['correct']), options[0])
            
            formatted_questions[i] = {
                "question": question,
                "answer": correct_answer,
                "options": options,
                "type": "multiple_choice"
            }
        else:
            formatted_questions[i] = {
                "question": question,
                "answer": answer,
                "options": [],
                "type": "subjective"
            }
    
    debug_content = f"Generated {len(formatted_questions)} questions:\n{'='*50}\n"
    for i, q_data in formatted_questions.items():
        debug_content += f"Q{i} ({q_data['type']}): {q_data['question']}\nA: {q_data['answer']}\n"
        if q_data['options']:
            debug_content += f"Options: {q_data['options']}\n"
        debug_content += "-" * 30 + "\n"
    
    save_debug_file('subjective_questions.txt', debug_content)
    
    return {
        "success": True,
        "questions": formatted_questions,
        "total_questions": len(formatted_questions),
        "answer_style": answer_style,
        "used_evaluator": use_evaluator,
        "message": f"Generated {len(formatted_questions)} subjective questions"
    }

@app.post("/generate-questions")
async def generate_questions(data: Dict[str, Any]) -> Dict[str, Any]:
    text = data.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided for question generation")
    
    num_questions = data.get("num_questions", 5)
    num_options = data.get("num_options", 4)
    
    save_debug_file('objective_input.txt', 
                   f"Questions: {num_questions}\nOptions: {num_options}\n"
                   f"{'='*50}\n{text}")
    
    questions_dict = text_to_questions(text, num_questions, num_options)
    
    debug_content = f"Generated {len(questions_dict)} questions:\n{'='*50}\n"
    for i, q_data in questions_dict.items():
        debug_content += f"Q{i}: {q_data.get('question', 'N/A')}\n"
        debug_content += f"A: {q_data.get('answer', 'N/A')}\n"
        debug_content += f"Options: {q_data.get('options', [])}\n"
        debug_content += "-" * 30 + "\n"
    
    save_debug_file('objective_questions.txt', debug_content)
    
    return {
        "success": True,
        "questions": questions_dict,
        "total_questions": len(questions_dict),
        "message": f"Generated {len(questions_dict)} objective questions"
    }

@app.post("/process-complete")
async def process_complete(
    file: UploadFile = File(...), 
    num_questions: int = 5, 
    num_options: int = 4
) -> Dict[str, Any]:
    transcribe_result = await transcribe_file(file)
    transcript = transcribe_result["transcript"]
    
    summary_result = await summarize_text({"text": transcript})
    
    questions_result = await generate_questions({
        "text": transcript, 
        "num_questions": num_questions,
        "num_options": num_options
    })
    
    return {
        "success": True,
        "transcript": transcript,
        "important_words": summary_result["important_words"],
        "summary": summary_result["summary"],
        "questions": questions_result["questions"],
        "total_questions": questions_result["total_questions"],
        "file_type": transcribe_result["file_type"],
        "message": "Complete processing: transcribed, summarized, and questions generated"
    }

@app.post("/process-complete-subjective")
async def process_complete_subjective(
    file: UploadFile = File(...), 
    num_questions: int = 10, 
    answer_style: str = "all",
    use_evaluator: bool = True
) -> Dict[str, Any]:
    transcribe_result = await transcribe_file(file)
    transcript = transcribe_result["transcript"]
    
    summary_result = await summarize_text({"text": transcript})
    
    questions_result = await generate_subjective_questions({
        "text": transcript, 
        "num_questions": num_questions,
        "answer_style": answer_style,
        "use_evaluator": use_evaluator
    })
    
    return {
        "success": True,
        "transcript": transcript,
        "important_words": summary_result["important_words"],
        "summary": summary_result["summary"],
        "questions": questions_result["questions"],
        "total_questions": questions_result["total_questions"],
        "answer_style": answer_style,
        "used_evaluator": use_evaluator,
        "file_type": transcribe_result["file_type"],
        "message": "Complete subjective processing: transcribed, summarized, and questions generated"
    }

@app.post("/process")
async def process_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    transcribe_result = await transcribe_file(file)
    transcript = transcribe_result["transcript"]
    
    summary_result = await summarize_text({"text": transcript})
    
    return {
        "success": True,
        "transcript": transcript,
        "important_words": summary_result["important_words"],
        "summary": summary_result["summary"],
        "file_type": transcribe_result["file_type"],
        "message": "File processed and summarized successfully"
    }

@app.post("/test-subjective-questions")
async def test_subjective_questions():
    sample_text = """
    Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. 
    This process occurs in the chloroplasts of plant cells. Chloroplasts contain chlorophyll, which is the green pigment 
    that captures light energy. The light-dependent reactions occur in the thylakoids, while the light-independent 
    reactions (Calvin cycle) occur in the stroma. Photosynthesis is essential for life on Earth as it produces oxygen 
    and serves as the foundation of most food chains.
    """
    
    return await generate_subjective_questions({
        "text": sample_text,
        "num_questions": 5,
        "answer_style": "all",
        "use_evaluator": True
    })

@app.post("/test-objective-questions")
async def test_objective_questions():
    sample_text = """
    Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. 
    This process occurs in the chloroplasts of plant cells. Chloroplasts contain chlorophyll, which is the green pigment 
    that captures light energy. The light-dependent reactions occur in the thylakoids, while the light-independent 
    reactions (Calvin cycle) occur in the stroma. Photosynthesis is essential for life on Earth as it produces oxygen 
    and serves as the foundation of most food chains.
    """
    
    return await generate_questions({
        "text": sample_text,
        "num_questions": 3,
        "num_options": 4
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)