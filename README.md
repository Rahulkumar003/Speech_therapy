# SpeakSmart

Welcome to **SpeakSmart**, your ultimate destination for innovative speech therapy solutions. Our platform is designed to empower individuals by analyzing their voice and providing personalized therapy options. Whether you prefer guidance from professional therapists or AI-driven therapy sessions, we cater to your unique needs.

## Project Description

At SpeakSmart, we believe in the power of technology to transform speech therapy. Our advanced analysis tools offer insights into your vocal patterns, helping you understand and improve your speech. With our AI therapy, you can practice and enhance your skills at your own pace, anytime and anywhere.

Dive into our extensive repository, brimming with resources to boost your speech in a fun and engaging way. Experience a gamified learning journey that makes speech improvement enjoyable and rewarding. Join us at SpeakSmart and take the first step towards a more confident and articulate you!

## Features

- **Voice Analysis**: Get detailed insights into your vocal patterns, including pitch, amplitude, and speech rate.
- **Personalized Therapy**: Tailored therapy sessions based on your unique vocal analysis.
- **User-Friendly Interface**: Easy navigation and interaction for a seamless experience.
- **Gamified Learning**: Engage with interactive resources that make learning enjoyable.
- **AI-Driven Insights**: Leverage advanced AI technology for effective speech therapy.

## 🧠 Speech Analysis Module

The **Speech Analysis Module** is the core of SpeakSmart. Here's how it works:

- 🎙️ **Upload Your Voice File**  
  Begin by uploading your voice recording directly through our simple interface.

- 📊 **Advanced Voice Analysis**  
  Using the **Parselmouth** library (Python wrapper for Praat), we extract essential vocal features such as:
  - Pitch
  - Amplitude
  - Speech Rate
  - Formants

- 🧮 **Data Visualization**  
  We use **NumPy** and **Matplotlib** to display your vocal trends in graphical form. These visuals give users an intuitive way to track and understand their voice patterns over time.

- 🌐 **Web Audio API Integration**  
  For real-time recording and audio input, we utilized the **Web Audio API**, allowing seamless interaction with your microphone from the browser.

- 🧠 **Personalized AI Therapy**  
  Based on the analysis results, the system generates targeted recommendations and interactive exercises tailored just for you.

### 📸 Screenshots

<p align="center">
  <img src="screenshots/speech_analysis_upload.jpg" width="30%" />
  <img src="screenshots/speech_analysis_graph1.jpg" width="30%" />
  <img src="screenshots/speech_analysis_graph1.jpg" width="30%" />
</p>

---

## Getting Started

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rahulkumar003/speaksmart.git
   cd speaksmart
