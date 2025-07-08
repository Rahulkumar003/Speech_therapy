import os
import wave
import parselmouth
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, render_template

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PLOT_FOLDER = 'static/plots'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
os.makedirs(PLOT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PLOT_FOLDER'] = PLOT_FOLDER

def is_wav_file(file_path):
    try:
        with wave.open(file_path, 'rb') as f:
            f.getparams()
        return True
    except wave.Error:
        return False


def save_plots(sound, plot_folder):
    plots = {}

    # Amplitude vs. Time
    plt.figure()
    plt.plot(sound.xs(), sound.values.T)
    plt.xlim([sound.xmin, sound.xmax])
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("Amplitude vs Time")
    amplitude_path = os.path.join(plot_folder, "amplitude_vs_time.png")
    plt.savefig(amplitude_path)
    plt.close()
    plots["amplitude"] = amplitude_path

    # Spectrogram with Intensity
    intensity = sound.to_intensity()
    spectrogram = sound.to_spectrogram()
    plt.figure()
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - 70, cmap="afmhot")
    plt.twinx()
    plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
    plt.xlim([sound.xmin, sound.xmax])
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.title("Spectrogram and Intensity")
    spectrogram_path = os.path.join(plot_folder, "spectrogram_intensity.png")
    plt.savefig(spectrogram_path)
    plt.close()
    plots["spectrogram"] = spectrogram_path

    # Spectrogram with Pitch
    pitch = sound.to_pitch()
    pre_emphasized_snd = sound.copy()
    pre_emphasized_snd.pre_emphasize()
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
    plt.figure()
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - 70, cmap="afmhot")
    plt.twinx()
    pitch_values = pitch.selected_array["frequency"]
    pitch_values[pitch_values == 0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.xlim([sound.xmin, sound.xmax])
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.title("Spectrogram with Pitch")
    pitch_path = os.path.join(plot_folder, "spectrogram_pitch.png")
    plt.savefig(pitch_path)
    plt.close()
    plots["pitch"] = pitch_path

    # Formant Analysis (F1 and F2)
    formant = sound.to_formant_burg()
    time_stamps = np.linspace(sound.xmin, sound.xmax, 100)
    F1 = [formant.get_value_at_time(1, t) for t in time_stamps]
    F2 = [formant.get_value_at_time(2, t) for t in time_stamps]
    plt.figure()
    plt.plot(time_stamps, F1, label="F1")
    plt.plot(time_stamps, F2, label="F2")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.title("Formants (F1 and F2) over Time")
    plt.legend()
    formant_path = os.path.join(plot_folder, "formants.png")
    plt.savefig(formant_path)
    plt.close()
    plots["formants"] = formant_path

    return plots



# Function to perform the audio analysis
def analyze_audio(filepath):
    try:
        sound = parselmouth.Sound(filepath)
        duration = sound.get_total_duration()
        sampling_frequency = sound.sampling_frequency

        # Amplitude analysis
        max_amplitude = np.max(np.abs(sound.values))
        amplitude_message = "Amplitude is within a suitable range."
        if max_amplitude < 0.2:
            amplitude_message = "The amplitude is very low. Ensure the recording volume is adequate."
        elif max_amplitude > 0.8:
            amplitude_message = "The amplitude is too high, which might cause distortion. Reduce the recording volume."

        # Intensity analysis
        intensity = sound.to_intensity()
        avg_intensity = np.mean(intensity.values)
        intensity_message = f"{avg_intensity:.3f}\nIntensity is appropriate."
        if avg_intensity < 50:
            intensity_message = f"{avg_intensity:.3f}\nThe intensity is low, indicating weak voice projection."
        elif avg_intensity > 80:
            intensity_message = f"{avg_intensity:.3f}\nThe intensity is very high, which might strain the voice."


        # Pitch analysis
        pitch = sound.to_pitch()
        pitch_values = pitch.selected_array["frequency"]
        pitch_values = pitch_values[pitch_values != 0]  # Exclude unvoiced frames
        avg_pitch = np.nanmean(pitch_values)
        pitch_message = "Pitch is normal."
        if avg_pitch < 85:
            pitch_message = "Pitch is below the normal range for adult males. Check for monotone delivery."
        elif 85 <= avg_pitch <= 180:
            pitch_message = "Pitch is normal for adult males."
        elif 180 < avg_pitch <= 255:
            pitch_message = "Pitch is normal for adult females."
        elif avg_pitch > 255:
            pitch_message = "Pitch is above normal. This may indicate tension or fatigue."

        # Jitter, Shimmer, and HNR analysis
        point_process = parselmouth.praat.call(sound, "To PointProcess (periodic, cc)", 75, 500)
        jitter = parselmouth.praat.call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        shimmer = parselmouth.praat.call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        try:
            hnr = parselmouth.praat.call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
            mean_hnr = parselmouth.praat.call(hnr, "Get mean", 0, 0)
        except parselmouth.PraatError as e:
            mean_hnr = None

        # shimmer_message = f"{shimmer:.6f} (proportion, multiply by 100 for percentage)"
        # hnr_message = f"{mean_hnr:.2f} dB"

        # Provide analysis for jitter, shimmer, and HNR
        if jitter <= 0.01:
            jitter_message = f"{jitter:.6f} (proportion, multiply by 100 for percentage). Jitter is within a normal range, indicating pitch stability."
        else:
            jitter_message = f"{jitter:.6f} (proportion, multiply by 100 for percentage). High jitter detected, which may suggest pitch instability."

        if shimmer <= 0.05:
            shimmer_message = f"{shimmer:.6f} (proportion, multiply by 100 for percentage). Shimmer is within a normal range, indicating stable amplitude."
        else:
            shimmer_message = f"{shimmer:.6f} (proportion, multiply by 100 for percentage). High shimmer detected, indicating amplitude instability."

        if mean_hnr > 20:
            hnr_message = f"{mean_hnr:.2f} dB. HNR indicates a healthy voice quality."
        else:
            hnr_message = f"{mean_hnr:.2f} dB. HNR is low, suggesting possible strain or breathiness."

        # Formant analysis for articulation
        formants = parselmouth.praat.call(sound, "To Formant (burg)", 0.01, 5, 5500, 0.025, 50)
        f1 = parselmouth.praat.call(formants, "Get mean", 1, 0, 0, "Hertz")
        f2 = parselmouth.praat.call(formants, "Get mean", 2, 0, 0, "Hertz")

        formant = sound.to_formant_burg()
        time_stamps = np.linspace(sound.xmin, sound.xmax, 100)
        formants = {
            "F1": [formant.get_value_at_time(1, t) for t in time_stamps],
            "F2": [formant.get_value_at_time(2, t) for t in time_stamps],
        }
        formant_message = ""
        if f1 < 250 or f1 > 800 :
            formant_message += "F1 values suggest issues in vowel articulation. "
        if f2 < 850 or f2 > 2500 :
            formant_message += "\nF2 values suggest issues in consonant articulation."
        else :
            formant_message += "F1 and F2 values are within the expected range, indicating normal articulation."

        # Speech rate analysis
        num_syllables = parselmouth.praat.call(point_process, "Get number of points")
        speech_rate = num_syllables / duration
        speech_rate_message = ""
        speech_rate_message += f"Speech rate is {speech_rate:.2f} syllables per second based on {num_syllables} syllables. "
        if speech_rate < 90:
            speech_rate_message += "Speech rate is too slow. Consider practicing fluent speaking."
        elif speech_rate > 120:
            speech_rate_message += "Speech rate is too fast, which might affect clarity."
        else:
            speech_rate_message += "Speech rate is within the normal conversational range."
    

        # Perform analyses and save plots
        plots = save_plots(sound, app.config['PLOT_FOLDER'])


        # Compile all results
        results = {
            "duration": f"{duration:.2f} seconds",
            "sampling_frequency": f"{sampling_frequency} Hz",
            "amplitude_message": amplitude_message,
            "intensity_message": intensity_message,
            "pitch_message": pitch_message,
            "jitter": jitter_message,
            "shimmer": shimmer_message,
            "hnr": hnr_message,
            "formant_message": formant_message,
            "speech_rate_message": speech_rate_message,
            "plots": plots
        }
        return results
    except parselmouth.PraatError as e:
        return {"error": f"Failed to analyze the audio file: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part provided!")

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No file selected!")

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    if not is_wav_file(filepath):
        os.remove(filepath)
        return render_template('index.html', error="Invalid file format. Please upload a valid WAV file!")

    try:
        analysis_results = analyze_audio(filepath)
        if "error" in analysis_results:
            return render_template('index.html', error=analysis_results["error"])
        return render_template('index.html', results=analysis_results)
    except Exception as e:
        return render_template('index.html', error=f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
