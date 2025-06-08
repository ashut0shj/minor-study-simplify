import React, { useState } from 'react';
import Home from './components/home';
import Results from './components/trans';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [transcript, setTranscript] = useState('');
  const [fileName, setFileName] = useState('');

  const handleFileProcessed = (transcriptText, file) => {
    setTranscript(transcriptText);
    setFileName(file);
    setCurrentPage('results');
  };

  const handleBackToHome = () => {
    setCurrentPage('home');
    setTranscript('');
    setFileName('');
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
        />
      )}
    </div>
  );
}

export default App;