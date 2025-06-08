import React, { useState } from 'react';

const Home = ({ onFileProcessed }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setError('');
    }
  };

  const handleStart = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setIsProcessing(true);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/transcribe', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        onFileProcessed(data.transcript, selectedFile.name);
      } else {
        setError('Failed to process file');
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Study-Simplify</h1>
      <h2>Upload Study Materials</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="file"
          accept=".pdf,.ppt,.pptx,.jpg,.jpeg,.png,.doc,.docx"
          onChange={handleFileSelect}
          style={{ marginBottom: '10px', display: 'block' }}
        />
        
        {selectedFile && (
          <p>Selected: {selectedFile.name}</p>
        )}
      </div>

      <button 
        onClick={handleStart}
        disabled={!selectedFile || isProcessing}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: isProcessing ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: isProcessing ? 'not-allowed' : 'pointer'
        }}
      >
        {isProcessing ? 'Processing...' : 'Start'}
      </button>

      {error && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          {error}
        </div>
      )}
    </div>
  );
};

export default Home;