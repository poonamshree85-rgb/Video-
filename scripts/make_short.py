"""One-command Roblox Short pipeline.

    python scripts/make_short.py stories/<slug>.py            # voice+music+SFX -> scenes -> checks -> typecheck
    python scripts/make_short.py stories/<slug>.py --stills   # + preview stills (one per camera shot) + contact sheets
    python scripts/make_short.py stories/<slug>.py --render   # + final 1080x1920 MP4 -> out/<slug>.mp4
    --skip-tts      reuse public/soundtrack.wav + kokoro-cues.json (only when BEATS/SFX/MUSIC did not change)
    --frames 120,480  render these stills instead of one per shot
    --force         render even if rule checks report problems

A story file defines TITLE, BEATS, SFX, MUSIC, CAST and scenes(T). See .agents/skills/roblox-shorts-director/SKILL.md.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
os.chdir(ROOT)

from shorts.audio import build_soundtrack, resolve_time  # noqa: E402
from shorts.scene import FPS, write_story  # noqa: E402

REMOTION = ["node", os.path.join("node_modules", "@remotion", "cli", "remotion-cli.js")]
BUNDLE = os.path.join("out", "bundle")


class Timing:
    """Frame lookups for scenes(T): T.B['b3'] start frame, T.E['b3'] end frame, T.END, T.f('b3+0.5')."""

    def __init__(self, cues):
        self.cues = cues
        self.timings = cues["beatTimings"]
        self.B = {k: v["startFrame"] for k, v in self.timings.items()}
        self.E = {k: v["endFrame"] for k, v in self.timings.items()}
        self.END = cues["durationInFrames"]

    def f(self, ref) -> int:
        return int(round(resolve_time(ref, self.timings) * FPS))


def run(cmd, **kw):
    print("$", " ".join(cmd))
    return subprocess.run(cmd, check=True, **kw)


def load_story(path):
    spec = importlib.util.spec_from_file_location("story", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name in ("TITLE", "BEATS", "CAST", "scenes"):
        if not hasattr(mod, name):
            sys.exit(f"{path}: missing {name}")
    return mod


def still_frames(scenes):
    frames = []
    for sc in scenes:
        for s in sc["cameraShots"]:
            frames.append((s["startFrame"] + s["endFrame"]) // 2)
    return sorted(set(frames))


def contact_sheets(paths, out_dir, per_row=6):
    from PIL import Image

    sheets = []
    for n in range(0, len(paths), per_row * 2):
        chunk = paths[n: n + per_row * 2]
        rows = (len(chunk) + per_row - 1) // per_row
        sheet = Image.new("RGB", (270 * per_row, 480 * rows), "black")
        for i, p in enumerate(chunk):
            sheet.paste(Image.open(p).resize((270, 480)), ((i % per_row) * 270, (i // per_row) * 480))
        out = os.path.join(out_dir, f"sheet-{n // (per_row * 2) + 1}.png")
        sheet.save(out)
        sheets.append(out)
    return sheets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--skip-tts", action="store_true")
    ap.add_argument("--stills", action="store_true")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--frames", default="")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    mod = load_story(args.story)
    slug = os.path.splitext(os.path.basename(args.story))[0]

    # 1. Audio: narration + captions + music + SFX
    cues_path = os.path.join("public", "kokoro-cues.json")
    if args.skip_tts and os.path.exists(cues_path):
        cues = json.load(open(cues_path, encoding="utf-8"))
        print(f"Reusing {cues_path} ({cues['durationInFrames']} frames)")
    else:
        cues = build_soundtrack(mod.BEATS, getattr(mod, "SFX", []), getattr(mod, "MUSIC", None))

    # 2. Scenes -> src/story/currentStory.ts + rule checks
    scenes = mod.scenes(Timing(cues))
    problems = write_story(mod.TITLE, scenes, mod.CAST, cues)
    if problems:
        print("\nRULE CHECKS FAILED:")
        for p in problems:
            print("  " + p)
    else:
        print("Rule checks: OK (scenes contiguous, cuts every 1-3.5 s, no overlapping actors)")

    # 3. Typecheck
    run(["node", os.path.join("node_modules", "typescript", "bin", "tsc"), "-p", "."])
    if problems and not args.force and (args.stills or args.render):
        if args.render:
            sys.exit("Fix the rule problems above (or pass --force) before rendering.")

    if not (args.stills or args.render):
        return

    # 4. Bundle once, then stills / render from the bundle
    run(REMOTION + ["bundle", "src/index.ts", f"--out-dir={BUNDLE}"], stdout=subprocess.DEVNULL)

    if args.stills:
        out_dir = os.path.join("out", "preview", slug)
        os.makedirs(out_dir, exist_ok=True)
        for f in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, f))
        frames = [int(x) for x in args.frames.split(",") if x.strip()] or still_frames(scenes)
        paths = []
        for fr in frames:
            p = os.path.join(out_dir, f"f{fr:05d}.png")
            run(REMOTION + ["still", BUNDLE, "RobloxShort", p, f"--frame={fr}", "--gl=angle", "--scale=0.5"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            paths.append(p)
        for s in contact_sheets(paths, out_dir):
            print("Contact sheet:", s)

    if args.render:
        out = os.path.join("out", f"{slug}.mp4")
        run(REMOTION + ["render", BUNDLE, "RobloxShort", out, "--gl=angle"])
        print("Rendered:", out)


if __name__ == "__main__":
    main()
