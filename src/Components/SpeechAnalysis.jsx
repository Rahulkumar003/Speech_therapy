import React, { useState } from "react";
import Navbar from "./Navbar";

const SpeechAnalysis = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Define styles object
  const styles = {
    body: {
      padding: "20px",
      maxWidth: "800px",
      margin: "0 auto",
    },
    h1: {
      textAlign: "center",
      marginBottom: "20px",
    },
    form: {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
    },
    label: {
      marginBottom: "10px",
    },
    input: {
      marginBottom: "20px",
    },
    button: {
      padding: "10px 20px",
      backgroundColor: "#007BFF",
      color: "#fff",
      border: "none",
      borderRadius: "5px",
      cursor: "pointer",
    },
    error: {
      color: "red",
      textAlign: "center",
      marginTop: "20px",
    },
    results: {
      marginTop: "20px",
    },
    resultsUl: {
      listStyleType: "none",
      padding: 0,
    },
    resultsLi: {
      marginBottom: "10px",
    },
    resultsImg: {
      maxWidth: "100%",
      height: "auto",
      marginBottom: "10px",
    },
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setResults(data);
        setError(null);
      } else {
        setError(data.error || "An error occurred during the upload.");
      }
    } catch (err) {
      setError("An error occurred while connecting to the server.");
    }
  };

  return (
    <div>
      <Navbar />
      <div style={styles.body}>
        <h1 style={{ marginTop: '80px' }}>Upload WAV File for Analysis</h1>
        <form onSubmit={handleSubmit} style={styles.form}>
          <label htmlFor="file" style={styles.label}>
            Select WAV File:
          </label>
          <input
            type="file"
            name="file"
            id="file"
            accept=".wav"
            onChange={handleFileChange}
            required
            style={styles.input}
          />
          <button type="submit" style={styles.button}>
            Upload
          </button>
        </form>

        {error && <div style={styles.error}>{error}</div>}
        {results && (
          <div style={styles.results}>
            <h2>Analysis Results</h2>
            <ul style={styles.resultsUl}>
              <li style={styles.resultsLi}>Duration: {results.duration}</li>
              <li style={styles.resultsLi}>Sampling Frequency: {results.sampling_frequency}</li>
              <li style={styles.resultsLi}>Amplitude: {results.amplitude_message}</li>
              <li style={styles.resultsLi}>Intensity: {results.intensity_message}</li>
              <li style={styles.resultsLi}>Pitch: {results.pitch_message}</li>
              <li style={styles.resultsLi}>Jitter: {results.jitter}</li>
              <li style={styles.resultsLi}>Shimmer: {results.shimmer}</li>
              <li style={styles.resultsLi}>HNR: {results.hnr}</li>
              <li style={styles.resultsLi}>Formant: {results.formant_message}</li>
              <li style={styles.resultsLi}>Speech Rate: {results.speech_rate_message}</li>
            </ul>
            <div>
              <img src={`/${results.plots.amplitude}`} alt="Amplitude vs Time" style={styles.resultsImg} />
              <img src={`/${results.plots.spectrogram}`} alt="Spectrogram and Intensity" style={styles.resultsImg} />
              <img src={`/${results.plots.pitch}`} alt="Spectrogram with Pitch" style={styles.resultsImg} />
              <img src={`/${results.plots.formants}`} alt="Formants" style={styles.resultsImg} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SpeechAnalysis;