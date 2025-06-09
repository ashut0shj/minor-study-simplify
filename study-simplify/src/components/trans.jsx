import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, FileText, Brain, HelpCircle, PenTool, Hash, Clock, Settings } from 'lucide-react';

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { transcript, fileName } = location.state || {};
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [isGeneratingObjective, setIsGeneratingObjective] = useState(false);
  const [isGeneratingSubjective, setIsGeneratingSubjective] = useState(false);
  const [error, setError] = useState('');
  const [showObjectiveSettings, setShowObjectiveSettings] = useState(false);
  const [showSubjectiveSettings, setShowSubjectiveSettings] = useState(false);
  const [objectiveQuestions, setObjectiveQuestions] = useState(5);
  const [subjectiveQuestions, setSubjectiveQuestions] = useState(5);

  if (!transcript || !fileName) {
    navigate('/');
    return null;
  }

  // Calculate file stats
  const wordCount = transcript.trim().split(/\s+/).length;
  const charCount = transcript.length;

  const handleSummarize = async () => {
    setIsSummarizing(true);
    setError('');
  
    try {
      const response = await fetch('https://minor-study-simplify.onrender.com/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: transcript }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      
      if (data.success) {
        navigate('/summary', { 
          state: { 
            important_words: data.important_words,
            summary: data.summary,
            fileName,
            transcript: transcript
          } 
        });
      } else {
        setError('Failed to generate summary');
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setIsSummarizing(false);
    }
  };

  const handleGenerateObjective = async () => {
    setIsGeneratingObjective(true);
    setError('');
    setShowObjectiveSettings(false);
  
    try {
      const response = await fetch('https://minor-study-simplify.onrender.com/generate-questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: transcript,
          num_questions: objectiveQuestions,
          num_options: 4
        }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      
      if (data.success) {
        navigate('/objective-questions', { 
          state: { 
            questions: data.questions,
            total_questions: data.total_questions,
            fileName,
            transcript: transcript
          } 
        });
      } else {
        setError('Failed to generate questions');
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setIsGeneratingObjective(false);
    }
  };

  const handleGenerateSubjective = async () => {
    setIsGeneratingSubjective(true);
    setError('');
    setShowSubjectiveSettings(false);
  
    try {
      const response = await fetch('https://minor-study-simplify.onrender.com/generate-subjective-questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: transcript,
          num_questions: subjectiveQuestions,
          answer_style: "all",
          use_evaluator: true
        }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      
      if (data.success) {
        navigate('/subjective-questions', { 
          state: { 
            questions: data.questions,
            total_questions: data.total_questions,
            answer_style: data.answer_style,
            fileName,
            transcript: transcript
          } 
        });
      } else {
        setError('Failed to generate questions');
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setIsGeneratingSubjective(false);
    }
  };

  // Cat-themed loading component
  const CatLoader = ({ text }) => (
    <div className="flex items-center space-x-2">
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>
      <span className="text-sm">{text}</span>
    </div>
  );

  // Question Settings Modal Component
  const QuestionSettings = ({ 
    isOpen, 
    onClose, 
    type, 
    questionCount, 
    setQuestionCount, 
    onGenerate, 
    isGenerating 
  }) => {
    if (!isOpen) return null;

    return (
      <div className="fixed inset-0 bg-black/20 backdrop-blur-sm z-50 flex items-center justify-center">
        <div className="bg-white rounded-xl shadow-xl border border-purple-200 p-6 m-4 w-full max-w-md">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            {type === 'objective' ? 'Objective Questions' : 'Subjective Questions'} Settings
          </h3>
          
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of questions (1-10)
            </label>
            <input
              type="number"
              min="1"
              max="10"
              value={questionCount}
              onChange={(e) => setQuestionCount(Math.min(10, Math.max(1, parseInt(e.target.value) || 1)))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          <div className="flex space-x-3">
            <button
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={onGenerate}
              disabled={isGenerating}
              className={`flex-1 px-4 py-2 rounded-lg text-white font-medium transition-all ${
                isGenerating
                  ? 'bg-gray-400 cursor-not-allowed'
                  : type === 'objective'
                  ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 hover:shadow-md'
                  : 'bg-gradient-to-r from-purple-600 to-purple-700 hover:shadow-md'
              }`}
            >
              {isGenerating ? 'Generating...' : 'Generate'}
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-blue-50">
      {/* Cat Paw Decorative Elements */}
      <div className="fixed top-20 right-20 opacity-5 text-purple-300 text-4xl rotate-45 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed bottom-40 left-16 opacity-5 text-blue-300 text-3xl -rotate-12 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-1/2 left-10 opacity-5 text-purple-400 text-2xl rotate-12 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed bottom-1/3 right-32 opacity-5 text-blue-400 text-3xl rotate-45 pointer-events-none z-0">
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
            onClick={() => navigate('/')}
            className="flex items-center space-x-2 text-gray-600 hover:text-purple-600 transition-colors text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back</span>
          </button>
        </div>
      </header>

      {/* File Info Bar */}
      <div className="bg-white/60 backdrop-blur-sm border-b border-purple-200">
        <div className="px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <FileText className="w-4 h-4 text-purple-600" />
                <span className="text-sm font-medium text-gray-800">{fileName}</span>
              </div>
              <div className="flex items-center space-x-4 text-xs text-gray-600">
                <div className="flex items-center space-x-1">
                  <Hash className="w-3 h-3" />
                  <span>{wordCount.toLocaleString()} words</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Clock className="w-3 h-3" />
                  <span>{charCount.toLocaleString()} chars</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Floating Action Panel */}
      <div className="fixed top-1/2 right-8 transform -translate-y-1/2 z-40">
        <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg border border-purple-200 p-4 space-y-3 min-w-[300px]">
          <h3 className="text-sm font-semibold text-gray-700 text-center mb-4">Study Tools</h3>
          
          {/* Summary Button */}
          <button
            onClick={handleSummarize}
            disabled={isSummarizing}
            className={`w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
              isSummarizing
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-blue-700 text-white hover:shadow-lg hover:scale-105'
            }`}
          >
            {isSummarizing ? (
              <CatLoader text="Summarizing" />
            ) : (
              <>
                <Brain className="w-4 h-4" />
                <span>Generate Summary</span>
              </>
            )}
          </button>

          {/* Subjective Questions Button */}
          <button
            onClick={() => setShowSubjectiveSettings(true)}
            disabled={isGeneratingSubjective}
            className={`w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
              isGeneratingSubjective
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-purple-600 to-purple-700 text-white hover:shadow-lg hover:scale-105'
            }`}
          >
            {isGeneratingSubjective ? (
              <CatLoader text="Creating" />
            ) : (
              <>
                <PenTool className="w-4 h-4" />
                <span>Subjective Q's</span>
                <Settings className="w-3 h-3 ml-1" />
              </>
            )}
          </button>

          {/* Objective Questions Button */}
          <button
            onClick={() => setShowObjectiveSettings(true)}
            disabled={isGeneratingObjective}
            className={`w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
              isGeneratingObjective
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white hover:shadow-lg hover:scale-105'
            }`}
          >
            {isGeneratingObjective ? (
              <CatLoader text="Generating" />
            ) : (
              <>
                <HelpCircle className="w-4 h-4" />
                <span>Objective Q's</span>
                <Settings className="w-3 h-3 ml-1" />
              </>
            )}
          </button>

          {/* Question count indicators */}
          <div className="text-xs text-gray-500 text-center space-y-1 pt-2 border-t border-gray-200">
            <div>Subjective: {subjectiveQuestions} questions</div>
            <div>Objective: {objectiveQuestions} questions</div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="fixed bottom-8 left-8 right-8 max-w-md mx-auto z-50">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 shadow-lg">
            <div className="text-red-700 text-sm">{error}</div>
          </div>
        </div>
      )}

      {/* Main Content - Full Width Transcript */}
      <main className="px-8 py-8 pr-64 relative z-10">
        <p className="text-gray-800 text-base leading-7 whitespace-pre-wrap">
          {transcript}
        </p>
      </main>

      {/* Question Settings Modals */}
      <QuestionSettings
        isOpen={showObjectiveSettings}
        onClose={() => setShowObjectiveSettings(false)}
        type="objective"
        questionCount={objectiveQuestions}
        setQuestionCount={setObjectiveQuestions}
        onGenerate={handleGenerateObjective}
        isGenerating={isGeneratingObjective}
      />

      <QuestionSettings
        isOpen={showSubjectiveSettings}
        onClose={() => setShowSubjectiveSettings(false)}
        type="subjective"
        questionCount={subjectiveQuestions}
        setQuestionCount={setSubjectiveQuestions}
        onGenerate={handleGenerateSubjective}
        isGenerating={isGeneratingSubjective}
      />
    </div>
  );
};

export default Results;