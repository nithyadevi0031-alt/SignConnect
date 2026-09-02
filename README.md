# 🤟 SIGNCONNECT AI

<h3 align="center">
  🌐 Breaking Communication Barriers with Technology
</h3>

<p align="center">
  <b>
    An accessibility-focused Indian Sign Language communication platform
    designed to make everyday communication simpler, more inclusive, and more connected.
  </b>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF6F00?style=for-the-badge)
![ISL](https://img.shields.io/badge/Language-Indian%20Sign%20Language-7B1FA2?style=for-the-badge)
![VLC](https://img.shields.io/badge/Video-python--vlc-FF8800?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Hackathon%20Prototype-00C853?style=for-the-badge)
![License](https://img.shields.io/badge/License-Hackathon%20Prototype-blue?style=for-the-badge)

</p>

<p align="center">

⭐ <b>Accessibility</b> •
🤟 <b>Indian Sign Language</b> •
🎤 <b>Speech Input</b> •
⌨️ <b>Text Input</b> •
🎬 <b>ISL Video Output</b>

</p>

---

# 🌟 INTRODUCTION

Communication is one of the most fundamental ways in which people connect, understand one another, and participate in society. However, communication can become challenging when people rely on different communication methods.

**SignConnect AI** was created with a simple idea:

> ### 💙 Technology should connect people, not create another barrier.

SignConnect is an accessibility-focused desktop application designed around **Indian Sign Language (ISL)**. The current prototype allows a user to provide a phrase through **speech or text**, processes the input, searches a structured ISL dictionary, and displays the corresponding sign-language video directly inside the application.

Rather than presenting sign-language resources as disconnected videos or static references, SignConnect brings them together into a **single interactive communication interface**.

The project is also designed with a larger vision in mind. The present dictionary-driven prototype establishes the foundation for a future intelligent system capable of incorporating **computer vision, hand-landmark detection, temporal sequence modelling, and real-time sign recognition**.

---

# 🎯 THE PROBLEM

People who communicate primarily through sign language can face difficulties when interacting with individuals who do not understand sign language.

This can affect everyday situations such as:

- 🏥 Healthcare communication
- 🏫 Educational environments
- 🏢 Workplace interaction
- 🚨 Emergency situations
- 🛍️ Public services
- 👨‍👩‍👧 Everyday conversations

Although Indian Sign Language resources are available, accessing the correct sign for a particular phrase can still require searching through external resources.

### ❗ The challenge

How can we create a simple technology interface that allows a person to enter a common phrase and quickly receive its corresponding **Indian Sign Language representation**?

### 💡 Our answer

**SignConnect AI.**

---

# 💡 OUR SOLUTION

SignConnect provides a unified interface that connects different forms of communication with Indian Sign Language resources.

The current prototype follows:

```text
        🎤 SPEECH
           │
           │
           ▼
    📝 SPEECH-TO-TEXT
           │
           │
           ├──────────────┐
           │              │
           ▼              ▼
      🔤 TEXT INPUT   ⌨️ DIRECT TEXT
           │              │
           └──────┬───────┘
                  │
                  ▼
          🧹 TEXT PROCESSING
                  │
                  ▼
         📖 ISL DICTIONARY
                  │
                  ▼
          🔎 PHRASE LOOKUP
                  │
                  ▼
          🎬 VIDEO MAPPING
                  │
                  ▼
           🤟 ISL OUTPUT
