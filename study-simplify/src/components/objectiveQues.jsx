import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, FileText, HelpCircle, CheckCircle, Play, Trophy, RotateCcw } from 'lucide-react';

const ObjectiveQuestions = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { questions, total_questions, fileName } = location.state || {};

  const [gameMode, setGameMode] = useState('preview'); // 'preview', 'playing', 'results'
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  if (!questions || !fileName) {
    navigate('/');
    return null;
  }

  const questionsArray = Object.entries(questions).map(([key, q]) => ({
    id: key,
    ...q
  }));

  const startQuiz = () => {
    setGameMode('playing');
    setCurrentQuestion(0);
    setSelectedAnswers({});
    setShowResults(false);
  };

  const selectAnswer = (answer) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionsArray[currentQuestion].id]: answer
    }));
  };

  const nextQuestion = () => {
    if (currentQuestion < questionsArray.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    } else {
      finishQuiz();
    }
  };

  const previousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    }
  };

  const finishQuiz = () => {
    setGameMode('results');
    setShowResults(true);
  };

  const calculateScore = () => {
    let correct = 0;
    questionsArray.forEach(q => {
      if (selectedAnswers[q.id] === q.answer) {
        correct++;
      }
    });
    return correct;
  };

  const resetQuiz = () => {
    setGameMode('preview');
    setCurrentQuestion(0);
    setSelectedAnswers({});
    setShowResults(false);
  };

  const currentQ = questionsArray[currentQuestion];
  const score = calculateScore();
  const percentage = Math.round((score / questionsArray.length) * 100);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-blue-50">
      {/* Cat Paw Decorative Elements */}
      <div className="fixed top-16 right-24 opacity-15 text-purple-300 text-5xl rotate-45 pointer-events-none z-0">🐾</div>
      <div className="fixed bottom-32 left-12 opacity-15 text-blue-300 text-4xl -rotate-12 pointer-events-none z-0">🐾</div>
      <div className="fixed top-1/2 left-8 opacity-15 text-purple-400 text-4xl rotate-12 pointer-events-none z-0">🐾</div>
      <div className="fixed bottom-1/4 right-28 opacity-15 text-blue-400 text-4xl rotate-45 pointer-events-none z-0">🐾</div>
      <div className="fixed top-1/4 right-12 opacity-15 text-purple-500 text-5xl -rotate-30 pointer-events-none z-0">🐾</div>
      <div className="fixed top-3/4 left-20 opacity-15 text-blue-500 text-4xl rotate-60 pointer-events-none z-0">🐾</div>

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
              <HelpCircle className="w-3 h-3" />
              <span>Interactive Quiz</span>
            </div>
            <div className="flex items-center space-x-2 text-xs text-blue-600">
              <CheckCircle className="w-3 h-3" />
              <span>Total: {total_questions} questions</span>
            </div>
            {gameMode === 'playing' && (
              <div className="flex items-center space-x-2 text-xs text-green-600">
                <span>Progress: {currentQuestion + 1}/{questionsArray.length}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="px-8 py-8 max-w-6xl mx-auto relative z-10">
        
        {/* Preview Mode */}
        {gameMode === 'preview' && (
          <div className="text-center">
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-purple-200 p-8 mb-8">
              <div className="flex items-center justify-center space-x-2 mb-4">
                <Play className="w-8 h-8 text-blue-600" />
                <h2 className="text-2xl font-bold text-gray-800">Ready to Start Quiz?</h2>
              </div>
              <p className="text-gray-600 mb-6">
                Test your knowledge with {questionsArray.length} questions from your study material.
              </p>
              <button
                onClick={startQuiz}
                className="inline-flex items-center bg-gradient-to-r from-blue-600 to-purple-500 text-white px-8 py-3 rounded-lg font-medium hover:shadow-lg transition-all duration-200"
              >
                <Play className="w-4 h-4 mr-2" />
                Start Quiz
              </button>
            </div>

            {/* Preview Questions */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-700 mb-4">Question Preview:</h3>
              {questionsArray.slice(0, 3).map((q, index) => (
                <div key={q.id} className="bg-white/50 backdrop-blur-sm rounded-lg border border-purple-100 p-4 text-left">
                  <p className="font-medium text-gray-800">Q{index + 1}: {q.question}</p>
                  {q.options && q.options.length > 0 && (
                    <div className="mt-2 text-sm text-gray-600">
                      Options: {q.options.join(', ')}
                    </div>
                  )}
                </div>
              ))}
              {questionsArray.length > 3 && (
                <p className="text-gray-500 text-sm">...and {questionsArray.length - 3} more questions</p>
              )}
            </div>
          </div>
        )}

        {/* Playing Mode */}
        {gameMode === 'playing' && currentQ && (
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-purple-200 p-8">
            <div className="mb-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-800">
                  Question {currentQuestion + 1} of {questionsArray.length}
                </h2>
                <div className="bg-purple-100 px-3 py-1 rounded-full text-purple-700 text-sm font-medium">
                  Q{currentQ.id}
                </div>
              </div>
              
              {/* Progress Bar */}
              <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${((currentQuestion + 1) / questionsArray.length) * 100}%` }}
                ></div>
              </div>

              <h3 className="text-lg font-medium text-gray-800 mb-6">{currentQ.question}</h3>

              {/* Answer Options */}
              {currentQ.options && currentQ.options.length > 0 ? (
                <div className="space-y-3 mb-8">
                  {currentQ.options.map((option, idx) => (
                  <button
                    key={idx}
                    onClick={() => selectAnswer(option)}
                    className={`w-full text-left p-4 rounded-lg border transition-all duration-200 ${
                      selectedAnswers[currentQ.id] === option
                        ? 'border-purple-500 bg-purple-50 text-purple-900'
                        : 'border-gray-300 bg-white hover:border-purple-300'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full border-2 ${
                        selectedAnswers[currentQ.id] === option
                          ? 'border-purple-500 bg-purple-500'
                          : 'border-gray-400'
                      }`}>
                      </div>
                      <span className="font-medium">{option}</span>
                    </div>
                  </button>
                  ))}
                </div>
              ) : (
                <div className="mb-8">
                  <input
                    type="text"
                    value={selectedAnswers[currentQ.id] || ''}
                    onChange={(e) => selectAnswer(e.target.value)}
                    placeholder="Type your answer here..."
                    className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-purple-500 focus:outline-none"
                  />
                </div>
              )}

              {/* Navigation Buttons */}
              <div className="flex justify-between">
                <button
                  onClick={previousQuestion}
                  disabled={currentQuestion === 0}
                  className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-400 transition-colors"
                >
                  Previous
                </button>
                <button
                  onClick={nextQuestion}
                  disabled={!selectedAnswers[currentQ.id]}
                  className="px-8 py-2 bg-gradient-to-r from-blue-600 to-purple-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-md transition-all font-medium"
                >
                  {currentQuestion === questionsArray.length - 1 ? 'Submit Quiz' : 'Continue'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Results Mode */}
        {gameMode === 'results' && (
          <div className="space-y-6">
            {/* Score Card */}
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-purple-200 p-8 text-center">
              <div className="flex items-center justify-center space-x-2 mb-4">
                <Trophy className={`w-12 h-12 ${percentage >= 70 ? 'text-yellow-500' : percentage >= 50 ? 'text-gray-400' : 'text-red-400'}`} />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Quiz Results</h2>
              <div className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-500 bg-clip-text text-transparent mb-4">
                {score}/{questionsArray.length}
              </div>
              <p className="text-xl text-gray-600 mb-6">
                You scored {percentage}%
              </p>
              <div className="mb-6">
                {percentage >= 80 && (
                  <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-lg">
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Excellent performance
                  </div>
                )}
                {percentage >= 60 && percentage < 80 && (
                  <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-lg">
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Good job
                  </div>
                )}
                {percentage < 60 && (
                  <div className="inline-flex items-center px-4 py-2 bg-amber-100 text-amber-800 rounded-lg">
                    <HelpCircle className="w-4 h-4 mr-2" />
                    Room for improvement
                  </div>
                )}
              </div>
              <button
                onClick={resetQuiz}
                className="inline-flex items-center bg-gradient-to-r from-blue-600 to-purple-500 text-white px-6 py-2 rounded-lg font-medium hover:shadow-lg transition-all duration-200"
              >
                <RotateCcw className="w-4 h-4 mr-2" />
                Try Again
              </button>
            </div>

            {/* Detailed Results */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-800 flex items-center space-x-2">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span>Detailed Results</span>
              </h3>
              {questionsArray.map((q) => {
                const userAnswer = selectedAnswers[q.id];
                const isCorrect = userAnswer === q.answer;
                return (
                  <div key={q.id} className={`bg-white/70 backdrop-blur-sm rounded-xl border-2 p-6 ${
                    isCorrect ? 'border-green-200' : 'border-red-200'
                  }`}>
                    <div className="flex items-start justify-between mb-3">
                      <h4 className="font-semibold text-gray-800">Q{q.id}: {q.question}</h4>
                    <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                        isCorrect ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                      }`}>
                        {isCorrect ? 'Correct' : 'Incorrect'}
                      </div>
                    </div>
                    <div className="space-y-2 text-sm">
                      <p><span className="font-medium">Your answer:</span> <span className={isCorrect ? 'text-green-600' : 'text-red-600'}>{userAnswer || 'No answer'}</span></p>
                      <p><span className="font-medium">Correct answer:</span> <span className="text-green-600">{q.answer}</span></p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <span>Study-Simplify Quiz</span>
        </div>
      </main>
    </div>
  );
};

export default ObjectiveQuestions;