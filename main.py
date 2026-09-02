import os
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk

try:
    import vlc
except ImportError:
    vlc = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import sounddevice as sd
    import numpy as np
except ImportError:
    sd = None
    np = None


class SignConnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SIGNCONNECT AI")
        self.root.geometry("1120x700")
        self.root.configure(bg="#071B20")
        self.root.minsize(1024, 660)

        self.base_path = Path(__file__).resolve().parent
        self.sign_data = {
            "hello": "signs/hello.mp4",
            "yes": "signs/Yes.mp4",
            "no": "signs/No.mp4",
            "thank you": "signs/Thank_You.mp4",
            "thankyou": "signs/Thank_You.mp4",
            "sorry": "signs/sorry.mp4",
            "help": "signs/help.mp4",
            "emergency": "signs/Emergency.mp4",
            "hospital": "signs/Hospital.mp4",
        }

        self.vlc_available = False
        self.vlc_instance = None
        self.vlc_player = None
        self.vlc_media = None
        self._initialize_vlc()

        self.current_input_var = tk.StringVar(value="Ready to translate")
        self.current_output_var = tk.StringVar(value="Waiting for input")
        self.status_var = tk.StringVar(value="STATUS: READY")
        self.speech_status_var = tk.StringVar(value="Speech ready")

        self._create_styles()
        self._build_ui()
        self.clear()
        self.set_status("READY")

    def _initialize_vlc(self):
        if vlc is None:
            print("[VIDEO] python-vlc not installed")
            return
        try:
            self.vlc_instance = vlc.Instance()
            self.vlc_player = self.vlc_instance.media_player_new()
            self.vlc_available = True
            print("[VIDEO] VLC/libVLC initialized")
        except Exception as exc:
            self.vlc_available = False
            print(f"[VIDEO] VLC initialization failed: {exc}")

    def _create_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#071B20")
        style.configure("Header.TLabel", background="#071B20", foreground="#FFFFFF", font=("Segoe UI", 20, "bold"))
        style.configure("SubHeader.TLabel", background="#071B20", foreground="#A8C5CA", font=("Segoe UI", 12))
        style.configure("Panel.TFrame", background="#12333B", relief="flat")
        style.configure("Section.TLabel", background="#12333B", foreground="#FFFFFF", font=("Segoe UI", 12, "bold"))
        style.configure("Body.TLabel", background="#12333B", foreground="#A8C5CA", font=("Segoe UI", 10))
        style.configure("Accent.TButton", background="#00E6C3", foreground="#071B20", font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#2BFFE0"), ("disabled", "#1A616E")])
        style.configure("TButton", background="#1B4149", foreground="#FFFFFF", font=("Segoe UI", 10), borderwidth=0)
        style.configure("Status.TLabel", background="#071B20", foreground="#A8C5CA", font=("Segoe UI", 10, "italic"))

    def _build_ui(self):
        header = ttk.Frame(self.root, style="TFrame")
        header.pack(fill="x", padx=20, pady=(16, 8))

        title = ttk.Label(header, text="SIGNCONNECT AI", style="Header.TLabel")
        title.pack(anchor="w")
        subtitle = ttk.Label(header, text="Breaking Communication Barriers", style="SubHeader.TLabel")
        subtitle.pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(self.root, style="TFrame")
        body.pack(fill="both", expand=True, padx=20)

        left_panel = ttk.Frame(body, style="Panel.TFrame")
        center_panel = ttk.Frame(body, style="Panel.TFrame")
        right_panel = ttk.Frame(body, style="Panel.TFrame")

        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        center_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        right_panel.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        self._build_input_panel(left_panel)
        self._build_output_panel(center_panel)
        self._build_quick_signs_panel(right_panel)

        status_frame = ttk.Frame(self.root, style="TFrame")
        status_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.pack(anchor="w")

    def _build_input_panel(self, parent):
        heading = ttk.Label(parent, text="TEXT INPUT", style="Section.TLabel")
        heading.pack(anchor="w", padx=10, pady=(10, 8))

        self.input_text = tk.Text(parent, height=12, wrap="word", bg="#0B1F26", fg="#FFFFFF", insertbackground="#00E6C3", bd=0, highlightthickness=1, highlightbackground="#0F3E4C", font=("Segoe UI", 11))
        self.input_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        button_frame = ttk.Frame(parent, style="TFrame")
        button_frame.pack(fill="x", padx=10)

        translate_button = ttk.Button(button_frame, text="TRANSLATE", style="Accent.TButton", command=self.translate)
        translate_button.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 6))
        clear_button = ttk.Button(button_frame, text="CLEAR", style="TButton", command=self.clear)
        clear_button.pack(side="left", fill="x", expand=True, ipady=10)

        speech_label = ttk.Label(parent, text="Speech Input", style="Body.TLabel")
        speech_label.pack(anchor="w", padx=10, pady=(14, 4))

        self.listen_button = ttk.Button(parent, text="START LISTENING", style="Accent.TButton", command=self.start_listening)
        self.listen_button.pack(fill="x", padx=10, pady=(0, 10), ipady=10)

        self.speech_status = ttk.Label(parent, textvariable=self.speech_status_var, style="Body.TLabel")
        self.speech_status.pack(anchor="w", padx=10, pady=(0, 6))

    def _build_output_panel(self, parent):
        heading = ttk.Label(parent, text="SIGN OUTPUT", style="Section.TLabel")
        heading.pack(anchor="w", padx=10, pady=(10, 8))

        self.current_input_label = ttk.Label(parent, textvariable=self.current_input_var, style="Header.TLabel", wraplength=360, justify="left")
        self.current_input_label.pack(anchor="w", padx=10, pady=(0, 8))

        self.current_output_label = ttk.Label(parent, textvariable=self.current_output_var, style="Header.TLabel", wraplength=360, justify="left")
        self.current_output_label.pack(anchor="w", padx=10, pady=(0, 14))

        video_frame = ttk.Frame(parent, style="SecondaryPanel.TFrame")
        video_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        video_frame.configure(style="Panel.TFrame")

        self.video_container = tk.Frame(video_frame, bg="#0B1F26")
        self.video_container.pack(fill="both", expand=True, padx=8, pady=8)

        self.video_message = ttk.Label(self.video_container, text="ISL VIDEO WILL APPEAR HERE", style="Body.TLabel", justify="center")
        self.video_message.place(relx=0.5, rely=0.5, anchor="center")

        controls = ttk.Frame(parent, style="TFrame")
        controls.pack(fill="x", padx=10)

        play_button = ttk.Button(controls, text="▶ PLAY", style="Accent.TButton", command=self.play_video)
        play_button.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 6))
        pause_button = ttk.Button(controls, text="⏸ PAUSE", style="Accent.TButton", command=self.pause_video)
        pause_button.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 6))
        replay_button = ttk.Button(controls, text="⟳ REPLAY", style="Accent.TButton", command=self.replay_video)
        replay_button.pack(side="left", fill="x", expand=True, ipady=10)

    def _build_quick_signs_panel(self, parent):
        heading = ttk.Label(parent, text="QUICK SIGNS", style="Section.TLabel")
        heading.pack(anchor="w", padx=10, pady=(10, 8))

        quick_signs = [
            ("HELLO", "hello"),
            ("YES", "yes"),
            ("NO", "no"),
            ("THANK YOU", "thank you"),
            ("SORRY", "sorry"),
            ("HELP", "help"),
            ("EMERGENCY", "emergency"),
            ("HOSPITAL", "hospital"),
        ]

        for label, key in quick_signs:
            button = ttk.Button(parent, text=label, style="Accent.TButton", command=lambda value=key: self.quick_sign(value))
            button.pack(fill="x", padx=10, pady=6, ipady=10)

    def translate(self):
        raw_text = self.input_text.get("1.0", "end").strip()
        if not raw_text:
            self.set_status("INPUT REQUIRED")
            return

        cleaned = self._normalize_text(raw_text)
        sign_key = self._find_sign_key(cleaned)
        self.current_input_var.set(raw_text.strip().title())

        if sign_key is None:
            self.current_output_var.set("SIGN NOT AVAILABLE")
            self._show_video_message("ISL VIDEO NOT AVAILABLE")
            self.set_status("VIDEO NOT FOUND")
            return

        self.current_output_var.set(sign_key.upper())
        self._show_video_message("Loading video...")
        self.load_video(self.base_path / self.sign_data[sign_key])

    def clear(self):
        self.input_text.delete("1.0", "end")
        self.current_input_var.set("Ready to translate")
        self.current_output_var.set("Waiting for input")
        self.speech_status_var.set("Speech ready")
        self._show_video_message("ISL VIDEO WILL APPEAR HERE")
        self.set_status("READY")
        self._stop_video()

    def quick_sign(self, sign):
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", sign)
        self.current_input_var.set(sign.title())
        self.current_output_var.set(sign.upper())
        self._show_video_message("Loading video...")
        self.load_video(self.base_path / self.sign_data.get(sign, ""))

    def load_video(self, path):
        video_name = path.stem if path else "unknown"
        print(f"[VIDEO] Input: {video_name}")
        print(f"[VIDEO] Path: {path}")

        actual_path = self._resolve_video_path(path)
        exists = bool(actual_path and actual_path.exists())
        print(f"[VIDEO] Exists: {exists}")
        if actual_path and actual_path != path:
            print(f"[VIDEO] Fallback Path: {actual_path}")

        if not actual_path or not exists:
            self._show_video_message(f"ISL VIDEO NOT AVAILABLE\nExpected:\n{path}")
            self.set_status("VIDEO NOT FOUND")
            return

        if not self.vlc_available:
            self._show_video_message("VLC/libVLC not available")
            self.set_status("VIDEO ERROR")
            return

        try:
            self._stop_video()
            media = self.vlc_instance.media_new(str(actual_path))
            self.vlc_player.set_media(media)
            self._set_video_window()
            self._show_video_message("")
            result = self.vlc_player.play()
            if result == -1:
                raise RuntimeError("VLC failed to start playback")
            self.set_status(f"Playing ISL sign: {video_name.upper()}")
            print("[VIDEO] Playing...")
        except Exception as exc:
            print(f"[VIDEO] Playback failed: {exc}")
            self._show_video_message("ISL VIDEO NOT AVAILABLE")
            self.set_status("VIDEO ERROR")

    def play_video(self):
        if not self.vlc_available or self.vlc_player is None:
            self._show_video_message("Video playback unavailable.\nPlease install VLC Media Player.")
            self.set_status("VLC UNAVAILABLE")
            return
        try:
            self.vlc_player.play()
            self.set_status("VIDEO PLAYING")
        except Exception:
            self.set_status("VIDEO ERROR")

    def pause_video(self):
        if self.vlc_available and self.vlc_player is not None:
            try:
                self.vlc_player.pause()
                self.set_status("VIDEO PAUSED")
            except Exception:
                self.set_status("VIDEO ERROR")

    def replay_video(self):
        if self.vlc_available and self.vlc_player is not None:
            try:
                self.vlc_player.stop()
                self.vlc_player.play()
                self.set_status("VIDEO PLAYING")
            except Exception:
                self.set_status("VIDEO ERROR")

    def start_listening(self):
        if sr is None or sd is None or np is None:
            self.speech_status_var.set("Speech recognition unavailable. Use text input.")
            self.set_status("SPEECH ERROR")
            return

        self.listen_button.config(state="disabled")
        self.speech_status_var.set("Listening...")
        self.set_status("LISTENING")
        threading.Thread(target=self._listen_in_background, daemon=True).start()

    def set_status(self, message):
        self.status_var.set(f"STATUS: {message}")

    def _normalize_text(self, text):
        value = text.lower().strip()
        value = " ".join(value.split())
        return value

    def _find_sign_key(self, text):
        if not text:
            return None
        for key in sorted(self.sign_data.keys(), key=len, reverse=True):
            if key in text:
                return key
        return None

    def _set_video_window(self):
        if not self.vlc_available or self.vlc_player is None:
            return
        handle = self.video_container.winfo_id()
        try:
            if os.name == "nt":
                self.vlc_player.set_hwnd(handle)
            else:
                self.vlc_player.set_xwindow(handle)
        except Exception:
            pass

    def _stop_video(self):
        if self.vlc_available and self.vlc_player is not None:
            try:
                self.vlc_player.stop()
            except Exception:
                pass

    def _show_video_message(self, message):
        self.video_message.config(text=message)
        if message:
            self.video_message.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.video_message.place_forget()

    def _resolve_video_path(self, path):
        if not path:
            return None
        if path.exists():
            return path

        video_dir = path.parent
        expected_name = path.name.lower()
        for candidate in video_dir.iterdir():
            if candidate.is_file() and candidate.name.lower() == expected_name:
                return candidate
        for candidate in video_dir.iterdir():
            if candidate.is_file() and candidate.name.lower().startswith(path.stem.lower()):
                return candidate
        return None

    def _listen_in_background(self):
        try:
            duration = 4
            sample_rate = 16000
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
            sd.wait()
            if recording is None or recording.size == 0:
                raise RuntimeError("No audio captured")
            audio_data = sr.AudioData(recording.tobytes(), sample_rate, 2)
            transcript = sr.Recognizer().recognize_google(audio_data)
            self.root.after(0, self._finish_speech, transcript)
        except Exception:
            self.root.after(0, self._finish_speech, None)

    def _finish_speech(self, transcript):
        if transcript:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", transcript)
            self.speech_status_var.set("Speech captured")
            self.set_status("SPEECH READY")
        else:
            self.speech_status_var.set("Speech recognition unavailable. Use text input.")
            self.set_status("SPEECH ERROR")
        self.listen_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    SignConnectApp(root)
    root.mainloop()
