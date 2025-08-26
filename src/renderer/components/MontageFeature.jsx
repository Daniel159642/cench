import React, { useState, useRef } from 'react';
import './MontageFeature.css';

const MontageFeature = ({ onBack }) => {
  const [step, setStep] = useState('upload'); // upload, music, building
  const [photos, setPhotos] = useState([]);
  const [selectedMusic, setSelectedMusic] = useState(null);
  const [progress, setProgress] = useState(0);
  const [isBuilding, setIsBuilding] = useState(false);
  const fileInputRef = useRef(null);
  const dropZoneRef = useRef(null);

  // AI Recommended Music Options
  const recommendedMusic = [
    { id: 1, title: "Epic Adventure", genre: "Cinematic", duration: "2:30" },
    { id: 2, title: "Summer Vibes", genre: "Pop", duration: "3:15" },
    { id: 3, title: "Emotional Journey", genre: "Ambient", duration: "4:20" },
    { id: 4, title: "Upbeat Energy", genre: "Electronic", duration: "2:45" },
    { id: 5, title: "Peaceful Moments", genre: "Acoustic", duration: "3:30" }
  ];

  const handleFileSelect = (files) => {
    const newPhotos = Array.from(files).map((file, index) => ({
      id: Date.now() + index,
      file,
      preview: URL.createObjectURL(file),
      name: file.name
    }));
    setPhotos(prev => [...prev, ...newPhotos]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    handleFileSelect(files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const removePhoto = (id) => {
    setPhotos(prev => prev.filter(photo => photo.id !== id));
  };

  const handleMusicSelect = (music) => {
    setSelectedMusic(music);
  };

  const handleCustomMusic = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedMusic({
        id: 'custom',
        title: file.name,
        genre: 'Custom',
        duration: 'Unknown',
        file: file
      });
    }
  };

  const startMontageBuild = async () => {
    setIsBuilding(true);
    setStep('building');
    
    // Simulate montage building process
    for (let i = 0; i <= 100; i += 10) {
      setProgress(i);
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // Montage complete
    setIsBuilding(false);
    setStep('complete');
  };

  const renderUploadStep = () => (
    <div className="montage-step">
      <h2>📸 Photo Montage Creator</h2>
      <p>Drop your photos to create an amazing montage</p>
      
      <div 
        ref={dropZoneRef}
        className="drop-zone"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="drop-zone-content">
          <div className="upload-icon">📁</div>
          <p>Drop photos here or click to select</p>
          <p className="upload-hint">Supports: JPG, PNG, HEIC</p>
        </div>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept="image/*"
        onChange={(e) => handleFileSelect(e.target.files)}
        style={{ display: 'none' }}
      />

      {photos.length > 0 && (
        <div className="photo-grid">
          <h3>Selected Photos ({photos.length})</h3>
          <div className="photos-container">
            {photos.map(photo => (
              <div key={photo.id} className="photo-item">
                <img src={photo.preview} alt={photo.name} />
                <button 
                  className="remove-photo"
                  onClick={() => removePhoto(photo.id)}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {photos.length > 0 && (
        <button 
          className="next-button"
          onClick={() => setStep('music')}
        >
          Next: Choose Music ({photos.length} photos)
        </button>
      )}
    </div>
  );

  const renderMusicStep = () => (
    <div className="montage-step">
      <h2>🎵 Choose Your Music</h2>
      <p>Select music to accompany your montage</p>

      <div className="music-section">
        <h3>AI Recommended Music</h3>
        <div className="music-grid">
          {recommendedMusic.map(music => (
            <div 
              key={music.id}
              className={`music-item ${selectedMusic?.id === music.id ? 'selected' : ''}`}
              onClick={() => handleMusicSelect(music)}
            >
              <div className="music-icon">🎵</div>
              <div className="music-info">
                <h4>{music.title}</h4>
                <p>{music.genre} • {music.duration}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="custom-music">
          <h3>Or Upload Your Own Music</h3>
          <input
            type="file"
            accept="audio/*"
            onChange={handleCustomMusic}
            className="custom-music-input"
          />
          {selectedMusic?.id === 'custom' && (
            <p className="selected-music">✓ {selectedMusic.title}</p>
          )}
        </div>
      </div>

      <div className="step-buttons">
        <button className="back-button" onClick={() => setStep('upload')}>
          ← Back to Photos
        </button>
        {selectedMusic && (
          <button 
            className="next-button"
            onClick={startMontageBuild}
          >
            Create Montage
          </button>
        )}
      </div>
    </div>
  );

  const renderBuildingStep = () => (
    <div className="montage-step">
      <h2>🎬 Building Your Montage</h2>
      <p>Creating something amazing for you...</p>

      <div className="progress-container">
        <div className="progress-circle">
          <div className="progress-ring">
            <svg width="200" height="200">
              <circle
                cx="100"
                cy="100"
                r="80"
                stroke="#e0e0e0"
                strokeWidth="8"
                fill="none"
              />
              <circle
                cx="100"
                cy="100"
                r="80"
                stroke="#4CAF50"
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${2 * Math.PI * 80}`}
                strokeDashoffset={`${2 * Math.PI * 80 * (1 - progress / 100)}`}
                transform="rotate(-90 100 100)"
              />
            </svg>
            <div className="progress-text">
              <span className="progress-percentage">{progress}%</span>
              <span className="progress-label">Complete</span>
            </div>
          </div>
        </div>

        <div className="building-steps">
          <div className={`step ${progress >= 20 ? 'completed' : ''}`}>
            <span className="step-icon">📸</span>
            <span>Processing Photos</span>
          </div>
          <div className={`step ${progress >= 40 ? 'completed' : ''}`}>
            <span className="step-icon">🎵</span>
            <span>Adding Music</span>
          </div>
          <div className={`step ${progress >= 60 ? 'completed' : ''}`}>
            <span className="step-icon">🎬</span>
            <span>Creating Transitions</span>
          </div>
          <div className={`step ${progress >= 80 ? 'completed' : ''}`}>
            <span className="step-icon">✨</span>
            <span>Adding Effects</span>
          </div>
          <div className={`step ${progress >= 100 ? 'completed' : ''}`}>
            <span className="step-icon">🎉</span>
            <span>Finalizing</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderCompleteStep = () => (
    <div className="montage-step">
      <div className="complete-container">
        <div className="success-icon">🎉</div>
        <h2>Montage Complete!</h2>
        <p>Your amazing montage has been created successfully</p>
        
        <div className="montage-preview">
          <div className="preview-placeholder">
            <span>🎬</span>
            <p>Montage Preview</p>
          </div>
        </div>

        <div className="action-buttons">
          <button className="download-button">
            📥 Download Montage
          </button>
          <button className="share-button">
            📤 Share
          </button>
          <button className="new-montage-button" onClick={() => {
            setPhotos([]);
            setSelectedMusic(null);
            setProgress(0);
            setStep('upload');
          }}>
            🆕 Create New Montage
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="montage-feature">
      <div className="montage-header">
        <button className="back-button" onClick={onBack}>
          ← Back to Cench AI
        </button>
        <h1>🎬 Montage Creator</h1>
      </div>

      <div className="montage-content">
        {step === 'upload' && renderUploadStep()}
        {step === 'music' && renderMusicStep()}
        {step === 'building' && renderBuildingStep()}
        {step === 'complete' && renderCompleteStep()}
      </div>
    </div>
  );
};

export default MontageFeature;
