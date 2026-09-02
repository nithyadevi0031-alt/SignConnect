# SIGNCONNECT AI

"Breaking Communication Barriers"

## Project Overview

SIGNCONNECT AI is a polished desktop demo for Indian Sign Language (ISL) accessibility. The app accepts speech or text input, maps supported phrases to ISL video files, and plays the selected sign inside the application.

## Problem Statement

Sign language demos often rely on placeholder animations or research prototypes. This project is built as a stable demonstration-ready ISL video player that keeps the current functionality simple while preparing for future machine learning upgrades.

## Features

- Speech-to-text input using `sounddevice` + `SpeechRecognition`
- Text input translation for supported ISL phrases
- Embedded ISL video playback with play/pause/replay controls
- Quick sign buttons for the eight demo phrases
- Dictionary-driven ISL video mapping via `data/sign_dictionary.json`
- Recent translation history for the last 3 signs
- Friendly missing-video handling with source attribution
- Professional dark teal dashboard UI

## System Architecture

1. Speech / Text input
2. Text preprocessing and normalization
3. Sign lookup in `data/sign_dictionary.json`
4. Load corresponding ISL MP4 video from `signs/`
5. Play video inside the Tkinter application

## Technology Stack

- Python 3
- Tkinter
- Pillow
- SpeechRecognition
- sounddevice
- numpy
- python-vlc

## Folder Structure

```
SIGNCONNECT/
+-- main.py
+-- requirements.txt
+-- README.md
+-- data/
¦   +-- sign_dictionary.json
+-- signs/
+-- assets/
+-- ml/
    +-- README.md
```

- `main.py`: Main desktop application and ISL video player
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation
- `data/sign_dictionary.json`: ISL video mappings and source URLs
- `signs/`: Place actual ISL MP4 files here
- `assets/`: Optional icons or resources
- `ml/README.md`: Future machine learning architecture

## Installation

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

## VLC Requirement

The application uses `python-vlc` to play videos inside the GUI. You also need VLC Media Player installed on your system.

- Windows: Install VLC from https://www.videolan.org/
- macOS/Linux: Install VLC from your package manager or official website

## Run the Project

From the project folder, run:

```bash
python main.py
```

## Speech Input

1. Click `START LISTENING`
2. Speak a supported phrase like `Hello` or `Thank You`
3. Recognized text appears in the speech box
4. Click `TRANSLATE` to load the ISL video

If speech recognition fails, the app displays a clear warning and text input remains available.

## Text Input

Type a supported phrase such as `Hello`, `Yes`, `No`, `Thank You`, `Sorry`, `Help`, `Emergency`, or `Hospital`, then click `TRANSLATE`.

## ISL Video Output

The center panel plays the corresponding ISL MP4 video inside the application. If a sign video is missing, the app displays a clear warning message and the source URL for the expected ISL resource.

## Quick Signs

The right panel contains quick sign buttons for the eight demo phrases. Clicking a quick sign immediately loads and plays the corresponding video.

## ISL Video Sources

This project is grounded in legitimate ISL resources such as the ISLRTC dictionary:

- ISLRTC ISL Dictionary: https://islrtc.nic.in/isl-dictionary/

All supported phrases are mapped to ISLRTC-style video entries in `data/sign_dictionary.json`.

## Current Limitations

- The app does not perform automatic sign recognition from camera input.
- The current demo uses a dictionary mapping to ISL video files.
- Actual ISL videos must be placed in `signs/` manually if not already available.

## Future Scope

- Camera capture with MediaPipe Holistic
- CNN-based feature extraction for hand landmarks
- LSTM for temporal sign sequence processing
- Transformer-based contextual ISL recognition
- Sign-to-text recognition pipeline

## How to Add a New Sign

1. Place a new MP4 file in the `signs/` folder.
2. Add the mapping to `data/sign_dictionary.json`, for example:

```json
"hello": {
  "video": "signs/hello.mp4",
  "language": "ISL",
  "source": "https://islrtc.nic.in/isl-dictionary/"
}
```

3. Restart the app.
4. Use the new phrase in the text input or add a quick sign button.
