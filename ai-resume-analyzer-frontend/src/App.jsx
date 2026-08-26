import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, FileText, CheckCircle, XCircle, AlertCircle, BarChart3, Star, X, User, BookOpen, Wrench } from 'lucide-react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const fileInputRef = useRef(null);

  const BACKEND_URL = "https://job-recommandation-system-dsv6.onrender.com";

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelection = (selectedFile) => {
    if (selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setResults(null);
    } else {
      alert('Please upload a valid PDF file.');
    }
  };

  const analyzeResume = async () => {
    if (!file) return;

    setIsAnalyzing(true);
    const formData = new FormData();
    formData.append('pdf', file);

    try {
      const response = await fetch('https://job-recommandation-system-dsv6.onrender.com/api/analyze/', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setResults(data);
      } else {
        alert("Error from backend: " + (data.error || "Unable to parse resume."));
      }
    } catch (error) {
      console.error("Network Error:", error);
      alert("Could not connect to the backend server. Please try again.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const containerVars = {
    hidden: { opacity: 0 },
    show: { opacity: 1, transition: { staggerChildren: 0.1 } }
  };
  const itemVars = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <>
      <nav className="navbar glass-panel">
        <div className="brand">
          <Star className="icon-success" fill="currentColor" />
          <span className="gradient-text">ResumeAI</span>
        </div>
        
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <a 
            href={BACKEND_URL} 
            style={{
              textDecoration: 'none',
              color: 'var(--text-main)',
              fontWeight: 600,
              fontSize: '0.9rem',
              padding: '0.5rem 1rem',
              borderRadius: '999px',
              border: '1px solid var(--surface-border)',
              background: 'rgba(255, 255, 255, 0.2)'
            }}
          >
            ← Back to Portal
          </a>

          <button 
            className="btn" 
            style={{padding: '0.5rem 1rem', fontSize: '0.9rem'}} 
            onClick={() => window.open('https://github.com', '_blank')}
          >
            View Docs
          </button>
        </div>
      </nav>

      <div className="main-container">
        {!results && !isAnalyzing && (
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="hero"
          >
            <h1>Unlock Your <span className="gradient-text">Career Potential</span></h1>
            <p>Our next-generation AI analyzes your resume against millions of successful profiles to give you an ATS score, skill radars, and actionable feedback.</p>
          </motion.div>
        )}

        <AnimatePresence mode="wait">
          {!results && !isAnalyzing && (
            <motion.div 
              key="upload"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9, filter: "blur(10px)" }}
              className="glass-panel" 
              style={{ padding: '3rem', marginTop: '2rem', maxWidth: '800px', margin: '2rem auto' }}
            >
              <label 
                className={`upload-zone ${isDragging ? 'active' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                style={{ display: 'block', cursor: 'pointer' }}
              >
                <div className="upload-icon-wrapper">
                  <UploadCloud size={40} />
                </div>
                <h2>Click to Upload or Drag & Drop</h2>
                <p style={{ marginTop: '0.5rem' }}>Supports PDF up to 5MB</p>
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  onChange={(e) => {
                    if (e.target.files && e.target.files[0]) {
                      handleFileSelection(e.target.files[0]);
                    }
                  }} 
                  accept="application/pdf"
                  style={{ display: 'none' }}
                />
              </label>

              {file && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="glass-panel"
                  style={{ marginTop: '1.5rem', padding: '1rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <FileText color="var(--primary)" />
                    <span style={{ fontWeight: 600 }}>{file.name}</span>
                  </div>
                  <X 
                    color="var(--text-muted)" 
                    style={{ cursor: 'pointer' }} 
                    onClick={() => { 
                      setFile(null); 
                      if (fileInputRef.current) fileInputRef.current.value = ''; 
                    }} 
                  />
                </motion.div>
              )}

              <div style={{ textAlign: 'center', marginTop: '2.5rem' }}>
                <button className="btn" onClick={analyzeResume} disabled={!file}>
                  Analyze with AI
                </button>
              </div>
            </motion.div>
          )}

          {isAnalyzing && (
            <motion.div 
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '5rem' }}
            >
              <div className="upload-icon-wrapper" style={{ animation: 'pulse 1.5s infinite' }}>
                <BarChart3 size={40} />
              </div>
              <h2 className="gradient-text" style={{ fontSize: '2rem' }}>Extracting insights...</h2>
              <p>Scanning against industry standards</p>
            </motion.div>
          )}

          {results && (
            <motion.div 
              key="results"
              variants={containerVars}
              initial="hidden"
              animate="show"
            >
              <motion.div variants={itemVars} style={{ textAlign: 'center', marginBottom: '3rem' }}>
                <h1 style={{ fontSize: '3rem' }}>Your Analysis is <span className="gradient-text">Ready</span></h1>
                <button className="btn" onClick={() => setResults(null)}>Analyze Another File</button>
              </motion.div>

              {/* Candidate Profile Details */}
              {results.personalDetails && (
                <motion.div variants={itemVars} className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
                  <div className="card-header">
                    <User className="icon-success" />
                    <h2>Candidate Profile</h2>
                  </div>
                  <div className="dashboard-grid" style={{ marginTop: 0, gap: '1rem' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      <div>
                        <h4 style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Full Name</h4>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.25rem', fontWeight: 600 }}>
                          <User size={20} className="icon-success" />
                          {results.personalDetails.name || 'Candidate'}
                        </div>
                      </div>
                      <div>
                        <h4 style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Education</h4>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.1rem' }}>
                          <BookOpen size={20} className="icon-warning" />
                          {results.personalDetails.education || 'N/A'}
                        </div>
                      </div>
                    </div>
                    <div>
                      <h4 style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>Top Extracted Skills</h4>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                        {(results.personalDetails.topSkills || []).map((skill, idx) => (
                          <span key={idx} className="chip" style={{ background: '#eff6ff', color: '#3b82f6', border: '1px solid #bfdbfe' }}>
                            <Wrench size={14} style={{ marginRight: '0.25rem' }} /> {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Top Metrics */}
              <div className="dashboard-grid" style={{ marginBottom: '2rem' }}>
                <motion.div variants={itemVars} className="glass-panel" style={{ padding: '2rem' }}>
                  <div className="card-header">
                    <Star className="icon-success" />
                    <h2>Overall Score</h2>
                  </div>
                  <div className="score-display">
                    <div className="score-number">{results.score || 0}</div>
                    <p>Out of 100</p>
                  </div>
                </motion.div>

                <motion.div variants={itemVars} className="glass-panel" style={{ padding: '2rem' }}>
                  <div className="card-header">
                    <CheckCircle className="icon-success" />
                    <h2>ATS Pass Probability</h2>
                  </div>
                  <div className="score-display">
                    <div className="score-number" style={{ background: 'linear-gradient(135deg, #10b981, #3b82f6)', WebkitBackgroundClip: 'text' }}>
                      {results.atsScore || 0}%
                    </div>
                    <div className="progress-bar-bg">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${results.atsScore || 0}%` }}
                        transition={{ duration: 1, delay: 0.5 }}
                        className="progress-bar-fill"
                      />
                    </div>
                  </div>
                </motion.div>
              </div>

              {/* Charts & Keywords */}
              <div className="dashboard-grid" style={{ marginBottom: '2rem' }}>
                <motion.div variants={itemVars} className="glass-panel" style={{ padding: '2rem', minHeight: '350px' }}>
                  <div className="card-header">
                    <BarChart3 className="icon-warning" />
                    <h2>Skills Radar</h2>
                  </div>
                  <div style={{ width: '100%', height: '250px' }}>
                    <ResponsiveContainer>
                      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={results.radarData || []}>
                        <PolarGrid stroke="rgba(0,0,0,0.1)" />
                        <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--text-muted)', fontSize: 12 }} />
                        <Radar name="Skills" dataKey="A" stroke="var(--primary)" fill="var(--primary)" fillOpacity={0.4} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                </motion.div>

                <motion.div variants={itemVars} className="glass-panel" style={{ padding: '2rem' }}>
                  <div className="card-header">
                    <FileText className="icon-success" />
                    <h2>Keyword Analysis</h2>
                  </div>
                  <div style={{ marginBottom: '1.5rem' }}>
                    <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Found in Resume</h4>
                    <div>
                      {(results.keywordsFound || []).map(kw => <span key={kw} className="chip found">{kw}</span>)}
                    </div>
                  </div>
                  <div>
                    <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Recommended Additions</h4>
                    <div>
                      {(results.keywordsMissing || []).map(kw => <span key={kw} className="chip missing">{kw}</span>)}
                    </div>
                  </div>
                </motion.div>
              </div>

              {/* Detailed Feedback */}
              <motion.div variants={itemVars} className="glass-panel" style={{ padding: '2rem' }}>
                <div className="dashboard-grid" style={{ marginTop: 0 }}>
                  <div>
                    <div className="card-header">
                      <CheckCircle className="icon-success" />
                      <h2>Strengths</h2>
                    </div>
                    <ul className="styled-list">
                      {(results.strengths || []).map((str, i) => (
                        <li key={i}><CheckCircle size={20} className="icon-success" style={{flexShrink: 0}} /> <span>{str}</span></li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <div className="card-header">
                      <XCircle className="icon-danger" />
                      <h2>Weaknesses</h2>
                    </div>
                    <ul className="styled-list">
                      {(results.weaknesses || []).map((wk, i) => (
                        <li key={i}><XCircle size={20} className="icon-danger" style={{flexShrink: 0}} /> <span>{wk}</span></li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div style={{ marginTop: '2rem', borderTop: '1px solid rgba(0,0,0,0.05)', paddingTop: '2rem' }}>
                  <div className="card-header">
                    <AlertCircle className="icon-warning" />
                    <h2>AI Recommendations</h2>
                  </div>
                  <ul className="styled-list">
                    {(results.recommendations || []).map((rec, i) => (
                      <li key={i}><AlertCircle size={20} className="icon-warning" style={{flexShrink: 0}} /> <span>{rec}</span></li>
                    ))}
                  </ul>
                </div>
              </motion.div>

            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </>
  );
}

export default App;