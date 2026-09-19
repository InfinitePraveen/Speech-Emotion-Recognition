# 🎙️ Speech Emotion Recognition

Classify the emotion behind a spoken audio clip — *neutral, calm, happy, sad,
angry, fearful, disgust,* or *surprised* — using MFCC / Chroma / Mel-spectrogram
features and a deep neural network built with Keras.

This started as a way for me to get hands-on with audio processing (something
I hadn't touched much beyond CS50's intro material) and ended up being one of
my favorite projects to demo — there's something satisfying about uploading a
clip and watching the model actually guess the mood right.

**Repo:** https://github.com/InfinitePraveen/Speech-Emotion-Recognition

---

## Requirements

- **Python 3.11**
- A stable internet connection while running the notebooks (see below on why)

---

## Demo

A small Flask web app is included so this isn't just notebooks sitting in a
folder — you can drag in an audio clip (or use one of the bundled samples)
and see the prediction + confidence breakdown live.

```bash
cd app
pip install -r ../requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000**.

---

## How it works

```
Audio clip (.wav)
      │
      ▼
librosa: MFCC (40) + Chroma (12) + Mel-spectrogram (128)  →  180-d feature vector
      │
      ▼
Feed-forward neural network (Dense 256 → 128 → 64 → softmax)
      │
      ▼
Predicted emotion + per-class confidence
```

The feature extraction step is the same function used both when training
(`notebooks/02_feature_extraction_and_model_training.ipynb`) and when serving
predictions in the Flask app (`app/app.py`), so there's no train/serve skew.

---

## Dataset

Trained against [RAVDESS](https://zenodo.org/record/1188976) (Ryerson
Audio-Visual Database of Emotional Speech and Song) — 24 professional actors
speaking the same lines with 8 different emotions. It's a nice dataset to
start with because it's clean, balanced, and doesn't need much cleanup.

**No local download required.** The full archive is ~25 GB, which isn't
something everyone has room for, so `01_data_exploration.ipynb` and
`02_feature_extraction_and_model_training.ipynb` pull audio **on demand**
straight from Zenodo using `requests`, reading each clip's bytes into memory,
processing it, and discarding it — nothing is written to disk and the zip is
never fully downloaded. This means:

- You need an internet connection while running those notebooks
- Feature extraction over the full dataset will be slower than reading from
  local disk (bounded by your download speed, not just CPU)
- If a request to Zenodo times out or gets rate-limited, just re-run the cell

> **Note on the shipped model:** the model file checked into `app/model/`
> was trained on a small synthetically generated stand-in dataset (same
> feature pipeline, generated audio) just so the app runs out of the box for
> a demo. **Run the notebooks against the real RAVDESS data for a model
> you'd actually trust the accuracy numbers on.** The sample clips under
> `app/static/sample_audio/` are from that same synthetic set, purely for
> convenience when demoing.

Swapping in [TESS](https://tspace.library.utoronto.ca/handle/1807/24487) or
[CREMA-D](https://github.com/CheyneyComputerScience/CREMA-D) instead just
means adjusting the filename-parsing logic and source URL in notebook 02 —
the rest of the pipeline doesn't care where the features came from.

---

## Repository structure

```
speech-emotion-recognition/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── requirements.txt
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_extraction_and_model_training.ipynb
│   └── 03_inference_demo.ipynb
├── app/
│   ├── app.py                ← Flask app
│   ├── templates/index.html
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/script.js
│   │   └── sample_audio/     ← demo clips for the "try a sample" buttons
│   └── model/                ← trained model + label encoder + scaler
```

Everything model-related lives in the notebooks on purpose — no separate
`src/` package to keep the repo approachable for anyone skimming it before
an interview. There's no `data/` folder anymore either, since the dataset is
streamed rather than stored locally.

---

## Running the notebooks

```bash
pip install -r requirements.txt
jupyter notebook notebooks/
```

1. **`01_data_exploration.ipynb`** — stream a handful of clips straight from
   Zenodo, look at class balance, listen to a couple of them, eyeball
   waveforms/spectrograms.
2. **`02_feature_extraction_and_model_training.ipynb`** — stream every clip,
   extract MFCC/Chroma/Mel features on the fly, train the neural network,
   evaluate it (confusion matrix, classification report), and export the
   model artifacts into `app/model/`.
3. **`03_inference_demo.ipynb`** — the shortest one: load the exported model
   and run a single prediction, exactly like the web app does.

---

## Results

On the held-out split of the (synthetic, demo-only) training run, the model
reaches ~90%+ accuracy — see the confusion matrix at the bottom of notebook
02 for the per-class breakdown. Expect a different, more realistic number
once you retrain on real RAVDESS audio; emotions like *calm* vs *neutral* and
*fearful* vs *surprised* tend to be the hardest pairs to separate in most
published SER work.

---

## Ideas for improvement

- Swap the pooled-feature MLP for a CNN or CNN-LSTM over the raw MFCC
  time-series (no time-averaging) to capture temporal dynamics
- Data augmentation: pitch shifting, time stretching, adding background noise
- Combine RAVDESS + TESS + CREMA-D for more speaker diversity
- Try wav2vec2 / HuBERT embeddings instead of hand-crafted MFCC features
- Add a live microphone recording option to the web app instead of only file upload
- Cache streamed clips locally (with an opt-in flag) to speed up repeated runs

---

## Tech stack

`Python 3.11` · `librosa` · `TensorFlow / Keras` · `scikit-learn` · `Flask` · `requests`

---

## Author

**Praveen**
Data science & ML portfolio project.

- GitHub: [InfinitePraveen](https://github.com/InfinitePraveen)
- LinkedIn: [infinitepraveen](https://www.linkedin.com/in/infinitepraveen)

Contributions and suggestions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
