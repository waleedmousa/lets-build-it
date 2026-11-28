# Try the same trick on your own music.
#   python my_songs.py  song1.wav song2.wav ...  --clip mystery.wav
# The songs become the library; the clip is what we try to name.
# WAV files only (16-bit). Any length, mono or stereo. No extra installs.
import sys, wave
import numpy as np
import shazam as z

def load(path):
    with wave.open(path) as f:
        sound = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(float)
        sound = sound.reshape(-1, f.getnchannels()).mean(axis=1)          # stereo -> mono
        step = f.getframerate() / z.RATE                                    # resample to 8000
    sound = np.interp(np.arange(int(len(sound) / step)) * step, np.arange(len(sound)), sound)
    return sound / (np.abs(sound).max() or 1)

if "--clip" not in sys.argv or len(sys.argv) < 4:
    sys.exit("usage: python my_songs.py song1.wav song2.wav ... --clip mystery.wav")
songs = sys.argv[1:sys.argv.index("--clip")]
clip = sys.argv[sys.argv.index("--clip") + 1]

z.library.clear()                                       # forget the invented songs
for path in songs:
    for mark, time in z.fingerprints(load(path)):
        z.library.setdefault(mark, []).append((path, time))
print(sum(len(p) for p in z.library.values()), "fingerprints remembered from", len(songs), "songs")

name, start, score = z.name_that_tune(load(clip))
print(f"I heard: {name}, starting at second {start:.1f}  ({score} fingerprints agree)")
