import React from 'react';

const ObjectiveQuestions = ({ questions, fileName, onBack }) => {
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

      <h1>Objective Questions</h1>
      <h3>File: {fileName}</h3>
      <p>Total questions: {questions.total_questions}</p>

      <div style={{ marginTop: '30px' }}>
        {Object.entries(questions.questions).map(([key, q]) => (
          <div 
            key={key}
            style={{
              border: '1px solid #ddd',
              borderRadius: '4px',
              padding: '20px',
              marginBottom: '20px',
              backgroundColor: '#f8f9fa'
            }}
          >
            <h4>Q{key}: {q.question}</h4>
            <p><strong>Answer:</strong> {q.answer}</p>
            {q.options && q.options.length > 0 && (
              <div>
                <strong>Options:</strong>
                <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
                  {q.options.map((option, idx) => (
                    <li key={idx}>{option}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ObjectiveQuestions;