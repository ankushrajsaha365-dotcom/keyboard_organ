import numpy as np
import sounddevice as sd
from pynput import keyboard
import string
import threading
import signal

SAMPLE_RATE = 44100
AMPLITUDE = 0.15
BASE_FREQ = 200
FREQ_STEP = 20

active_freqs = set()
lock = threading.Lock()
running = True

def audio_callback(outdata, frames, time, status):
    t = np.arange(frames) / SAMPLE_RATE
    buffer = np.zeros(frames)

    with lock:
        for freq in active_freqs:
            buffer += np.sin(2 * np.pi * freq * t)

    outdata[:, 0] = buffer * AMPLITUDE

def on_press(key):
    global running
    try:
        if key == keyboard.Key.esc:
            running = False
            return False

        if hasattr(key, "char") and key.char:
            c = key.char.lower()
            if c in string.ascii_lowercase:
                freq = BASE_FREQ + (ord(c) - ord('a')) * FREQ_STEP
                with lock:
                    active_freqs.add(freq)
    except:
        pass

def on_release(key):
    try:
        if hasattr(key, "char") and key.char:
            c = key.char.lower()
            if c in string.ascii_lowercase:
                freq = BASE_FREQ + (ord(c) - ord('a')) * FREQ_STEP
                with lock:
                    active_freqs.discard(freq)
    except:
        pass

# Ignore Ctrl+Z
signal.signal(signal.SIGTSTP, signal.SIG_IGN)

print("🔊 ASCII POLYPHONIC TEST")
print("Hold keys A–Z | ESC to exit")

with sd.OutputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    callback=audio_callback,
):
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=True
    ) as listener:
        while running:
            pass
