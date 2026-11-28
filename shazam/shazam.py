# Let's Build It: name that song from 3 noisy seconds. Needs only numpy.
import numpy as np

RATE = 8000                                   # sound samples per second
NAMES = ["Midnight Tacos", "Turbo Snail", "Disco Potato", "Moon Pickles",
         "Sleepy Robot", "Banana Thunder", "Cactus Disco", "Penguin Taxi",
         "Quantum Soup", "Left Sock Blues", "Pixel Lemonade", "Lazy Volcano",
         "Funky Toaster", "Electric Hummus", "Sneaky Giraffe", "Wifi in the Rain",
         "Bubble Wrap Opera", "Grandma's Laser", "Tuesday Spaghetti", "Robot Lullaby"]

# 1. THE LIBRARY: 20 made-up songs, 30 seconds each (bass + melody + sparkle)
def make_song(number):
    dice = np.random.default_rng(number)
    scale = np.array([0, 2, 4, 7, 9, 12, 14, 16, 19, 21])
    song = np.zeros(30 * RATE)
    for low_note, beats in [(110, 60), (440, 120), (1760, 240)]:
        size = len(song) // beats
        t = np.arange(size) / RATE
        for beat in range(beats):
            pitch = low_note * 2 ** (dice.choice(scale) / 12)
            song[beat * size:(beat + 1) * size] += np.sin(2 * np.pi * pitch * t) * np.exp(-4 * t)
    return song

# 2. SOUND -> PICTURE: slice the sound, ask each slice "which pitches are loud?"
def picture(sound):
    slices = [sound[i:i + 1024] * np.hanning(1024) for i in range(0, len(sound) - 1024, 256)]
    return np.abs(np.fft.rfft(slices))[:, :480]          # rows = time, columns = pitch

# 3. KEEP ONLY THE BRIGHTEST DOTS: the loudest pitch in each of 4 bands
def bright_dots(pic):
    dots = []
    for time, row in enumerate(pic):
        for band in range(4):
            dots.append((time, band * 120 + int(np.argmax(row[band * 120:(band + 1) * 120]))))
    return dots

# 4. FINGERPRINTS: two dots and the gap between them
def fingerprints(sound):
    dots = bright_dots(picture(sound))
    for i, (time1, pitch1) in enumerate(dots):
        for time2, pitch2 in dots[i + 1:i + 13]:
            yield (pitch1, pitch2, time2 - time1), time1

# 5. REMEMBER EVERY SONG: fingerprint -> where it happens
library = {}
for number, name in enumerate(NAMES):
    for mark, time in fingerprints(make_song(number)):
        library.setdefault(mark, []).append((name, time))

# 6. NAME THAT TUNE: every matching fingerprint votes for (song, start time)
def name_that_tune(clip):
    votes = {}
    for mark, time in fingerprints(clip):
        for name, song_time in library.get(mark, []):
            votes[name, song_time - time] = votes.get((name, song_time - time), 0) + 1
    (name, start), score = max(votes.items(), key=lambda vote: vote[1])
    return name, start * 256 / RATE, score

# 7. THE TEST: 3 seconds from the middle of a song, buried in noise
NOISE = 1.0
if __name__ == "__main__":
    dice = np.random.default_rng(0)
    print(sum(len(places) for places in library.values()), "fingerprints remembered from", len(NAMES), "songs")
    secret = 12                                           # Funky Toaster
    clip = make_song(secret)[17 * RATE:20 * RATE]
    clip = clip + NOISE * dice.normal(size=len(clip))
    name, start, score = name_that_tune(clip)
    print(f"I heard: {name}, starting at second {start:.1f}  ({score} fingerprints agree)")
