from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from typing import Dict, Any
import traceback
from transcript import Transcriber, runner
from offline import get_keywords

# Import the workers function instead of direct class import
try:
    from workers import text_to_questions
    print("Successfully imported text_to_questions from workers")
except ImportError as e:
    print(f"Failed to import from workers: {e}")
    # Fallback to direct import
    try:
        from obj_q_gen.question_generation_main import QuestionGeneration
        print("Successfully imported QuestionGeneration from obj_q_gen")
    except ImportError as e2:
        print(f"Failed to import QuestionGeneration: {e2}")
        # Try without obj_q_gen prefix
        try:
            from question_generation_main import QuestionGeneration
            print("Successfully imported QuestionGeneration directly")
        except ImportError as e3:
            print(f"All imports failed: {e3}")

app = FastAPI(title="Study Material Processor", version="1.0.0")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Study Material Processor API"}

@app.post("/transcribe")
async def transcribe_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Transcribe uploaded file (PDF, PPT, or Image) to text
    """
    try:
        # Check file type
        content_type = file.content_type
        if not content_type:
            raise HTTPException(status_code=400, detail="Could not determine file type")
        
        media_type = content_type.split("/")
        
        # Only allow PDF, PPT, and Image files for now
        allowed_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "image/jpeg",
            "image/png",
            "image/jpg"
        ]
        
        if content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {content_type} not supported. Supported: PDF, PPT, Images"
            )
        
        # Create temporary file
        file_extension = media_type[1] if media_type[1] != "vnd.openxmlformats-officedocument.presentationml.presentation" else "pptx"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Process with your existing transcriber
        transcriber = Transcriber(temp_file_path)
        transcript = runner(transcriber, media_type)
        
        # Convert list to string if needed (for PPT)
        if isinstance(transcript, list):
            transcript = ' '.join(transcript)
        
        # Save transcribed text to debug file for inspection
        try:
            os.makedirs('debug', exist_ok=True)
            with open('debug/latest_transcript.txt', 'w+', encoding='utf-8') as debug_file:
                debug_file.write(transcript)
        except Exception as e:
            print(f"Warning: Could not save debug transcript: {e}")
        
        return {
            "success": True,
            "transcript": transcript,
            "file_type": content_type,
            "message": "File transcribed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/summarize")
async def summarize_text(data: Dict[str, str]) -> Dict[str, Any]:
    """
    Summarize provided text using your existing offline logic
    """
    try:
        text = data.get("text", "")
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text provided for summarization")
        
        # Use your existing get_keywords function with debug file saving enabled
        important_words, summary_paragraph = get_keywords(text, save_debug_files=True)
        
        return {
            "success": True,
            "important_words": important_words,
            "summary": summary_paragraph,
            "message": "Text summarized successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing text: {str(e)}")

@app.post("/generate-questions")
async def generate_questions(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate questions from provided text
    """
    try:
        text = data.get("text", "")
        num_questions = data.get("num_questions", 5)
        num_options = data.get("num_options", 4)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text provided for question generation")
        
        print(f"Generating {num_questions} questions with {num_options} options each")
        print(f"Text length: {len(text)} characters")
        
        # Save text used for question generation to debug file
        try:
            os.makedirs('debug', exist_ok=True)
            with open('debug/question_input.txt', 'w+', encoding='utf-8') as debug_file:
                debug_file.write(f"Text length: {len(text)}\n")
                debug_file.write(f"Num questions: {num_questions}\n")
                debug_file.write(f"Num options: {num_options}\n")
                debug_file.write("="*50 + "\n")
                debug_file.write(text)
        except Exception as e:
            print(f"Warning: Could not save question debug file: {e}")
        
        # Try to use workers function first
        try:
            if 'text_to_questions' in globals():
                print("Using workers.text_to_questions function")
                questions_dict = text_to_questions(text, num_questions, num_options)
            else:
                raise NameError("text_to_questions not available")
        except Exception as worker_error:
            print(f"Workers function failed: {worker_error}")
            print("Falling back to direct QuestionGeneration class")
            
            # Fallback to direct class usage
            if 'QuestionGeneration' in globals():
                qGen = QuestionGeneration(num_questions, num_options)
                questions_dict = qGen.generate_questions_dict(text)
                
                # Format options properly (convert from dict to list)
                formatted_questions = {}
                for i in range(1, len(questions_dict) + 1):
                    if i in questions_dict:
                        options_list = []
                        if 'options' in questions_dict[i]:
                            for j in range(1, num_options + 1):
                                if j in questions_dict[i]['options']:
                                    options_list.append(questions_dict[i]['options'][j])
                        
                        formatted_questions[i] = {
                            "question": questions_dict[i]['question'],
                            "answer": questions_dict[i]['answer'],
                            "options": options_list
                        }
                questions_dict = formatted_questions
            else:
                raise HTTPException(status_code=500, detail="Question generation system not available")
        
        # Debug: Save generated questions
        try:
            with open('debug/generated_questions.txt', 'w+', encoding='utf-8') as debug_file:
                debug_file.write(f"Generated {len(questions_dict)} questions:\n")
                debug_file.write("="*50 + "\n")
                for i, q_data in questions_dict.items():
                    debug_file.write(f"Question {i}:\n")
                    debug_file.write(f"Q: {q_data.get('question', 'N/A')}\n")
                    debug_file.write(f"A: {q_data.get('answer', 'N/A')}\n")
                    debug_file.write(f"Options: {q_data.get('options', [])}\n")
                    debug_file.write("-"*30 + "\n")
        except Exception as e:
            print(f"Warning: Could not save generated questions debug file: {e}")
        
        print(f"Successfully generated {len(questions_dict)} questions")
        
        return {
            "success": True,
            "questions": questions_dict,
            "total_questions": len(questions_dict),
            "message": f"Questions generated successfully ({len(questions_dict)} questions)"
        }
        
    except Exception as e:
        print(f"Error in generate_questions: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")

@app.post("/process-complete")
async def process_complete(file: UploadFile = File(...), num_questions: int = 5, num_options: int = 4) -> Dict[str, Any]:
    """
    Complete pipeline: Transcribe file, summarize it, and generate questions
    """
    try:
        # First transcribe
        transcribe_result = await transcribe_file(file)
        transcript = transcribe_result["transcript"]
        
        # Then summarize
        summary_result = await summarize_text({"text": transcript})
        
        # Then generate questions
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
            "message": "File completely processed: transcribed, summarized, and questions generated"
        }
        
    except Exception as e:
        print(f"Error in process_complete: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error in complete processing: {str(e)}")

@app.post("/process")
async def process_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Complete pipeline: Transcribe file and then summarize it
    """
    try:
        # First transcribe
        transcribe_result = await transcribe_file(file)
        transcript = transcribe_result["transcript"]
        
        # Then summarize
        summary_result = await summarize_text({"text": transcript})
        
        return {
            "success": True,
            "transcript": transcript,
            "important_words": summary_result["important_words"],
            "summary": summary_result["summary"],
            "file_type": transcribe_result["file_type"],
            "message": "File processed and summarized successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in complete processing: {str(e)}")

# Add a test endpoint to debug question generation
@app.post("/test-questions")
async def test_question_generation():
    """
    Test question generation with sample text
    """
    sample_text = """
    Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. 
    This process occurs in the chloroplasts of plant cells. Chloroplasts contain chlorophyll, which is the green pigment 
    that captures light energy. The light-dependent reactions occur in the thylakoids, while the light-independent 
    reactions (Calvin cycle) occur in the stroma. Photosynthesis is essential for life on Earth as it produces oxygen 
    and serves as the foundation of most food chains.
    """
    
    try:
        result = await generate_questions({
            "text": sample_text,
            "num_questions": 3,
            "num_options": 4
        })
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)