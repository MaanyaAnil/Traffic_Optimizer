import React, { useState } from 'react';
import { uploadVideos } from '../api';

const UploadPage = () => {
  const [files, setFiles] = useState([]);
  const [error, setError] = useState(null);
  const [optimizedTimings, setOptimizedTimings] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setError(null);
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length !== 4) {
      setError("You must upload exactly 4 videos (North, South, East, West).");
      return;
    }
    setFiles(selectedFiles);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await uploadVideos(files);
      setOptimizedTimings(data.optimized_timings);
    } catch (err) {
      setError("There was an error uploading the videos. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">
      <h2>Upload Traffic Videos</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" multiple accept="video/*" onChange={handleFileChange} />
        <button type="submit" disabled={loading || files.length !== 4}>
          {loading ? "Uploading..." : "Submit"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {optimizedTimings && (
        <div className="timings">
          <h3>Optimized Traffic Signal Timings</h3>
          <ul>
            <li>North: {optimizedTimings.north} sec</li>
            <li>South: {optimizedTimings.south} sec</li>
            <li>East: {optimizedTimings.east} sec</li>
            <li>West: {optimizedTimings.west} sec</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default UploadPage;
