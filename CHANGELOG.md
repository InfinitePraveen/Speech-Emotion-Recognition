# Changelog

All notable changes to this project are documented in this file.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project doesn't currently follow strict semantic versioning since
it's a portfolio/learning project rather than a published package.

## [Unreleased]

- Consider adding a live microphone recording option to the web app
- Consider augmenting training data with pitch/time-stretch variants

## [1.1.0] - 2026-09-19

### Added
- `03_inference_demo.ipynb` — a short notebook that loads the exported model
  and runs a single prediction end-to-end, mirroring what the Flask app does
- Sample audio clips bundled under `app/static/sample_audio/` with one-click
  "try a sample" buttons in the web UI, so the app is demoable without
  needing to hunt for a test file first
- Per-class confidence breakdown in the prediction response, rendered as
  bars under the main result in the UI

### Changed
- Reworked the web app UI: drag-and-drop upload zone, loading state, and a
  cleaner result card instead of a plain text response
- Feature scaling (mean/std) is now saved alongside the model
  (`app/model/scaler.pkl`) instead of being recomputed ad hoc, so
  train-time and serve-time normalization are guaranteed to match

### Fixed
- Uploaded files are now deleted from `app/uploads/` after prediction
  instead of accumulating on disk

## [1.0.0] - 2026-08-30

### Added
- Initial project structure: `notebooks/`, `app/`, `data/`
- `01_data_exploration.ipynb` — dataset loading, class balance, waveform and
  mel-spectrogram visualization
- `02_feature_extraction_and_model_training.ipynb` — MFCC + Chroma + Mel
  feature extraction, Keras MLP training, evaluation (confusion matrix,
  classification report), and model export
- Basic Flask app (`app/app.py`) with a single upload form and text-based
  prediction output
- README with dataset instructions and project overview
