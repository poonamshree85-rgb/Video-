# Roblox Shorts Engine — Agent Instructions

Whenever the user asks to create, write, or render a Roblox Short video (or gives a story topic/rule):

1. Read and follow the [`roblox-shorts-director`](./.agents/skills/roblox-shorts-director/SKILL.md) skill.
2. Write one story file `stories/<slug>.py` (copy `stories/_template.py`; full example: `stories/hair_color.py`) from the catalogs in the skill: beats, music, SFX, cast, scenes.
3. Run the pipeline end-to-end without asking unnecessary permission questions:
   - `python scripts/make_short.py stories/<slug>.py --stills`
     - Fix every `RULE CHECKS FAILED` line.
     - Inspect `out/preview/<slug>/sheet-*.png`.
   - `python scripts/make_short.py stories/<slug>.py --skip-tts --render` → `out/<slug>.mp4`

Hard rules, enforced by the skill and the build checks:
- The script opens with "In this town," / "In this world,".
- A camera cut every 2–3 s; no shot longer than 3.5 s.
- Narrator voice `af_heart`.
- Music from `public/music/`.
- Soft SFX presets only.
- Actors at least 4.5 studs apart.

Never edit `src/story/currentStory.ts` by hand; it is generated.
