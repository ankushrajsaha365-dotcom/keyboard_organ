import numpy as np
import sounddevice as sd
from pynput import keyboard
import string
import threading
import signal

SAMPLE_RATE = 44100
AMPLITUDE = 0.15

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
                freq = 200 + (ord(c) - 97) * 20
                with lock:
                    active_freqs.add(freq)
    except:
        pass

def on_release(key):
    try:
        if hasattr(key, "char") and key.char:
            c = key.char.lower()
            if c in string.ascii_lowercase:
                freq = 200 + (ord(c) - 97) * 20
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
    from pynput import keyboard
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=True
    ) as listener:
        while running:
            pass
