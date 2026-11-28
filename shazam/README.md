# Let's Build It 16 · A tiny Shazam

Name a song from 3 noisy seconds, in about 50 lines of Python. Only needs numpy.

This is a learning build: the core idea, small enough to read in one sitting.
It is not the real app, it uses no Shazam code, and it is not affiliated with Shazam.
The idea comes from the paper Shazam's co-founder published in 2003
(Avery Wang, "An Industrial-Strength Audio Search Algorithm").

## Run it

```bash
pip install numpy
python shazam.py
```

You should see:

```
895080 fingerprints remembered from 20 songs
I heard: Funky Toaster, starting at second 17.0  (1164 fingerprints agree)
```

It takes a second or two.

## The four pieces

| Piece | In the code | What it does |
|---|---|---|
| 1. Picture | `picture()` | Slices the sound and asks each slice which pitches are loud. Sound becomes a picture. |
| 2. Dots | `bright_dots()` | Keeps only the loudest pitch in each of 4 bands. 43,200 numbers become 360 dots. |
| 3. Pairs | `fingerprints()` | Ties each dot to the next few dots: (this pitch, that pitch, gap). |
| 4. Vote | `name_that_tune()` | Looks up every fingerprint and counts only the matches that agree on *when* the clip starts. |

The 20 songs are invented by `make_song()`, so no real music is used.

## Try to break it

```bash
python break_it.py
```

This runs every test from the video on the same 200 random clips:

```
count every match          : 116 of 200
only matches that agree    : 200 of 200
half a second of sound     : 194 of 200
a fifth of a second        : 64 of 200
noise 4x stronger          : 200 of 200
played 5% faster, no noise : 26 of 200
```

The first line is the version without the fix (count every match, ignore timing).
The speed test is the classic weak spot: every pitch moves, so every fingerprint changes.

Things to change yourself: `NOISE` at the bottom of `shazam.py`, the `secret` song
number, and where the clip starts.

## Try it on your own music

```bash
python my_songs.py song1.wav song2.wav song3.wav --clip mystery.wav
```

The songs become the library and the clip is what it tries to name. WAV files
only (16-bit), any length, mono or stereo.

Honest note: I tested this helper with generated tunes saved as WAV files, not
with real recordings. Real music is much messier than our beeps, so expect it
to be weaker. Making it solid on real songs is what a full build would be about.

## Honest notes

- Our songs are simple generated tones and there are only 20. That makes the job
  far easier than real life, which is why it survives so much noise.
- It always answers, even for a song it has never heard. A real system needs a
  "not sure" threshold.
- Tested with Python 3.10 to 3.13 and numpy 1.26 to 2.x.

Video: Runtime Explained on YouTube, playlist "Let's Build It".
