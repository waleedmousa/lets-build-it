# Every test from the video. Run:  python break_it.py   (takes a minute or two)
import numpy as np
from collections import Counter
import shazam as z

R = z.RATE

def faster(clip, speed):                               # play a clip faster
    return np.interp(np.arange(int(len(clip) / speed)) * speed, np.arange(len(clip)), clip)

def count_every_match(clip):                           # the first idea, the one that fails
    matches = Counter()
    for mark, time in z.fingerprints(clip):
        for name, song_time in z.library.get(mark, []):
            matches[name] += 1
    return matches.most_common(1)[0][0]

def final(clip):                                       # the fix: only matches that agree on when
    return z.name_that_tune(clip)[0]

def score(guess, seconds=3.0, noise=z.NOISE, speed=None):
    dice = np.random.default_rng(1)                    # same 200 random clips every run
    right = 0
    for _ in range(200):
        number = int(dice.integers(len(z.NAMES)))
        start = int(float(dice.uniform(0, 30 - seconds)) * R)
        clip = z.make_song(number)[start:start + int(seconds * R)]
        clip = faster(clip, speed) if speed else clip + noise * dice.normal(size=len(clip))
        try:
            right += guess(clip) == z.NAMES[number]
        except (ValueError, IndexError):
            pass                                       # no match at all counts as wrong
    return right

print("count every match          :", score(count_every_match), "of 200")
print("only matches that agree    :", score(final), "of 200")
print("half a second of sound     :", score(final, seconds=0.5), "of 200")
print("a fifth of a second        :", score(final, seconds=0.2), "of 200")
print("noise 4x stronger          :", score(final, noise=4.0), "of 200")
print("played 5% faster, no noise :", score(final, speed=1.05), "of 200")
