import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, FileText, BookOpen, MessageSquare } from 'lucide-react';

const SubjectiveQuestions = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { questions, total_questions, answer_style, fileName } = location.state || {};

  if (!questions || !fileName) {
    navigate('/');
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-blue-50">
      {/* Cat Paw Decorative Elements */}
      <div className="fixed top-16 right-24 opacity-15 text-purple-300 text-5xl rotate-45 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed bottom-32 left-12 opacity-15 text-blue-300 text-4xl -rotate-12 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-1/2 left-8 opacity-15 text-purple-400 text-4xl rotate-12 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed bottom-1/4 right-28 opacity-15 text-blue-400 text-4xl rotate-45 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-1/4 right-12 opacity-15 text-purple-500 text-5xl -rotate-30 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-3/4 left-20 opacity-15 text-blue-500 text-4xl rotate-60 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-1/3 left-1/3 opacity-15 text-purple-300 text-5xl rotate-12 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed bottom-1/2 right-1/4 opacity-15 text-blue-300 text-4xl -rotate-45 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-2/3 right-1/3 opacity-15 text-purple-400 text-4xl rotate-30 pointer-events-none z-0">
        🐾
      </div>

      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-purple-200 sticky top-0 z-50">
        <div className="px-6 py-3 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold text-sm relative">
              S
              <div className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-purple-400 rounded-full"></div>
              <div className="absolute -top-0.5 -left-0.5 w-2 h-2 bg-blue-400 rounded-full"></div>
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-500 bg-clip-text text-transparent">
              Study-Simplify
            </h1>
          </div>
          <button 
            onClick={() => navigate('/results', { 
              state: { 
                transcript: location.state.transcript, 
                fileName,
                ...location.state 
              } 
            })}
            className="flex items-center space-x-2 text-gray-600 hover:text-purple-600 transition-colors text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Results</span>
          </button>
        </div>
      </header>

      {/* File Info Bar */}
      <div className="bg-white/60 backdrop-blur-sm border-b border-purple-200">
        <div className="px-6 py-3">
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <FileText className="w-4 h-4 text-purple-600" />
              <span className="text-sm font-medium text-gray-800">{fileName}</span>
            </div>
            <div className="flex items-center space-x-2 text-xs text-purple-600">
              <BookOpen className="w-3 h-3" />
              <span>Subjective Questions</span>
            </div>
            <div className="flex items-center space-x-2 text-xs text-blue-600">
              <MessageSquare className="w-3 h-3" />
              <span>Total: {total_questions} questions</span>
            </div>
            <div className="flex items-center space-x-2 text-xs text-green-600">
              <span>Style: {answer_style}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="px-8 py-8 max-w-7xl mx-auto relative z-10">
        {/* Questions Section */}
        <div className="mb-8">
          <div className="flex items-center space-x-2 mb-6">
            <BookOpen className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-semibold text-gray-800">Subjective Questions</h2>
          </div>
          
          <div className="space-y-6">
            {Object.entries(questions).map(([key, q]) => (
              <div 
                key={key}
                className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-purple-200 p-6"
              >
                <h4 className="text-lg font-semibold text-gray-800 mb-4">
                  Q{key}: {q.question}
                </h4>
                
                <div className="mb-4">
                  <h5 className="font-medium text-gray-700 mb-3 flex items-center space-x-2">
                    <MessageSquare className="w-4 h-4 text-green-600" />
                    <span>Answer:</span>
                  </h5>
                  {/* <div className="bg-green-50 border border-green-200 rounded-lg p-4"> */}
                    <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{q.answer}</p>
                  {/* </div> */}
                </div>
                
                {q.options && q.options.length > 0 && (
                  <div>
                    <h5 className="font-medium text-gray-700 mb-3">Reference Points:</h5>
                    <div className="space-y-2">
                      {q.options.map((option, idx) => (
                        <div 
                          key={idx}
                          className="flex items-start space-x-3 text-gray-600 bg-blue-50 border border-blue-200 rounded-lg p-3"
                        >
                          <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-sm leading-relaxed">{option}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <span>Study-Simplify Questions</span>
        </div>
      </main>
    </div>
  );
};

export default SubjectiveQuestions;