import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [generationStatus, setGenerationStatus] = useState({
    is_running: false,
    progress: 0,
    total: 0,
    current_phase: "",
    completed: false,
    files_created: []
  });
  
  const [sampleReview, setSampleReview] = useState(null);
  const [aspects, setAspects] = useState(null);
  const [testBatch, setTestBatch] = useState(null);
  const [settings, setSettings] = useState({
    total_reviews: 750000,
    chunk_size: 50000
  });

  // Poll for generation status
  useEffect(() => {
    const pollStatus = async () => {
      try {
        const response = await axios.get(`${API}/generation/status`);
        setGenerationStatus(response.data);
      } catch (error) {
        console.error("Error fetching status:", error);
      }
    };

    // Poll every 2 seconds when generation is running
    const interval = setInterval(pollStatus, 2000);
    pollStatus(); // Initial call

    return () => clearInterval(interval);
  }, []);

  const startGeneration = async () => {
    try {
      const response = await axios.post(`${API}/generation/start`, settings);
      alert(response.data.message);
    } catch (error) {
      alert(error.response?.data?.detail || "Error starting generation");
    }
  };

  const getSample = async () => {
    try {
      const response = await axios.get(`${API}/generation/sample`);
      setSampleReview(response.data);
    } catch (error) {
      alert("Error generating sample");
    }
  };

  const getAspects = async () => {
    try {
      const response = await axios.get(`${API}/generation/aspects`);
      setAspects(response.data);
    } catch (error) {
      alert("Error fetching aspects");
    }
  };

  const generateTestBatch = async () => {
    try {
      const response = await axios.post(`${API}/generation/test-batch?size=100`);
      setTestBatch(response.data);
    } catch (error) {
      alert("Error generating test batch");
    }
  };

  const formatProgress = () => {
    if (generationStatus.total === 0) return "0%";
    return ((generationStatus.progress / generationStatus.total) * 100).toFixed(1) + "%";
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Hotel Review Dataset Generator
          </h1>
          <p className="text-gray-600">
            Generate 750,000 balanced negative hotel reviews for AI training
          </p>
        </div>

        {/* Generation Controls */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Settings */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Generation Settings</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Total Reviews
                </label>
                <input
                  type="number"
                  value={settings.total_reviews}
                  onChange={(e) => setSettings({...settings, total_reviews: parseInt(e.target.value)})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={generationStatus.is_running}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Reviews per File
                </label>
                <input
                  type="number"
                  value={settings.chunk_size}
                  onChange={(e) => setSettings({...settings, chunk_size: parseInt(e.target.value)})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={generationStatus.is_running}
                />
              </div>
              
              <button
                onClick={startGeneration}
                disabled={generationStatus.is_running}
                className={`w-full py-2 px-4 rounded-md font-medium ${
                  generationStatus.is_running
                    ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                    : "bg-blue-600 text-white hover:bg-blue-700"
                }`}
              >
                {generationStatus.is_running ? "Generation Running..." : "Start Generation"}
              </button>
            </div>
          </div>

          {/* Status */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Generation Status</h2>
            
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Progress</span>
                  <span>{formatProgress()}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: formatProgress() }}
                  ></div>
                </div>
              </div>
              
              <div>
                <span className="text-sm text-gray-600">Current Phase:</span>
                <p className="font-medium">{generationStatus.current_phase || "Not started"}</p>
              </div>
              
              <div>
                <span className="text-sm text-gray-600">Reviews Generated:</span>
                <p className="font-medium">{generationStatus.progress.toLocaleString()} / {generationStatus.total.toLocaleString()}</p>
              </div>
              
              {generationStatus.completed && generationStatus.files_created.length > 0 && (
                <div>
                  <span className="text-sm text-gray-600">Files Created:</span>
                  <p className="font-medium text-green-600">{generationStatus.files_created.length} files</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Tools */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-3">Sample Review</h3>
            <button
              onClick={getSample}
              className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 mb-3"
            >
              Generate Sample
            </button>
            {sampleReview && (
              <div className="bg-gray-50 p-3 rounded text-sm">
                <p className="font-medium mb-2">Review {sampleReview.review_id}:</p>
                <p className="mb-2">"{sampleReview.review_text}"</p>
                <p className="text-blue-600">Aspects: {sampleReview.aspects.join(", ")}</p>
                <p className="text-red-600">Problems: {sampleReview.problems.join(" | ")}</p>
              </div>
            )}
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-3">Covered Aspects</h3>
            <button
              onClick={getAspects}
              className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 mb-3"
            >
              View Aspects
            </button>
            {aspects && (
              <div className="bg-gray-50 p-3 rounded text-sm max-h-32 overflow-y-auto">
                <p className="font-medium mb-2">Total: {aspects.total_aspects} aspects</p>
                <div className="text-xs">
                  {Object.keys(aspects.aspects).map(key => (
                    <span key={key} className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded mr-1 mb-1">
                      {key}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-3">Test Batch</h3>
            <button
              onClick={generateTestBatch}
              className="w-full bg-orange-600 text-white py-2 px-4 rounded-md hover:bg-orange-700 mb-3"
            >
              Generate 100 Reviews
            </button>
            {testBatch && (
              <div className="bg-gray-50 p-3 rounded text-sm">
                <p className="font-medium mb-2">{testBatch.message}</p>
                <p className="text-blue-600 mb-2">File: {testBatch.file}</p>
                <div className="max-h-24 overflow-y-auto">
                  {testBatch.sample.map(review => (
                    <p key={review.review_id} className="text-xs mb-1">
                      {review.review_id}: "{review.review_text}"
                    </p>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Dataset Information */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Dataset Features</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">750,000</div>
              <div className="text-sm text-gray-600">Negative Reviews</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">45+</div>
              <div className="text-sm text-gray-600">Hotel Aspects</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">60</div>
              <div className="text-sm text-gray-600">Max Tokens</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">100%</div>
              <div className="text-sm text-gray-600">Balanced Data</div>
            </div>
          </div>
          
          <div className="mt-6">
            <h3 className="font-bold text-gray-900 mb-2">Covered Aspects Include:</h3>
            <div className="flex flex-wrap gap-2 text-sm">
              {[
                "rooms", "bathrooms", "shower", "bed", "wifi", "elevator", "breakfast", 
                "restaurant", "staff", "service", "cleaning", "air conditioning", "bar",
                "food", "price", "pool", "parking", "noise", "temperature", "tv"
              ].map(aspect => (
                <span key={aspect} className="bg-gray-200 text-gray-700 px-2 py-1 rounded">
                  {aspect}
                </span>
              ))}
              <span className="text-gray-500">...and many more with synonyms</span>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-8">
          <h3 className="text-lg font-bold text-blue-900 mb-2">Next Steps for GitHub Upload</h3>
          <ol className="list-decimal list-inside text-blue-800 space-y-1">
            <li>Click "Start Generation" to create your 750k review dataset</li>
            <li>Files will be saved in the 'dataset_parts' directory</li>
            <li>Each file contains 50,000 reviews (15 files total)</li>
            <li>Upload files to your GitHub repository</li>
            <li>Share the repository link for easy dataset distribution</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default App;
