import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import Results from './components/trans';
import Summary from './components/summary';
import ObjectiveQuestions from './components/objectiveQues';
import SubjectiveQuestions from './components/subjectiveQues';

function App() {
  return (
    <Router>
      <Routes>
        {/* Main route - Home page */}
        <Route path="/" element={<Home />} />
        
        {/* Results page - shows transcript with action buttons */}
        <Route path="/results" element={<Results />} />
        
        {/* Summary page */}
        <Route path="/summary" element={<Summary />} />
        
        {/* Objective questions page */}
        <Route path="/objective-questions" element={<ObjectiveQuestions />} />
        
        {/* Subjective questions page */}
        <Route path="/subjective-questions" element={<SubjectiveQuestions />} />
      </Routes>
    </Router>
  );
}

export default App;