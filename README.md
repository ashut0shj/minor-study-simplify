# Study-Simplify

A comprehensive study material processing platform that transforms educational content into structured study materials through AI-powered transcription, summarization, and question generation.

## 🔗 Live Demo

- **Frontend**: [https://study-simplify-three.vercel.app/](https://study-simplify-three.vercel.app/)
- **API**: [https://minor-study-simplify.onrender.com](https://minor-study-simplify.onrender.com)

## Features

### Core Functionality
- **Multi-format File Processing**: Upload and process PDFs, PowerPoint presentations, and images
- **Intelligent Transcription**: Extract text content using OCR and document parsing
- **AI-Powered Summarization**: Generate concise summaries with keyword extraction
- **Question Generation**: Create both subjective and objective questions for study practice
- **Interactive Quiz Mode**: Take quizzes with generated multiple-choice questions

### Supported File Types
- PDF documents
- PowerPoint presentations (.pptx)
- Images (JPG, PNG, JPEG) with OCR processing

## Architecture

### Backend (FastAPI)
The backend API provides four main endpoints:

- `/transcribe` - Extract text from uploaded files
- `/summarize` - Generate summaries and extract keywords
- `/generate-subjective-questions` - Create open-ended questions
- `/generate-questions` - Generate multiple-choice questions

### Frontend (React)
The React application provides an intuitive interface with:

- **Upload Page**: Drag-and-drop file upload with progress tracking
- **Results Page**: Display transcribed text with action buttons
- **Summary Page**: Show generated summaries and important keywords
- **Question Pages**: Display subjective questions and interactive quiz interface

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **PyPDF2**: PDF text extraction
- **python-pptx**: PowerPoint processing
- **Tesseract OCR**: Image text recognition
- **Transformers**: T5 and BERT models for NLP tasks
- **scikit-learn**: TF-IDF and text processing
- **spaCy**: Named Entity Recognition

### Frontend
- **React**: Component-based UI framework
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Icon library

### AI/ML Models
- **T5 Transformer**: Question generation
- **BERT**: Question-answer evaluation
- **GloVe Embeddings**: Semantic similarity for distractor generation
- **TF-IDF**: Keyword extraction and text analysis

## Installation

### Backend Setup

1. Clone the repository:

2. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt

```

4. Install Tesseract OCR:
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`

5. Run the setup script to download models:
```bash
python setup.py
```

6. Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1.   In a new terminal navigate to the frontend directory:
```bash
cd study-simplify
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## API Documentation

### Endpoints

#### POST `/transcribe`
Upload and transcribe files to extract text content.

**Request**: Multipart form data with file
**Response**:
```json
{
  "success": true,
  "transcript": "extracted text content",
  "file_type": "application/pdf",
  "message": "File transcribed successfully"
}
```

#### POST `/summarize`
Generate summary and extract keywords from text.

**Request**:
```json
{
  "text": "input text to summarize"
}
```

**Response**:
```json
{
  "success": true,
  "important_words": ["keyword1", "keyword2"],
  "summary": "generated summary",
  "message": "Text summarized successfully"
}
```

#### POST `/generate-subjective-questions`
Create subjective/open-ended questions from text.

**Request**:
```json
{
  "text": "input text",
  "num_questions": 5,
  "answer_style": "all",
  "use_evaluator": true
}
```

#### POST `/generate-questions`
Generate objective/multiple-choice questions.

**Request**:
```json
{
  "text": "input text",
  "num_questions": 5,
  "num_options": 4
}
```

## Configuration

### Environment Variables
- `TESSDATA_PREFIX`: Path to Tesseract data directory
- `MODEL_CACHE_DIR`: Directory for caching downloaded models

### Model Configuration
The system automatically downloads required models on first run:
- T5-base model for question generation
- BERT model for QA evaluation
- GloVe embeddings for semantic similarity

## Development

### Project Structure
```
study-simplify/
├── main.py                 # FastAPI application
├── transcript.py           # File transcription module
├── summarize.py           # Text summarization
├── sub_q_gen/             # Subjective question generation
├── obj_q_gen/             # Objective question generation
├── setup.py               # Model setup and downloads
├── frontend/              # React application
└── debug/                 # Debug output files
```

### Adding New Features

1. **New File Types**: Extend the `transcript.py` module
2. **Custom Models**: Modify model loading in respective modules
3. **API Endpoints**: Add new routes in `main.py`
4. **Frontend Pages**: Create new components and routes

## Deployment

### Backend Deployment
The backend is deployed on Render with automatic deployments from the main branch.

### Frontend Deployment
The React application is deployed on Vercel with automatic deployments.

## Performance Considerations

- **Memory Usage**: ML models require significant RAM (2-4GB recommended)
- **Processing Time**: Large files may take several minutes to process
- **Model Caching**: Models are cached after first download to improve startup time

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs` endpoint
- Review debug files in the `debug/` directory for troubleshooting

## Acknowledgments

- Hugging Face Transformers for pre-trained models
- OpenAI for NLP research and methodologies
- FastAPI and React communities for excellent documentation