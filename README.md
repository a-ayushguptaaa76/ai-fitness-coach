# AI Fitness Coach

An independently built computer-vision fitness assistant that estimates body pose from a webcam or video, counts repetitions for supported exercises, and displays simple workout feedback.

## Features

- Live pose landmarks with MediaPipe
- Rep counting for squats, push-ups, and bicep curls
- Basic movement-phase tracking and angle-based feedback
- Session summary with repetition counts and elapsed time
- Local processing: camera frames are not uploaded by this app

## Tech stack

- Python 3.10–3.12
- OpenCV
- MediaPipe
- NumPy

## Quick start

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Allow camera access when prompted. Press `q` to exit the camera window. Choose an exercise in the terminal before the camera opens.

## Project structure

```text
ai-fitness-coach/
├── app.py                 # Webcam loop and user interaction
├── fitness_coach/
│   ├── __init__.py
│   ├── angles.py           # Joint-angle helpers
│   └── exercises.py        # Exercise state and feedback logic
├── tests/
│   └── test_angles.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Supported exercises and limitations

The initial version uses heuristic, 2D landmark angles. It is a learning/demo tool, not a medical device or a substitute for a qualified trainer. Camera placement, lighting, loose clothing, and partial visibility can affect estimates. Feedback is intentionally basic and should not be treated as a guarantee that an exercise is safe or correctly performed.

## Development

```bash
python -m unittest discover -s tests -v
```

Contributions and bug reports are welcome. If you extend exercise support, add unit tests for the movement-state transitions and document the camera angle that works best.
