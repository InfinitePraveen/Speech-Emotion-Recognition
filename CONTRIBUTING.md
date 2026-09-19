# Contributing

Thanks for taking a look at this project! It started as a personal learning
exercise, but I'm happy to take contributions, bug reports, or suggestions.

## Ways to help

- **Bug reports** — if the web app crashes on a certain audio file, or a
  notebook cell errors out, open an issue with the file (or a way to
  reproduce it) and the full traceback.
- **Model improvements** — better architectures, augmentation ideas, or a
  swap to a stronger dataset are all welcome. See the "Ideas for improvement"
  section in the README for a starting list.
- **Web app polish** — UI tweaks, better error handling, drag-and-drop
  improvements, etc.
- **Docs** — if something in the README or notebooks was confusing to
  follow, let me know or send a fix directly.

## Getting set up locally

```bash
git clone https://github.com/InfinitePraveen/speech-emotion-recognition.git
cd speech-emotion-recognition
pip install -r requirements.txt
```

Download RAVDESS into `data/RAVDESS/` (see README for the link and expected
folder layout) if you plan on touching anything related to training.

To just run the web app without retraining anything, you can skip the
dataset — the checked-in demo model under `app/model/` is enough:

```bash
cd app
python app.py
```

## Making a change

1. Fork the repo and create a branch off `main`:
   `git checkout -b fix/short-description`
2. Make your change. If it touches the model or feature extraction, please
   re-run the relevant notebook(s) so the outputs in the diff reflect what
   actually happened.
3. Keep commits focused — one logical change per commit is easier to review
   than one giant commit.
4. Update `CHANGELOG.md` under an "Unreleased" heading describing what
   changed.
5. Open a pull request with a short description of the change and, if it's
   a visual change to the web app, a screenshot.

## Code style

- Python: keep it close to [PEP 8](https://peps.python.org/pep-0008/);
  no strict linter enforced, just keep it readable.
- Notebooks: clear outputs of huge intermediate arrays before committing
  where possible, but it's fine to keep the trained plots/metrics so
  reviewers can see the results without re-running everything.
- Keep the repo structure flat and simple — this project intentionally
  avoids a `src/` package; new logic should live in a notebook or directly
  in `app/app.py` unless there's a strong reason otherwise.

## Reporting issues

Please include:
- What you expected to happen vs. what actually happened
- Python version and OS
- Full error message / traceback
- Steps to reproduce (a sample audio file helps a lot if it's app-related)

## Code of conduct

Be respectful, assume good intent, and keep feedback constructive. This is a
learning project — questions are always welcome.
