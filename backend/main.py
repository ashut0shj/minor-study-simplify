from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from typing import Dict, Any
from transcript import Transcriber, runner
# Import the new Gemini-based modules
from summarize import get_keywords_gemini
from subjective import generate_subjective_questions_gemini
from objective import generate_objective_questions_gemini

app = FastAPI(title="Study Material Processor", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        transcriber = Transcriber(temp_file_path)
        transcript = runner(transcriber, media_type)
        
        if isinstance(transcript, list):
            transcript = ' '.join(transcript)
        
        save_debug_file('latest_transcript.txt', transcript)
        
        return {
            "success": True,
            "transcript": transcript,
            "file_type": file.content_type,
            "message": "File transcribed successfully"
        }
    
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError as e:
                print(f"Warning: Could not delete temporary file {temp_file_path}: {e}")

@app.post("/summarize")
async def summarize_text(data: Dict[str, str]) -> Dict[str, Any]:
    text = data.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided for summarization")
    
    try:
        # Using Gemini API for summarization
        important_words, summary_paragraph = get_keywords_gemini(text, save_debug_files=True)
        
        return {
            "success": True,
            "important_words": important_words,
            "summary": summary_paragraph,
            "message": "Text summarized successfully using Gemini"
        }
    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error summarizing text: {str(e)}"
        )

@app.post("/generate-subjective-questions")
async def generate_subjective_questions(data: Dict[str, Any]) -> Dict[str, Any]:
    text = data.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided for question generation")
    
    num_questions = data.get("num_questions", 10)
    answer_style = data.get("answer_style", "all")
    use_evaluator = data.get("use_evaluator", True)
    
    try:
        save_debug_file('subjective_input.txt', 
                       f"Questions: {num_questions}\nStyle: {answer_style}\nEvaluator: {use_evaluator}\n"
                       f"{'='*50}\n{text}")
        
        # Using Gemini API for subjective question generation
        formatted_questions = generate_subjective_questions_gemini(
            text=text,
            num_questions=num_questions,
            answer_style=answer_style,
            use_evaluator=use_evaluator
        )
        
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
            "message": f"Generated {len(formatted_questions)} subjective questions using Gemini"
        }
    
    except Exception as e:
        print(f"Error generating subjective questions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating questions: {str(e)}"
        )

@app.post("/generate-questions")
async def generate_questions(data: Dict[str, Any]) -> Dict[str, Any]:
    text = data.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided for question generation")
    
    num_questions = data.get("num_questions", 5)
    num_options = data.get("num_options", 4)
    
    try:
        save_debug_file('objective_input.txt', 
                       f"Questions: {num_questions}\nOptions: {num_options}\n"
                       f"{'='*50}\n{text}")
        
        # Using Gemini API for objective question generation
        questions_dict = generate_objective_questions_gemini(text, num_questions, num_options)
        
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
            "message": f"Generated {len(questions_dict)} objective questions using Gemini"
        }
    
    except Exception as e:
        print(f"Error generating objective questions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating questions: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)