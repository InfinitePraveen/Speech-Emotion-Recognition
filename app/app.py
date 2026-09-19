"""
Speech Emotion Recognition - Flask demo app
--------------------------------------------
Loads the trained model (see notebooks/) and lets a user upload a short
.wav clip to see the predicted emotion, along with the full probability
breakdown across classes.

Run with:
    cd app
    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

import os
import pickle
import numpy as np
import librosa
from flask import Flask, render_template, request, jsonify
from tensorflow import keras
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "emotion_model.h5")
ENCODER_PATH = os.path.join(BASE_DIR, "model", "label_encoder.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"wav", "mp3", "ogg", "flac"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

# ---------------------------------------------------------------------
# Load model + preprocessing artifacts once at startup
# ---------------------------------------------------------------------
print("Loading model...")
model = keras.models.load_model(MODEL_PATH)

with open(ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)
    FEATURE_MEAN = scaler["mean"]
    FEATURE_STD = scaler["std"]

EMOJI_MAP = {
    "neutral": "😐",
    "calm": "🙂",
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "fearful": "😨",
    "disgust": "🤢",
    "surprised": "😲",
}

print("Model loaded. Ready to serve predictions.")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_feature(file_path, mfcc=True, chroma=True, mel=True):
    """Identical to the feature extractor used in the training notebook."""
    X, sr = librosa.load(file_path, sr=22050)
    result = np.array([])
    stft = np.abs(librosa.stft(X))
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sr, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
    if chroma:
        chroma_f = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T, axis=0)
        result = np.hstack((result, chroma_f))
    if mel:
        mel_f = np.mean(librosa.feature.melspectrogram(y=X, sr=sr).T, axis=0)
        result = np.hstack((result, mel_f))
    return result


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "audio_file" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files["audio_file"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type. Please upload a .wav, .mp3, .ogg or .flac file."}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        features = extract_feature(file_path)
        features_scaled = (features - FEATURE_MEAN) / FEATURE_STD
        features_scaled = features_scaled.reshape(1, -1)

        probs = model.predict(features_scaled, verbose=0)[0]
        pred_idx = int(np.argmax(probs))
        pred_label = label_encoder.inverse_transform([pred_idx])[0]

        breakdown = sorted(
            [
                {"emotion": label_encoder.classes_[i], "probability": round(float(p) * 100, 2)}
                for i, p in enumerate(probs)
            ],
            key=lambda x: x["probability"],
            reverse=True,
        )

        return jsonify({
            "prediction": pred_label,
            "emoji": EMOJI_MAP.get(pred_label, ""),
            "confidence": round(float(probs[pred_idx]) * 100, 2),
            "breakdown": breakdown,
        })
    except Exception as exc:
        return jsonify({"error": f"Could not process the audio file: {exc}"}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    # Turn debug on locally if you're poking at the code; leave off by default
    # so the interactive debugger/reloader doesn't accidentally ship enabled.
    app.run(debug=False, port=5000)
