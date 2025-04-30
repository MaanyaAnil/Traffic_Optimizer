import React, { useState } from 'react';
import './App.css'; // You can add styling in this file

async function uploadVideos(videos) {
    const formData = new FormData();
    videos.forEach(video => formData.append('videos', video));

    const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to upload videos');
    }
    return response.json();
}

function App() {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [optimizedTimings, setOptimizedTimings] = useState(null);
    const [processedVideos, setProcessedVideos] = useState([]);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        const selectedFiles = Array.from(e.target.files);
        if (selectedFiles.length !== 4) {
            setError('You must upload exactly 4 videos (North, South, East, West)');
            return;
        }
        setError(null);
        setFiles(selectedFiles);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (files.length !== 4) {
            setError('You must upload exactly 4 videos');
            return;
        }

        setLoading(true);
        try {
          const data = await uploadVideos(files);
          setOptimizedTimings(data.optimized_timings);
          setProcessedVideos(data.processed_videos);
          console.log("Frontend received processedVideos:", data.processed_videos); // Add this line
          setError(null);
      } catch (err) {
          console.error(err);
          setError('Failed to upload videos.');
      } finally {
          setLoading(false);
      }
  };

    return (
        <div className="App">
            <h1>🚦 AI Traffic Flow Optimizer</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" multiple accept="video/*" onChange={handleFileChange} />
                <button type="submit" disabled={loading}>
                    {loading ? 'Uploading...' : 'Submit'}
                </button>
            </form>

            {error && <p style={{ color: 'red' }}>{error}</p>}

            {optimizedTimings && (
                <div>
                    <h2>Optimized Timings:</h2>
                    <ul>
                        <li><strong>North:</strong> {optimizedTimings.north} seconds</li>
                        <li><strong>South:</strong> {optimizedTimings.south} seconds</li>
                        <li><strong>East:</strong> {optimizedTimings.east} seconds</li>
                        <li><strong>West:</strong> {optimizedTimings.west} seconds</li>
                    </ul>
                </div>
            )}

            {processedVideos.length === 4 && (
                <div>
                    <h2>Processed Videos:</h2>
                    <div style={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap' }}>
                        {processedVideos.map((filename, index) => (
                            <div key={index} style={{ margin: '10px' }}>
                                <h3>{['North', 'South', 'East', 'West'][index]}</h3>
                                {console.log("Current filename:", filename)} {/* ADD THIS LINE */}
                                {filename ? (
                                  <video width="320" height="240" controls preload="auto">
                                      <source src={`http://localhost:8000/processed_video/${filename}`} type="video/mp4" />
                                      Your browser does not support the video tag.
                                 </video>
                                ) : (
                                    <p>Processing failed for this video.</p>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;