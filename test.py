import sounddevice as sd
import numpy as np

print(sd.query_devices())

tone = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 44100))
sd.play(tone, 44100)
sd.wait()
