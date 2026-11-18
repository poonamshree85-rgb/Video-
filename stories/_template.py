"""TEMPLATE - copy to stories/<slug>.py, then:
    python scripts/make_short.py stories/<slug>.py --stills
    python scripts/make_short.py stories/<slug>.py --skip-tts --render
All parts (presets, hair, clothes, locations, anims, props, SFX) are listed in
.agents/skills/roblox-shorts-director/SKILL.md. This template is a runnable mini-story.
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, medium, shot, wide  # noqa: F401

TITLE = "TEMPLATE STORY"

# 1. SCRIPT: first words "In this town," / "In this world,". 14-16 beats, 35-45 s in a real Short.
BEATS = [
    {"id": "b1", "text": "In this town, everyone gets a crown on their tenth birthday.", "pause": 0.08},
    {"id": "b2", "text": "Kids count the days, and parents throw giant parties.", "pause": 0.08},
    {"id": "b3", "text": "But on my birthday, the crown went to my little sister.", "pause": 0.12},
    {"id": "w1", "text": "WHY!", "voice": "am_michael", "shout": True, "pause": 0.2},
    {"id": "b4", "text": "Turns out, she was born first. Mom never told me.", "pause": 0.3},
]

# 2. MUSIC + SFX: (time, preset, {opts}); time = "b2", "b2.end", "b2+0.4"
MUSIC = {"file": "music/fallen-down.mp3", "under_voice": 0.022, "gaps": 0.05, "dropouts": [("b3.end-0.3", "w1.end")]}
SFX = [
    ("b1", "whoosh"),
    ("b1+1.6", "sparkle"),
    ("b2+0.8", "pop"),
    ("b3+0.4", "riser", {"dur": 1.6}),
    ("w1", "impact"),
    ("b4+1.0", "twist"),
]

# 3. CAST: preset name or {"extends": preset, hair/top/bottom/shoes/accessories/..., "scale"}
HERO = {"extends": "kid_boy", "hair": {"style": "messyFringe", "color": "black"},
        "top": {"style": "hoodie", "color": "royal", "secondary": "white"}}
CAST = {
    "hero": HERO,
    "sister": {"extends": "kid_girl", "hair": {"style": "pigtails", "color": "black"},
               "accessories": ["crown"], "scale": 0.8},
    "mom": {"extends": "real_mom", "hair": {"color": "black"}},
}


# 4. SCENES: contiguous from 0 to T.END; cameraShots 1-3.5 s each (cover() does 2-3 s cuts for you)
def scenes(T):
    S2, S3, END = T.B["b2"] - 1, T.B["b3"] - 1, T.END
    HERO_P, SIS_P, MOM_P = [-2.5, 0, 1.5], [2.5, 0, 1.5], [6.0, 0, -1.0]
    return [
        {   # hook: aerial town
            "id": "hook", "location": "town_overview", "startFrame": 0, "endFrame": S2,
            "cameraShots": [shot(0, S2, [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55)],
            "characters": {},
        },
        {   # world-building
            "id": "party", "location": "playground", "startFrame": S2, "endFrame": S3,
            "cameraShots": cover(S2, S3, [lambda a, b: wide(a, b), lambda a, b: medium(a, b, HERO_P)]),
            "characters": {
                "hero": hold(S2, S3, HERO_P, 0.3, "celebrate", "laugh"),
                "mom": hold(S2, S3, MOM_P, -0.6, "wave", "smile"),
            },
        },
        {   # stakes + shout + twist
            "id": "crown", "location": "living_room", "variant": "blue", "startFrame": S3, "endFrame": END,
            "cameraShots": cover(S3, END, [
                lambda a, b: medium(a, b, [0, 0, 1.5]),
                lambda a, b: close_up(a, b, SIS_P, scale=0.8),
                lambda a, b: close_up(a, b, HERO_P, shake=0.06),
            ]),
            "characters": {
                "hero": [kf(S3, HERO_P, 0.5, "idle", "smile"), kf(T.B["w1"], HERO_P, 0.5, "point", "angry"),
                         kf(END, HERO_P, 0.5, "idle", "shocked")],
                "sister": hold(S3, END, SIS_P, -0.4, "dance", "laugh"),
            },
        },
    ]
