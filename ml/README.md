# Machine Learning Architecture Roadmap

This `ml/README.md` describes the future architecture for Indian Sign Language recognition and translation.

## Current Demo

The current `SIGNCONNECT AI` demo is a reliable prototype:

- Speech input through `sounddevice` + `SpeechRecognition`
- Text preprocessing and supported sign lookup
- ISL video selection from a dictionary
- Embedded video playback in the desktop app

This demo does not perform real-time sign recognition or advanced deep learning.

## Future Architecture

Planned machine learning modules for future versions:

1. Camera capture
2. MediaPipe Holistic
   - Hand landmarks
   - Body landmarks
   - Face landmarks
3. CNN for visual feature extraction
4. LSTM for temporal sequence modeling
5. Transformer for sentence context and translation
6. ISL recognition
7. Text or speech output

## Future Sign-to-Text Flow

Camera → MediaPipe → Landmark sequences → CNN → LSTM → Transformer → ISL recognition → Text/Speech

## Notes

- No CNN/LSTM/Transformer is implemented in the current version.
- The current app remains a dictionary-based demo with clear separation from future ML functionality.
