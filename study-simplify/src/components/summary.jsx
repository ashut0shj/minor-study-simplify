import React from 'react';

const Summary = ({ summaryData, fileName, onBack }) => {
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
        ← Back to Results
      </button>

      <h1>Summary</h1>
      <h3>File: {fileName}</h3>

      <div style={{ marginBottom: '30px' }}>
        <h4>Important Keywords:</h4>
        <div style={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: '8px',
          marginBottom: '20px'
        }}>
          {summaryData.important_words.map((word, index) => (
            <span 
              key={index}
              style={{
                padding: '4px 8px',
                backgroundColor: '#e9ecef',
                borderRadius: '4px'
              }}
            >
              {word}
            </span>
          ))}
        </div>

        <h4>Summary:</h4>
        <div style={{
          border: '1px solid #ddd',
          borderRadius: '4px',
          padding: '20px',
          backgroundColor: '#f8f9fa',
          lineHeight: '1.6',
          whiteSpace: 'pre-wrap'
        }}>
          {summaryData.summary}
        </div>
      </div>
    </div>
  );
};

export default Summary;