import React, { useState } from 'react';
import { Upload, FileText, Check, Loader2, HelpCircle, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  // Mock navigate function - replace with useNavigate() from react-router-dom in your actual app
  const navigate = useNavigate();

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setError('');
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      const allowedTypes = ['.pdf', '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.doc', '.docx'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (allowedTypes.includes(fileExtension)) {
        setSelectedFile(file);
        setError('');
      } else {
        setError('File type not supported');
      }
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
      const response = await fetch('https://minor-study-simplify.onrender.com/transcribe', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        navigate('/results', { 
          state: { 
            transcript: data.transcript, 
            fileName: selectedFile.name 
          } 
        });
      } else {
        setError('Failed to process file');
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const teamMembers = [
    {
      name: "Ashutosh Jaiswal",
      github: "https://github.com/ashut0shj",
      email: "ashutosh22102@iiitnr.edu.in"
    },
    {
      name: "Kanika Malhotra", 
      github: "https://github.com/kanika1-13",
      email: "kanika22102@iiitnr.edu.in"
    },
    {
      name: "Swasti Srivastava",
      github: "https://github.com/Swasti-23", 
      email: "swasti22102@iiitnr.edu.in"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-blue-50">
      {/* Decorative Elements */}
      <div className="fixed top-10 right-10 opacity-10 text-purple-300 text-6xl rotate-12 pointer-events-none">
        🐱
      </div>
      <div className="fixed bottom-20 left-10 opacity-10 text-blue-300 text-4xl -rotate-12 pointer-events-none">
        🐾
      </div>
      <div className="fixed top-16 right-24 opacity-15 text-purple-300 text-5xl rotate-45 pointer-events-none z-0">
      🐱
      </div>
      <div className="fixed bottom-32 left-12 opacity-15 text-blue-300 text-4xl -rotate-12 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-1/2 left-8 opacity-15 text-purple-400 text-4xl rotate-12 pointer-events-none z-0">
      🐱
      </div>
      <div className="fixed bottom-1/4 right-28 opacity-15 text-blue-400 text-4xl rotate-45 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-1/4 right-12 opacity-15 text-purple-500 text-5xl -rotate-30 pointer-events-none z-0">
      🐱
      </div>
      <div className="fixed top-3/4 left-20 opacity-15 text-blue-500 text-4xl rotate-60 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-1/3 left-1/3 opacity-15 text-purple-300 text-5xl rotate-12 pointer-events-none z-0">
      🐱
      </div>
      <div className="fixed bottom-1/2 right-1/4 opacity-15 text-blue-300 text-4xl -rotate-45 pointer-events-none z-0">
        🐾
      </div>
      <div className="fixed top-2/3 right-1/3 opacity-15 text-purple-400 text-4xl rotate-30 pointer-events-none z-0">
      🐱
      </div>

      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-purple-200 sticky top-0 z-50">
        <div className="l mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-500 rounded-xl flex items-center justify-center text-white font-bold text-xl relative">
              S
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-purple-400 rounded-full"></div>
              <div className="absolute -top-1 -left-1 w-3 h-3 bg-blue-400 rounded-full"></div>
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-500 bg-clip-text text-transparent">
              Study-Simplify
            </h1>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <h2 className="text-5xl font-bold text-gray-800 mb-6 leading-tight">
            Transform Your Study Materials into
            <span className="bg-gradient-to-r from-blue-600 to-purple-500 bg-clip-text text-transparent block">
              Smart Learning Notes
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Upload PDFs, presentations, or images and get AI-powered summaries and custom questions using our proprietary AI model. 
            Learning made simple and smart! 🎯
          </p>
        </div>

        {/* AI Model Info Banner */}
        <div className="max-w-2xl mx-auto mb-8">
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-6 text-center">
            <div className="flex items-center justify-center space-x-2 mb-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-sm">AI</span>
              </div>
              <h4 className="text-lg font-bold text-gray-800">Powered by Our Custom AI Model</h4>
            </div>
            <p className="text-gray-600 text-sm">
              No external APIs used - Built entirely with our proprietary AI technology for enhanced privacy and performance
            </p>
          </div>
        </div>

        {/* Upload Section - Only show if no file is selected */}
        <div className="max-w-2xl mx-auto mb-16">
          {!selectedFile ? (
            <div
              className={`border-3 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ${
                dragActive 
                  ? 'border-purple-400 bg-purple-50 scale-105' 
                  : 'border-purple-300 bg-white/50 hover:border-purple-400 hover:bg-white/70'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <div className="mb-6">
                <div className="w-20 h-20 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Upload className="w-10 h-10 text-purple-600" />
                </div>
                <h3 className="text-2xl font-semibold text-gray-700 mb-2">
                  Drop your study materials here
                </h3>
                <p className="text-gray-500">or click to browse files</p>
              </div>
              
              <input
                type="file"
                accept=".pdf,.ppt,.pptx,.jpg,.jpeg,.png,.doc,.docx"
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="inline-block bg-gradient-to-r from-blue-600 to-purple-500 text-white px-8 py-3 rounded-full cursor-pointer hover:shadow-lg transition-all duration-300 transform hover:scale-105"
              >
                Choose Files
              </label>
              
              <div className="mt-4 text-sm text-gray-400">
                Supports PDF, PPT, Images, DOC, and more
              </div>
            </div>
          ) : (
            /* Selected File Display - Only show when file is selected */
            <div className="bg-white/70 backdrop-blur-sm rounded-xl p-6 border border-purple-200">
              <h6 className="font-semibold text-gray-700 mb-3 flex items-center">
                <Check className="w-5 h-5 text-green-500 mr-2" />
                Selected File
              </h6>
              <div className="flex items-center justify-between bg-white rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <FileText className="w-6 h-6 text-blue-600" />
                  <div>
                    <div className="text-gray-700 font-medium">{selectedFile.name}</div>
                    <div className="text-sm text-gray-500">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </div>
                  </div>
                </div>
                <button
                  onClick={handleStart}
                  disabled={isProcessing}
                  className={`px-6 py-2 rounded-full text-white font-medium transition-all duration-300 transform ${
                    isProcessing
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-600 to-purple-500 hover:shadow-lg hover:scale-105'
                  }`}
                >
                  {isProcessing ? (
                    <div className="flex items-center space-x-2">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Processing...</span>
                    </div>
                  ) : (
                    'Start Analysis'
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 text-red-700">
                <span className="font-medium">⚠️ Error:</span>
                <span>{error}</span>
              </div>
            </div>
          )}
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 hover:shadow-xl transition-all duration-300 transform hover:scale-105 border border-blue-200">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center mb-6">
              <FileText className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-3">Smart Summaries</h3>
            <p className="text-gray-600 leading-relaxed">
              Get concise, organized notes that capture all key concepts and important information from your study materials.
            </p>
          </div>

          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 hover:shadow-xl transition-all duration-300 transform hover:scale-105 border border-purple-200">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-100 to-purple-200 rounded-2xl flex items-center justify-center mb-6">
              <HelpCircle className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-3">Custom Questions</h3>
            <p className="text-gray-600 leading-relaxed">
              Generate both subjective and objective questions tailored to your content for effective exam preparation.
            </p>
          </div>
        </div>

        {/* How It Works
        <div className="text-center">
          <h3 className="text-3xl font-bold text-gray-800 mb-12">How Study-Simplify Works</h3>
          <div className="flex flex-col md:flex-row items-center justify-center space-y-8 md:space-y-0 md:space-x-8">
            <div className="flex flex-col items-center max-w-xs">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
                1
              </div>
              <h4 className="font-semibold text-gray-700 mb-2">Upload Materials</h4>
              <p className="text-gray-500 text-center">Drop your PDFs, presentations, or images</p>
            </div>
            
            <ArrowRight className="w-8 h-8 text-purple-400 hidden md:block" />
            
            <div className="flex flex-col items-center max-w-xs">
              <div className="w-16 h-16 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
                2
              </div>
              <h4 className="font-semibold text-gray-700 mb-2">Custom AI Processing</h4>
              <p className="text-gray-500 text-center">Our proprietary AI model analyzes and extracts key information</p>
            </div>
            
            <ArrowRight className="w-8 h-8 text-purple-400 hidden md:block" />
            
            <div className="flex flex-col items-center max-w-xs">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
                3
              </div>
              <h4 className="font-semibold text-gray-700 mb-2">Get Results</h4>
              <p className="text-gray-500 text-center">Receive summaries and custom questions</p>
            </div>
          </div>
        </div> */}
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12 mt-16">
        <div className="max-w-6xl mx-auto px-6">
          {/* Logo and Title */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold relative">
                S
                <div className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-purple-400 rounded-full"></div>
                <div className="absolute -top-0.5 -left-0.5 w-2 h-2 bg-blue-400 rounded-full"></div>
              </div>
              <h3 className="text-xl font-bold">Study-Simplify</h3>
            </div>
            <p className="text-gray-400 mb-6">Making learning simple and smart with our custom AI!</p>
          </div>

          {/* Team Section */}
          <div className="mb-8 text-center">
            <h4 className="text-lg font-semibold mb-6 text-purple-300">Our Team</h4>
            <div className="flex flex-wrap justify-center gap-8">
              {teamMembers.map((member, index) => (
                <div key={index} className="text-gray-300">
                  <div className="font-semibold text-white text-lg mb-1">{member.name}</div>
                  <div className="text-sm">
                    <a 
                      href={member.github} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-purple-400 hover:text-purple-300 transition-colors block"
                    >
                      {member.github}
                    </a>
                  </div>
                  <div className="text-blue-400 text-sm">{member.email}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Bottom Section */}
          <div className="border-t border-gray-700 pt-6 text-center">
            <div className="flex flex-col md:flex-row justify-center items-center space-y-2 md:space-y-0 md:space-x-6 text-sm text-gray-400">
              <span><a href = 'https://github.com/ashut0shj/minor-study-simplify/'>Github Link</a></span><br />
              <span>Made with 💜 for students</span>
              <span className="hidden md:block">•</span>
              <span>Powered by Our Custom AI Model & React</span>
              <span className="hidden md:block">•</span>
              <span>© 2024 Study-Simplify Team</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
