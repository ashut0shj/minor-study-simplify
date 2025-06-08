import React, { useState } from 'react';

const Results = ({ 
  transcript, 
  fileName, 
  onBack, 
  onSummaryGenerated, 
  onObjectiveQuestionsGenerated,
  onSubjectiveQuestionsGenerated
}) => {
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [isGeneratingObjective, setIsGeneratingObjective] = useState(false);
  const [isGeneratingSubjective, setIsGeneratingSubjective] = useState(false);
  const [error, setError] = useState('');

  const handleSummarize = async () => {
    setIsSummarizing(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/summarize', {
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
        onSummaryGenerated({
          important_words: data.important_words,
          summary: data.summary
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

    try {
      const response = await fetch('http://localhost:8000/generate-questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: transcript,
          num_questions: 5,
          num_options: 4
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        onObjectiveQuestionsGenerated(data);
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

    try {
      const response = await fetch('http://localhost:8000/generate-subjective-questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: transcript,
          num_questions: 5,
          answer_style: "all",
          use_evaluator: true
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        onSubjectiveQuestionsGenerated(data);
      } else {
        setError('Failed to generate questions');
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setIsGeneratingSubjective(false);
    }
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
        
        {error && (
          <div style={{ color: 'red', marginBottom: '10px' }}>
            {error}
          </div>
        )}

        <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
          <button
            onClick={handleSummarize}
            disabled={isSummarizing}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              backgroundColor: isSummarizing ? '#ccc' : '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: isSummarizing ? 'not-allowed' : 'pointer'
            }}
          >
            {isSummarizing ? 'Summarizing...' : 'Summarize Text'}
          </button>

          <button
            onClick={handleGenerateSubjective}
            disabled={isGeneratingSubjective}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              backgroundColor: isGeneratingSubjective ? '#ccc' : '#17a2b8',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: isGeneratingSubjective ? 'not-allowed' : 'pointer'
            }}
          >
            {isGeneratingSubjective ? 'Generating...' : 'Generate Subjective Questions'}
          </button>

          <button
            onClick={handleGenerateObjective}
            disabled={isGeneratingObjective}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              backgroundColor: isGeneratingObjective ? '#ccc' : '#ffc107',
              color: 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: isGeneratingObjective ? 'not-allowed' : 'pointer'
            }}
          >
            {isGeneratingObjective ? 'Generating...' : 'Generate Objective Questions'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Results;