from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from typing import Dict, Any
from transcript import Transcriber, runner
from backend.offline import get_keywords

app = FastAPI(title="Study Material Processor", version="1.0.0")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
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
        
        # Use your existing get_keywords function
        important_words, summary_paragraph = get_keywords(text)
        
        return {
            "success": True,
            "important_words": important_words,
            "summary": summary_paragraph,
            "message": "Text summarized successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing text: {str(e)}")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)