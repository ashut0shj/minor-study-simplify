import React, { useState } from 'react';
import Home from './components/home';
import Results from './components/trans';
import Summary from './components/summary';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [transcript, setTranscript] = useState('');
  const [fileName, setFileName] = useState('');
  const [summaryData, setSummaryData] = useState(null);

  const handleFileProcessed = (transcriptText, file) => {
    setTranscript(transcriptText);
    setFileName(file);
    setCurrentPage('results');
  };

  const handleSummaryGenerated = (summary) => {
    setSummaryData(summary);
    setCurrentPage('summary');
  };

  const handleBackToResults = () => {
    setCurrentPage('results');
  };

  const handleBackToHome = () => {
    setCurrentPage('home');
    setTranscript('');
    setFileName('');
    setSummaryData(null);
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
        />
      )}

      {currentPage === 'summary' && (
        <Summary 
          summaryData={summaryData}
          fileName={fileName}
          onBack={handleBackToResults}
        />
      )}
    </div>
  );
}

export default App;