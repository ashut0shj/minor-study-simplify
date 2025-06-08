import React from 'react';

const Results = ({ transcript, fileName, onBack }) => {
  const handleSummarize = () => {
    // TODO: Add summarization functionality
    console.log('Summarize clicked');
  };

  const handleGenerateSubjective = () => {
    // TODO: Add subjective question generation functionality
    console.log('Generate Subjective Questions clicked');
  };

  const handleGenerateObjective = () => {
    // TODO: Add objective question generation functionality
    console.log('Generate Objective Questions clicked');
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <button 
        onClick={onBack}
        style={{
          marginBottom: '20px',
          padding: '8px 16px',
          backgroundColor: '#6c757d',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        ← Back to Upload
      </button>

      <h1>Transcribed Content</h1>
      <h3>File: {fileName}</h3>

      <div style={{
        border: '1px solid #ddd',
        borderRadius: '4px',
        padding: '20px',
        marginBottom: '30px',
        backgroundColor: '#f8f9fa',
        maxHeight: '400px',
        overflowY: 'auto'
      }}>
        <h4>Transcript:</h4>
        <p style={{ lineHeight: '1.6', whiteSpace: 'pre-wrap' }}>
          {transcript}
        </p>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Choose an action:</h3>
        
        <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
          <button
            onClick={handleSummarize}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Summarize Text
          </button>

          <button
            onClick={handleGenerateSubjective}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              backgroundColor: '#17a2b8',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Generate Subjective Questions
          </button>

          <button
            onClick={handleGenerateObjective}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              backgroundColor: '#ffc107',
              color: 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Generate Objective Questions
          </button>
        </div>
      </div>
    </div>
  );
};

export default Results;