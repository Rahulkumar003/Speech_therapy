import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()  # Use seaborn's default style for attractive graphs

# Load the audio file
snd = parselmouth.Sound("harvard.wav")

# Plot amplitude vs. time
plt.figure()
plt.plot(snd.xs(), snd.values.T)
plt.xlim([snd.xmin, snd.xmax])
plt.xlabel("time [s]")
plt.ylabel("amplitude")
plt.title("Amplitude vs Time")
plt.savefig("amplitude_vs_time.png")
plt.close()  # Close the figure to free up memory

# Analysis of amplitude graph
max_amplitude = np.max(np.abs(snd.values))
if max_amplitude < 0.2:
    print("The amplitude is very low. Ensure the recording volume is adequate.")
elif max_amplitude > 0.8:
    print("The amplitude is too high, which might cause distortion. Reduce the recording volume.")
else:
    print("Amplitude is within a suitable range.")

# Function to draw spectrogram
def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap="afmhot")
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")


# Function to draw intensity
def draw_intensity(intensity):
    plt.plot(intensity.xs(), intensity.values.T, linewidth=3, color="w")
    plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
    plt.grid(False)
    plt.ylim(0)
    plt.ylabel("intensity [dB]")


# Draw spectrogram with intensity
intensity = snd.to_intensity()
spectrogram = snd.to_spectrogram()
plt.figure()
draw_spectrogram(spectrogram)
plt.twinx()
draw_intensity(intensity)
plt.xlim([snd.xmin, snd.xmax])
plt.title("Spectrogram and Intensity")
plt.savefig("spectrogram_intensity.png")
plt.close()

# Intensity analysis
avg_intensity = np.mean(intensity.values)
if avg_intensity < 50:
    print("The intensity is low, indicating weak voice projection. Consider speaking louder.")
elif avg_intensity > 80:
    print("The intensity is very high, which might strain the voice. Aim for a moderate intensity.")

# Function to draw pitch
def draw_pitch(pitch):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("fundamental frequency [Hz]")

pitch = snd.to_pitch()
# point_process = parselmouth.praat.call([snd, pitch], "To PointProcess (periodic, cc)")
# If desired, pre-emphasize the sound fragment before calculating the spectrogram
pre_emphasized_snd = snd.copy()
pre_emphasized_snd.pre_emphasize()
spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)

plt.figure()
draw_spectrogram(spectrogram)
plt.twinx()
draw_pitch(pitch)
plt.xlim([snd.xmin, snd.xmax])
plt.savefig("spectrogram_pitch.png")
plt.close()

# Pitch analysis
pitch_values = pitch.selected_array["frequency"]
pitch_values = pitch_values[pitch_values != 0]  # Exclude unvoiced frames
avg_pitch = np.nanmean(pitch_values)
if avg_pitch < 85:
    print("Pitch is below the normal range for adult males. Check for monotone delivery.")
elif 85 <= avg_pitch <= 180:
    print("Pitch is normal for adult males.")
elif 180 < avg_pitch <= 255:
    print("Pitch is normal for adult females.")
elif avg_pitch > 255:
    print("Pitch is above normal. This may indicate tension or fatigue.")
else:
    print("Pitch is abnormal. Further evaluation is required.")


# Speech Quality Assessment: Jitter, Shimmer, HNR
def speech_quality_assessment(sound):
    point_process = parselmouth.praat.call(sound, "To PointProcess (periodic, cc)", 75, 500)
    jitter = parselmouth.praat.call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    
    # Correct shimmer call with the "Maximum amplitude factor" argument
    shimmer = parselmouth.praat.call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    
    # Correct HNR calculation
    try:
        hnr = parselmouth.praat.call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
        mean_hnr = parselmouth.praat.call(hnr, "Get mean", 0, 0)
        print(f"Jitter: {jitter:.6f} (proportion, multiply by 100 for percentage)")
        print(f"Shimmer: {shimmer:.6f} (proportion, multiply by 100 for percentage)")
        print(f"HNR: {mean_hnr:.2f} dB")
        
        # Provide analysis
        if jitter <= 0.01:
            print("Jitter is within a normal range, indicating pitch stability.")
        else:
            print("High jitter detected, which may suggest pitch instability.")

        if shimmer <= 0.05:
            print("Shimmer is within a normal range, indicating stable amplitude.")
        else:
            print("High shimmer detected, indicating amplitude instability.")

        if mean_hnr > 20:
            print("HNR indicates a healthy voice quality.")
        else:
            print("HNR is low, suggesting possible strain or breathiness.")

    except parselmouth.PraatError as e:
        print("Error in calculating Harmonics-to-Noise Ratio (HNR):", e)

speech_quality_assessment(snd)
print()

# Formant Analysis for Articulation Monitoring
def analyze_formants(sound):
    formant = sound.to_formant_burg()
    time_stamps = np.linspace(sound.xmin, sound.xmax, 100)
    formants = {
        "F1": [formant.get_value_at_time(1, t) for t in time_stamps],
        "F2": [formant.get_value_at_time(2, t) for t in time_stamps],
    }
    plt.figure()
    plt.plot(time_stamps, formants["F1"], label="F1", color="r")
    plt.plot(time_stamps, formants["F2"], label="F2", color="b")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.title("Formants (F1 and F2)")
    plt.legend()
    plt.savefig("formants_f1_f2.png")
    plt.close()

    # Provide analysis
    if any(f < 250 or f > 800 for f in formants["F1"]):
        print("F1 values suggest issues in vowel articulation.")
    if any(f < 850 or f > 2500 for f in formants["F2"]):
        print("F2 values suggest issues in consonant articulation.")

analyze_formants(snd)
print()

# Speech Rate and Rhythm
def speech_rate_and_rhythm(sound):
    point_process = parselmouth.praat.call(sound, "To PointProcess (periodic, cc)", 75, 500)
    num_syllables = parselmouth.praat.call(point_process, "Get number of points")
    duration = sound.get_total_duration()
    speech_rate = num_syllables / duration
    print(f"Speech Rate: {speech_rate:.2f} syllables/second")

    # Provide analysis
    if speech_rate < 90:
        print("Speech rate is too slow. Consider practicing fluent speaking.")
    elif speech_rate > 120:
        print("Speech rate is too fast, which might affect clarity.")
    else:
        print("Speech rate is within the normal conversational range.")

speech_rate_and_rhythm(snd)
print()
