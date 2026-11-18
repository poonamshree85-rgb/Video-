"""Audio engine: Kokoro narration + captions, background music bed, soft SFX palette.

Output: public/soundtrack.wav (mono, 24 kHz) and public/kokoro-cues.json
(durationInFrames, beatTimings, captions) that the scene builder reads.
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import wave

import numpy as np

FPS = 30
SR = 24000
MODEL_PATH = os.path.join("models", "kokoro-v1.0.onnx")
VOICES_PATH = os.path.join("models", "voices-v1.0.bin")

# Narrator voice measured against references/*.mp4 (median pitch ~200 Hz, ~5.8 syllables/s):
# af_heart is the closest Kokoro voice in pitch, timbre and pace.
NARRATOR_VOICE = "af_heart"
NARRATOR_SPEED = 1.18
SHOUT_SPEED = 0.95


# ---------------------------------------------------------------------------
# Narration
# ---------------------------------------------------------------------------
def trim_silence(audio: np.ndarray, threshold: float = 0.012, pad_samples: int = 720) -> np.ndarray:
    mask = np.abs(audio) > threshold
    if not np.any(mask):
        return audio
    idx = np.where(mask)[0]
    return audio[max(0, idx[0] - pad_samples): min(len(audio), idx[-1] + pad_samples)]


def split_into_short_cues(text: str, max_words: int = 2) -> list[str]:
    words = text.strip().split()
    chunks, i = [], 0
    while i < len(words):
        take = max_words
        if i + take < len(words) and len(words[i + take - 1]) <= 2:
            take = min(3, len(words) - i)
        chunks.append(" ".join(words[i: i + take]))
        i += take
    return chunks


def synthesize_narration(beats: list[dict]):
    """beats: [{id, text, voice?, speed?, pause?, shout?}] -> (voice_track, beat_timings, captions)."""
    from kokoro_onnx import Kokoro

    kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
    parts = [np.zeros(int(0.15 * SR), dtype=np.float32)]
    cur = len(parts[0])
    timings, captions = {}, []
    for beat in beats:
        shout = beat.get("shout", False)
        voice = beat.get("voice", NARRATOR_VOICE)
        speed = beat.get("speed", SHOUT_SPEED if shout else NARRATOR_SPEED)
        samples, _ = kokoro.create(beat["text"], voice=voice, speed=speed, lang="en-us")
        clip = trim_silence(samples.astype(np.float32))
        if shout:
            clip = np.clip(clip * 1.28, -0.98, 0.98)
        start = cur / SR
        end = start + len(clip) / SR
        timings[beat["id"]] = {
            "startSec": round(start, 3), "endSec": round(end, 3),
            "startFrame": int(round(start * FPS)), "endFrame": int(round(end * FPS)),
            "text": beat["text"],
        }
        if shout:
            captions.append({"startFrame": int(round(start * FPS)), "endFrame": int(round((end + 0.10) * FPS)), "text": beat["text"]})
        else:
            chunks = split_into_short_cues(beat["text"])
            total = max(1, sum(len(c) for c in chunks))
            acc = 0
            for c in chunks:
                t0 = start + acc / total * (end - start)
                acc += len(c)
                t1 = start + acc / total * (end - start)
                f0 = int(round(t0 * FPS))
                captions.append({"startFrame": f0, "endFrame": max(f0 + 1, int(round(t1 * FPS)) - 1), "text": c})
        pause = np.zeros(int(beat.get("pause", 0.08) * SR), dtype=np.float32)
        parts += [clip, pause]
        cur += len(clip) + len(pause)
    return np.concatenate(parts), timings, captions


# ---------------------------------------------------------------------------
# Soft SFX palette (no harsh square/saw beeps)
# ---------------------------------------------------------------------------
def _span(buf, t, dur):
    s0 = max(0, int(t * SR))
    s1 = min(len(buf), int((t + dur) * SR))
    return s0, s1, np.arange(max(0, s1 - s0), dtype=np.float32) / SR


def piano(buf, t, f, dur=1.2, vol=0.05, tau=0.45):
    s0, s1, x = _span(buf, t, dur)
    if s1 <= s0:
        return
    sig = sum(a * np.sin(2 * np.pi * f * h * x * (1 + 0.0007 * h)) for h, a in [(1, 1.0), (2, 0.38), (3, 0.16), (4, 0.07)])
    buf[s0:s1] += (sig * np.minimum(1.0, x / 0.006) * np.exp(-x / tau) * vol).astype(np.float32)


def pad(buf, t, dur, freqs, vol=0.03, attack=0.6, release=0.8):
    s0, s1, x = _span(buf, t, dur)
    if s1 <= s0:
        return
    env = np.minimum(1.0, x / attack) * np.clip((dur - x) / release, 0, 1)
    sig = sum(np.sin(2 * np.pi * f * (1 + d) * x) for f in freqs for d in (-0.004, 0.004)) / (2 * len(freqs))
    buf[s0:s1] += (sig * env * vol * 4).astype(np.float32)


def bell(buf, t, f, vol=0.06, dur=2.0):
    s0, s1, x = _span(buf, t, dur)
    if s1 <= s0:
        return
    sig = sum(a * np.sin(2 * np.pi * f * r * x) * np.exp(-x / tau) for r, a, tau in [(1.0, 1.0, 0.9), (2.76, 0.45, 0.35), (5.4, 0.2, 0.15), (2.0, 0.3, 0.6)])
    buf[s0:s1] += (sig * np.minimum(1.0, x / 0.003) * vol).astype(np.float32)


def pop(buf, t, f0=500, f1=1100, vol=0.08, dur=0.12):
    s0, s1, x = _span(buf, t, dur)
    if s1 <= s0:
        return
    phase = 2 * np.pi * np.cumsum(f0 * (f1 / f0) ** (x / dur)) / SR
    buf[s0:s1] += (np.sin(phase) * np.minimum(1.0, x / 0.004) * np.exp(-x / (dur * 0.35)) * vol).astype(np.float32)


def whoosh(buf, t, dur=0.8, vol=0.05, bright=0.08, seed=1):
    s0, s1, x = _span(buf, t, dur)
    n = s1 - s0
    if n <= 0:
        return
    noise = np.random.default_rng(seed).uniform(-1, 1, n)
    try:
        from scipy.signal import lfilter
        out = lfilter([bright], [1, -(1 - bright)], noise)
    except ImportError:  # pragma: no cover
        out = np.convolve(noise, np.ones(int(1 / bright)) * bright, "same")
    out = out / (np.max(np.abs(out)) + 1e-6)
    buf[s0:s1] += (out * np.sin(np.pi * np.arange(n) / n) ** 2 * vol).astype(np.float32)


def kick(buf, t, vol=0.12):
    s0, s1, x = _span(buf, t, 0.35)
    if s1 <= s0:
        return
    phase = 2 * np.pi * np.cumsum(45 + 75 * np.exp(-x / 0.03)) / SR
    buf[s0:s1] += (np.sin(phase) * np.exp(-x / 0.12) * vol).astype(np.float32)


NOTE = {"C3": 130.81, "E3": 164.81, "G3": 196.0, "A3": 220.0, "C4": 261.63, "D4": 293.66, "Eb4": 311.13,
        "E4": 329.63, "G4": 392.0, "A4": 440.0, "C5": 523.25, "E5": 659.25, "G5": 783.99}


def _sfx_preset(buf, name: str, t: float, seed: int, **kw):
    """Named sound effects a story can place on any beat (see SFX_PRESETS)."""
    v = kw.get("vol", 1.0)
    if name == "whoosh":          # scene transition / fast move
        whoosh(buf, t, kw.get("dur", 0.8), 0.05 * v, 0.07, seed)
    elif name == "swish":         # broom, brush, hand wave
        whoosh(buf, t, kw.get("dur", 0.35), 0.025 * v, 0.25, seed)
    elif name == "pop":           # list items, comedic beats, something appears
        f = kw.get("f", 650)
        pop(buf, t, f, f * 1.9, 0.07 * v)
    elif name == "pop_down":      # something removed / thrown away
        pop(buf, t, 700, 350, 0.06 * v, 0.15)
    elif name == "bubbles":       # washing, water, magic fizzing
        for k in range(3):
            pop(buf, t + k * 0.11, 300 + k * 90, 900 + k * 150, 0.05 * v, 0.10)
    elif name == "laugh":         # crowd laughing (bouncy pops)
        for k in range(5):
            pop(buf, t + k * 0.14, 420 + k * 40, 700 + k * 60, 0.035 * v, 0.09)
    elif name == "sparkle":       # magic, rich, shiny reveal
        for k, n in enumerate(["C5", "E5", "G5"]):
            bell(buf, t + k * 0.07, NOTE[n] * 2, 0.02 * v, 1.2)
    elif name == "ding_dong":     # school bell / doorbell
        bell(buf, t, NOTE["E5"], 0.045 * v)
        bell(buf, t + 0.4, NOTE["C5"], 0.045 * v)
    elif name == "bell_low":      # ominous line, "until me", rule stated
        bell(buf, t, NOTE["C4"], 0.06 * v, 2.4)
    elif name == "sad":           # lonely / failure: descending piano
        for k, n in enumerate(["E4", "D4", "C4"]):
            piano(buf, t + k * 0.45, NOTE[n], 1.4, 0.04 * v, 0.6)
    elif name == "thud":          # book drop, door, body hits floor
        kick(buf, t, 0.09 * v)
        whoosh(buf, t + 0.03, 0.4, 0.03 * v, 0.2, seed)
    elif name == "impact":        # big hit, shout word
        kick(buf, t, 0.11 * v)
    elif name == "riser":         # tension swell until `dur` seconds later
        pad(buf, t, kw.get("dur", 2.0), [NOTE["A3"], NOTE["E4"]], 0.03 * v, attack=kw.get("dur", 2.0) * 0.6, release=0.2)
    elif name == "reveal":        # payoff: kick + bright bell chord
        kick(buf, t, 0.12 * v)
        whoosh(buf, t - 0.25, 0.6, 0.04 * v, 0.1, seed)
        for k, n in enumerate(["C5", "E5", "G5"]):
            bell(buf, t + k * 0.05, NOTE[n], 0.035 * v, 2.2)
    elif name == "twist":         # dark twist ending: low detuned bells
        bell(buf, t, NOTE["A3"] / 2, 0.07 * v, 3.0)
        bell(buf, t + 0.02, NOTE["Eb4"] / 2, 0.03 * v, 3.0)
    else:
        raise ValueError(f"Unknown SFX preset '{name}'. Available: {', '.join(SFX_PRESETS)}")


SFX_PRESETS = ["whoosh", "swish", "pop", "pop_down", "bubbles", "laugh", "sparkle", "ding_dong", "bell_low",
               "sad", "thud", "impact", "riser", "reveal", "twist"]


# ---------------------------------------------------------------------------
# Time references:  "b3" = start of beat b3, "b3.end" = its end, "b3+0.4" / "b3.end-0.2" offsets
# ---------------------------------------------------------------------------
def resolve_time(ref, timings) -> float:
    if isinstance(ref, (int, float)):
        return float(ref)
    m = re.fullmatch(r"([A-Za-z0-9_]+)(\.end)?([+-][0-9.]+)?", ref.strip())
    if not m or m.group(1) not in timings:
        raise ValueError(f"Bad time reference '{ref}' (beat ids: {', '.join(timings)})")
    base = timings[m.group(1)]["endSec" if m.group(2) else "startSec"]
    return base + float(m.group(3) or 0)


# ---------------------------------------------------------------------------
# Music bed
# ---------------------------------------------------------------------------
def _ffmpeg() -> str:
    hits = glob.glob(os.path.join("node_modules", "@remotion", "compositor-*", "ffmpeg*"))
    if not hits:
        raise RuntimeError("ffmpeg not found (expected Remotion's bundled one in node_modules/@remotion/compositor-*)")
    return hits[0]


def decode_music(path: str) -> np.ndarray:
    tmp = os.path.join("out", "_music_decoded.wav")
    os.makedirs("out", exist_ok=True)
    subprocess.run([_ffmpeg(), "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", str(SR), tmp], check=True)
    with wave.open(tmp) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    os.remove(tmp)
    return a


def _smooth(x: np.ndarray, win: int) -> np.ndarray:
    return np.convolve(x, np.ones(win) / win, "same")


def music_bed(music: dict, voice: np.ndarray, timings: dict) -> np.ndarray:
    """Levelled, voice-ducked music. music = {file, start?, under_voice?, gaps?, dropouts?: [(from, to)], fade_out?}."""
    n = len(voice)
    src = decode_music(os.path.join("public", music["file"]))
    src = src[int(music.get("start", 0.0) * SR):]
    reps = int(np.ceil(n / max(1, len(src))))
    track = np.tile(src, reps)[:n] if reps > 1 else src[:n]
    if len(track) < n:
        track = np.pad(track, (0, n - len(track)))

    hop = SR // 20  # 50 ms control rate
    def ctrl(sig):
        k = len(sig) // hop
        return np.sqrt((sig[: k * hop].reshape(k, hop) ** 2).mean(1) + 1e-9)

    m_rms = _smooth(ctrl(track), 30)                # 1.5 s loudness of the music
    v_act = _smooth((ctrl(voice) > 0.02).astype(np.float32), 6)  # voice activity (0..1)
    target = music.get("gaps", 0.05) + (music.get("under_voice", 0.022) - music.get("gaps", 0.05)) * np.clip(v_act * 1.5, 0, 1)
    gain = np.clip(target / m_rms, 0.0, 3.0)
    t_ctrl = np.arange(len(gain)) * hop / SR
    for a, b in music.get("dropouts", []):
        ta, tb = resolve_time(a, timings), resolve_time(b, timings)
        fade = np.clip(np.minimum((t_ctrl - (ta - 0.3)) / 0.3, ((tb + 0.15) - t_ctrl) / 0.15), 0, 1)
        gain *= 1 - fade
    gain = _smooth(gain, 4)
    g = np.interp(np.arange(n) / SR, t_ctrl, gain).astype(np.float32)
    t = np.arange(n) / SR
    g *= np.clip(t / 0.4, 0, 1) * np.clip((t[-1] - t) / music.get("fade_out", 1.2), 0, 1)
    return track * g


# ---------------------------------------------------------------------------
# Full mix
# ---------------------------------------------------------------------------
def build_soundtrack(beats: list[dict], sfx: list, music: dict | None, tail_sec: float = 0.4) -> dict:
    voice, timings, captions = synthesize_narration(beats)
    voice = np.concatenate([voice, np.zeros(int(tail_sec * SR), dtype=np.float32)])
    total = len(voice)
    fx = np.zeros(total, dtype=np.float32)
    for i, item in enumerate(sfx):
        ref, name = item[0], item[1]
        kw = item[2] if len(item) > 2 else {}
        _sfx_preset(fx, name, resolve_time(ref, timings), seed=i + 7, **kw)
    bed = music_bed(music, voice, timings) if music else 0.0
    mixed = voice * 0.95 + fx + bed
    peak = np.max(np.abs(mixed))
    if peak > 0.95:
        mixed *= 0.95 / peak
    os.makedirs("public", exist_ok=True)
    with wave.open(os.path.join("public", "soundtrack.wav"), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((mixed * 32767).astype(np.int16).tobytes())
    meta = {
        "durationSeconds": round(total / SR, 2),
        "durationInFrames": int(np.ceil(total / SR * FPS)),
        "beatTimings": timings,
        "captions": captions,
    }
    with open(os.path.join("public", "kokoro-cues.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"Soundtrack: {meta['durationSeconds']}s ({meta['durationInFrames']} frames), peak {min(peak, 0.95):.2f}")
    for k, v in timings.items():
        print(f"  {k:6s} {v['startFrame']:5d}..{v['endFrame']:5d}  {v['text']}")
    return meta
