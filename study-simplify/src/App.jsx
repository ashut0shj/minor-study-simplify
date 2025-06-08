import React, { useState } from 'react';
import Home from './components/home';
import Results from './components/trans';
import Summary from './components/summary';
import ObjectiveQuestions from './components/ObjectiveQuestions';
import SubjectiveQuestions from './components/SubjectiveQuestions';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [transcript, setTranscript] = useState('');
  const [fileName, setFileName] = useState('');
  const [summaryData, setSummaryData] = useState(null);
  const [objectiveQuestions, setObjectiveQuestions] = useState(null);
  const [subjectiveQuestions, setSubjectiveQuestions] = useState(null);

  const handleFileProcessed = (transcriptText, file) => {
    setTranscript(transcriptText);
    setFileName(file);
    setCurrentPage('results');
  };

  const handleSummaryGenerated = (summary) => {
    setSummaryData(summary);
    setCurrentPage('summary');
  };

  const handleObjectiveQuestionsGenerated = (questions) => {
    setObjectiveQuestions(questions);
    setCurrentPage('objective-questions');
  };

  const handleSubjectiveQuestionsGenerated = (questions) => {
    setSubjectiveQuestions(questions);
    setCurrentPage('subjective-questions');
  };

  const handleBackToResults = () => {
    setCurrentPage('results');
  };

  const handleBackToHome = () => {
    setCurrentPage('home');
    setTranscript('');
    setFileName('');
    setSummaryData(null);
    setObjectiveQuestions(null);
    setSubjectiveQuestions(null);
  };

  return (
    <div>
      {currentPage === 'home' && (
        <Home onFileProcessed={handleFileProcessed} />
      )}
      
      {currentPage === 'results' && (
        <Results 
          transcript={transcript}
          fileName={fileName}
          onBack={handleBackToHome}
          onSummaryGenerated={handleSummaryGenerated}
          onObjectiveQuestionsGenerated={handleObjectiveQuestionsGenerated}
          onSubjectiveQuestionsGenerated={handleSubjectiveQuestionsGenerated}
        />
      )}

      {currentPage === 'summary' && (
        <Summary 
          summaryData={summaryData}
          fileName={fileName}
          onBack={handleBackToResults}
        />
      )}

      {currentPage === 'objective-questions' && (
        <ObjectiveQuestions 
          questions={objectiveQuestions}
          fileName={fileName}
          onBack={handleBackToResults}
        />
      )}

      {currentPage === 'subjective-questions' && (
        <SubjectiveQuestions 
          questions={subjectiveQuestions}
          fileName={fileName}
          onBack={handleBackToResults}
        />
      )}
    </div>
  );
}

export default App;