"""HAIR COLOR DECIDES YOUR LIFE - test Short for the character constructor and the town.

Build:   python scripts/make_short.py stories/hair_color.py --stills
Render:  python scripts/make_short.py stories/hair_color.py --skip-tts --render
"""
from shorts.scene import HALF, OFF, hold, kf, shot  # noqa: F401

TITLE = "HAIR COLOR DECIDES YOUR LIFE"

# 1. SCRIPT ------------------------------------------------------------------
# Narrator = af_heart (reference-matched). `shout: True` lines are single words, boosted, own caption.
BEATS = [
    {"id": "b1", "text": "In this town, your hair color decides your whole life.", "pause": 0.08},
    {"id": "b2", "text": "Black hair? You're a cop. Blonde? A teacher. Brown? You build houses.", "pause": 0.08},
    {"id": "b3", "text": "On day one, the school sorts every kid by hair.", "pause": 0.07},
    {"id": "b4", "text": "But nobody here had ever been born a ginger. Until me.", "pause": 0.10},
    {"id": "b5", "text": "No class would take me, so I sat alone in the hallway.", "pause": 0.07},
    {"id": "b6", "text": "The bully called me the glitch, and everyone laughed.", "pause": 0.08},
    {"id": "b7", "text": "Every morning, my mom dyed my hair brown.", "pause": 0.06},
    {"id": "b8", "text": "And every day, it washed out by lunch.", "pause": 0.09},
    {"id": "b9", "text": "Then the principal opened the oldest rule book in town.", "pause": 0.07},
    {"id": "b10", "text": "On the last page, in red ink, it said...", "pause": 0.14},
    {"id": "w1", "text": "GINGER!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "IS!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "MAYOR!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "Now the bully sweeps the street in front of my house.", "pause": 0.07},
    {"id": "b12", "text": "And mom finally threw away the brown dye.", "pause": 0.12},
    {"id": "b13", "text": "But last night, my baby brother was born... with blue hair.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,          # music loudness while the narrator talks
    "gaps": 0.05,                  # loudness in pauses
    "dropouts": [("b10+0.3", "w3.end")],   # silence before the reveal, music returns after MAYOR!
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.5", "sparkle"),
    ("b2+0.15", "pop", {"f": 600}),
    ("b2+1.25", "pop", {"f": 720}),
    ("b2+2.35", "pop", {"f": 860}),
    ("b3", "ding_dong"),
    ("b4+1.7", "bell_low"),
    ("b5+0.3", "sad"),
    ("b6+1.3", "laugh"),
    ("b7+0.9", "swish"),
    ("b8+0.95", "bubbles"),
    ("b9+1.2", "thud"),
    ("b10", "riser", {"dur": 2.1}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.6", "swish"),
    ("b11+1.1", "swish"),
    ("b11+1.6", "swish"),
    ("b12+1.3", "pop_down"),
    ("b13+2.0", "twist"),
]

# 3. CAST (character constructor, src/characters/look.ts) ----------------------
HERO = {
    "skin": "light",
    "hair": {"style": "messyFringe", "color": "ginger"},
    "top": {"style": "hoodie", "color": "green", "secondary": "white"},
    "bottom": {"style": "jeans", "color": "denim"},
    "shoes": {"color": "white", "sole": "white"},
    "freckles": True,
}
CAST = {
    "hero": HERO,
    "hero_dyed": {**HERO, "hair": {"style": "messyFringe", "color": "brown"}},
    "hero_mayor": {**HERO, "accessories": ["crown"]},
    "cop": {"extends": "dad", "hair": {"style": "buzz", "color": "black"},
            "top": {"style": "uniform", "color": "navy", "secondary": "yellow"},
            "bottom": {"style": "pants", "color": "navy"}, "shoes": {"style": "boots", "color": "black"},
            "accessories": [{"type": "cap", "color": "navy"}], "facialHair": "mustache"},
    "teacher": {"extends": "teacher_woman", "skin": "fair", "hair": {"style": "bun", "color": "blonde"}},
    "builder": {"extends": "dad", "hair": {"style": "messyFringe", "color": "brown"},
                "top": {"style": "plaid", "color": "orange", "secondary": "mustard"},
                "bottom": {"style": "jeans", "color": "denim"}, "shoes": {"style": "boots", "color": "brown"},
                "accessories": [{"type": "cap", "color": "yellow"}], "facialHair": "beard"},
    "kid_black": {"extends": "schoolboy", "hair": {"style": "spikyAnime", "color": "black"}},
    "kid_blonde": {"extends": "schoolgirl", "hair": {"style": "ponytail", "color": "blonde"}},
    "kid_brown": {"extends": "schoolboy", "skin": "tan", "hair": {"style": "curly", "color": "brown"}},
    "bully": "bully",
    "principal": "principal",
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
    "baby": {"extends": "little_brother", "hair": {"style": "curly", "color": "blue"}, "scale": 0.55},
}


# 4. SCENES (frames come from the narration timings: T.B[id] = start, T.E[id] = end, T.END) --
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S_B = B["b2"] - 1     # street: three jobs
    S_C = B["b3"] - 1     # school sorting + "until me"
    S_D = B["b5"] - 1     # hallway alone + bully
    S_E = B["b7"] - 1     # bedroom: mom dyes hair
    S_F = B["b8"] - 1     # classroom: washes out, rule book, GINGER IS MAYOR
    S_G = B["b11"] - 1    # yellow house: bully sweeps, mom throws dye away
    S_H = B["b13"] - 1    # living room night: blue-haired baby

    SWAP = B["b8"] + 30       # dye washes out
    MAYOR = B["w3"]           # crown appears

    scenes = []

    # A. TOWN OVERVIEW - hook --------------------------------------------------
    scenes.append({
        "id": "scene-hook",
        "location": "town_overview",
        "startFrame": 0,
        "endFrame": S_B,
        "cameraShots": [shot(0, S_B, [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55)],
        "characters": {},
    })

    # B. STREET - cop / teacher / builder ---------------------------------------
    c1, c2 = B["b2"] + 38, B["b2"] + 70
    scenes.append({
        "id": "scene-jobs",
        "location": "street",
        "startFrame": S_B,
        "endFrame": S_C,
        "cameraShots": [
            shot(S_B, c1, [-9.4, 5.8, 14.0], [-9.0, 5.6, 12.5], [-9, 4.3, 0], [-9, 4.3, 0], 48),
            shot(c1, c2, [-3.1, 5.6, 12.0], [-3.5, 5.4, 10.8], [-3.5, 4.3, 0], [-3.5, 4.3, 0], 48),
            shot(c2, S_C, [1.6, 5.8, 13.0], [1.2, 5.6, 11.4], [1, 4.3, 0], [1, 4.3, 0], 50),
        ],
        "characters": {
            "cop": [kf(S_B, [-9, 0, 0.5], 0.15, "point", "cool"), kf(c1 - 4, [-9, 0, 0.5], 0.15, "point", "cool"),
                    kf(c1, [-9, 0, 0.5], 0.3, "idle", "smile"), kf(S_C, [-9, 0, 0.5], 0.3, "idle", "smile")],
            "teacher": [kf(S_B, [-3.5, 0, 0.5], 0, "idle", "smile", "pointer"), kf(c1, [-3.5, 0, 0.5], 0, "wave", "laugh", "pointer"),
                        kf(c2, [-3.5, 0, 0.5], 0, "idle", "smile", "pointer"), kf(S_C, [-3.5, 0, 0.5], 0, "idle", "smile", "pointer")],
            "builder": [kf(S_B, [1, 0, 0.5], -0.2, "idle", "smile", "hammer"), kf(c2, [1, 0, 0.5], -0.2, "celebrate", "laugh", "hammer"),
                        kf(S_C, [1, 0, 0.5], -0.2, "celebrate", "laugh", "hammer")],
        },
    })

    # C. SCHOOL EXTERIOR - sorting, then the ginger arrives ----------------------
    UNTIL = B["b4"] + 52
    scenes.append({
        "id": "scene-sorting",
        "location": "school_exterior",
        "schoolName": "HAIRVILLE SCHOOL",
        "startFrame": S_C,
        "endFrame": S_D,
        "cameraShots": [
            shot(S_C, B["b4"], [0, 7.6, 23], [0, 7.2, 20.5], [0, 4.8, 0], [0, 4.8, 0], 60),
            shot(B["b4"], UNTIL, [2.5, 6.4, 19], [3.5, 5.8, 16], [3, 4.4, 3], [4, 4.3, 4], 54),
            shot(UNTIL, S_D, [4.5, 5.0, 12.8], [4.5, 4.8, 11.6], [4.5, 4.4, 4.8], [4.5, 4.4, 4.8], 46, 0.04),
        ],
        "characters": {
            "kid_black": [kf(S_C, [-4.5, 0, 0], 0, "idle", "smile"), kf(UNTIL - 6, [-4.5, 0, 0], 0, "idle", "smile"),
                          kf(UNTIL, [-4.5, 0, 0], 1.1, "idle", "shocked"), kf(S_D, [-4.5, 0, 0], 1.1, "idle", "shocked")],
            "kid_blonde": [kf(S_C, [0, 0, 0], 0, "wave", "smile"), kf(B["b4"], [0, 0, 0], 0, "idle", "smile"),
                           kf(UNTIL - 6, [0, 0, 0], 0, "idle", "smile"), kf(UNTIL, [0, 0, 0], 0.8, "idle", "shocked"),
                           kf(S_D, [0, 0, 0], 0.8, "idle", "shocked")],
            "kid_brown": [kf(S_C, [4.5, 0, 0], 0, "idle", "cool"), kf(UNTIL - 6, [4.5, 0, 0], 0, "idle", "cool"),
                          kf(UNTIL, [4.5, 0, 0], 0.2, "idle", "shocked"), kf(S_D, [4.5, 0, 0], 0.2, "idle", "shocked")],
            "principal": [kf(S_C, [-2.25, 0, -4.5], 0.0, "point", "deadpan", "clipboard"), kf(B["b4"], [-2.25, 0, -4.5], 0.0, "idle", "deadpan", "clipboard"),
                          kf(UNTIL, [-2.25, 0, -4.5], 0.9, "idle", "shocked", "clipboard"), kf(S_D, [-2.25, 0, -4.5], 0.9, "idle", "shocked", "clipboard")],
            "hero": [kf(S_C, [11, 0, 11], -0.8, "idle", "smile"), kf(B["b4"], [11, 0, 11], -0.8, "walk", "smile"),
                     kf(B["b4"] + 48, [4.5, 0, 4.8], -0.6, "walk", "smile"), kf(B["b4"] + 54, [4.5, 0, 4.8], 0, "idle", "smile"),
                     kf(UNTIL, [4.5, 0, 4.8], 0, "wave", "deadpan"), kf(S_D, [4.5, 0, 4.8], 0, "wave", "deadpan")],
        },
    })

    # D. HALLWAY - alone, then the bully ------------------------------------------
    LAUGH = B["b6"] + 40
    scenes.append({
        "id": "scene-hallway",
        "location": "hallway",
        "startFrame": S_D,
        "endFrame": S_E,
        "cameraShots": [
            shot(S_D, B["b6"], [0.5, 8.4, 20], [1.2, 6.2, 13.5], [0.5, 4.6, -2], [1.5, 4.4, 0], 55),
            shot(B["b6"], S_E, [0, 7.2, 20], [0, 6.8, 18.5], [0, 4.4, -0.5], [0, 4.4, -0.5], 58),
        ],
        "characters": {
            "hero": [kf(S_D, [1.5, 0, 1.5], 0, "idle", "deadpan"), kf(B["b6"] + 14, [1.5, 0, 1.5], 0, "idle", "deadpan"),
                     kf(B["b6"] + 20, [1.5, 0, 1.5], -0.6, "idle", "shocked"), kf(S_E, [1.5, 0, 1.5], -0.6, "idle", "panic")],
            "kid_black": [kf(S_D, [5.8, 0, -2.6], 2.6, "idle", "cool"), kf(LAUGH - 6, [5.8, 0, -2.6], 2.6, "idle", "cool"),
                          kf(LAUGH, [5.8, 0, -2.6], -0.9, "celebrate", "laugh"), kf(S_E, [5.8, 0, -2.6], -0.9, "celebrate", "laugh")],
            "kid_blonde": [kf(S_D, [-1.0, 0, -3.5], 3.1, "idle", "smile"), kf(LAUGH - 6, [-1.0, 0, -3.5], 3.1, "idle", "smile"),
                           kf(LAUGH, [-1.0, 0, -3.5], 0.2, "dance", "laugh"), kf(S_E, [-1.0, 0, -3.5], 0.2, "dance", "laugh")],
            "bully": [kf(S_D, [-12, 0, 1.5], HALF, "idle", "angry"), kf(B["b6"], [-12, 0, 1.5], HALF, "walk", "angry"),
                      kf(B["b6"] + 22, [-3.5, 0, 1.5], HALF, "walk", "angry"), kf(B["b6"] + 26, [-3.5, 0, 1.5], 1.2, "point", "laugh"),
                      kf(S_E, [-3.5, 0, 1.5], 1.2, "point", "laugh")],
        },
    })

    # E. BEDROOM (yellow family) - mom dyes the hair brown -----------------------
    scenes.append({
        "id": "scene-dye",
        "location": "bedroom",
        "variant": "yellow",
        "startFrame": S_E,
        "endFrame": S_F,
        "cameraShots": [shot(S_E, S_F, [3.0, 6.6, 16.5], [3.4, 5.8, 13.5], [3.4, 4.4, -0.5], [3.5, 4.3, -0.5], 56)],
        "characters": {
            "hero_dyed": hold(S_E, S_F, [1.6, 0, 0.5], 0.15, "idle", "deadpan"),
            "mom": [kf(S_E, [5.6, 0, -1.6], -0.9, "wave", "smile"), kf(S_F, [5.6, 0, -1.6], -0.9, "wave", "smile")],
        },
    })

    # F. CLASSROOM - washes out, the rule book, GINGER IS MAYOR ----------------------
    board = ["HAIR RULES", "BLACK = COP", "BLONDE = TEACHER", "BROWN = BUILDER"]
    scenes.append({
        "id": "scene-rulebook",
        "location": "classroom",
        "boardText": board,
        "startFrame": S_F,
        "endFrame": S_G,
        "cameraShots": [
            shot(S_F, B["b9"], [1.0, 5.6, 11.5], [1.0, 5.2, 10], [1.0, 4.4, 2.5], [1.0, 4.4, 2.5], 48),
            shot(B["b9"], B["b10"], [0, 8.2, 19], [-0.8, 7.6, 16.5], [-0.8, 5.2, -2.5], [-1.0, 5.0, -2.5], 56),
            shot(B["b10"], B["w1"], [-2.8, 5.0, 7.6], [-2.8, 4.8, 6.0], [-2.0, 4.4, -1.5], [-2.0, 4.4, -1.5], 46),
            shot(B["w1"], S_G, [1.0, 5.0, 9.5], [0.8, 5.6, 12.0], [1.0, 4.4, 2.5], [0.6, 4.6, 1.5], 48, 0.08),
        ],
        "characters": {
            "hero_dyed": [kf(S_F, [1.0, 0, 2.5], 0, "idle", "smile"), kf(SWAP, [1.0, 0, 2.5], 0, "idle", "smile"),
                          kf(SWAP + 1, OFF, 0, "idle", "smile"), kf(S_G, OFF, 0, "idle", "smile")],
            "hero": [kf(S_F, OFF, 0, "idle", "shocked"), kf(SWAP, OFF, 0, "idle", "shocked"),
                     kf(SWAP + 1, [1.0, 0, 2.5], 0, "idle", "shocked"), kf(B["b9"], [1.0, 0, 2.5], -0.5, "idle", "deadpan"),
                     kf(B["w1"], [1.0, 0, 2.5], -0.4, "idle", "shocked"), kf(MAYOR, [1.0, 0, 2.5], 0, "idle", "shocked"),
                     kf(MAYOR + 1, OFF, 0, "idle", "shocked"), kf(S_G, OFF, 0, "idle", "shocked")],
            "hero_mayor": [kf(S_F, OFF, 0, "celebrate", "laugh"), kf(MAYOR, OFF, 0, "celebrate", "laugh"),
                           kf(MAYOR + 1, [1.0, 0, 2.5], 0, "celebrate", "laugh"), kf(S_G, [1.0, 0, 2.5], 0, "celebrate", "laugh")],
            "kid_blonde": [kf(S_F, [-5.5, 0, 3], 0.6, "idle", "smile"), kf(SWAP, [-5.5, 0, 3], 0.6, "idle", "smile"),
                           kf(SWAP + 4, [-5.5, 0, 3], 0.9, "point", "laugh"), kf(B["b9"], [-5.5, 0, 3], 0.4, "idle", "deadpan"),
                           kf(MAYOR, [-5.5, 0, 3], 0.6, "idle", "shocked"), kf(S_G, [-5.5, 0, 3], 0.6, "idle", "shocked")],
            "bully": [kf(S_F, [5.5, 0, 3], -0.6, "idle", "cool"), kf(SWAP, [5.5, 0, 3], -0.6, "idle", "cool"),
                      kf(SWAP + 4, [5.5, 0, 3], -0.9, "point", "laugh"), kf(B["b9"], [5.5, 0, 3], -0.4, "idle", "cool"),
                      kf(MAYOR, [5.5, 0, 3], -0.6, "idle", "panic"), kf(S_G, [5.5, 0, 3], -0.6, "idle", "panic")],
            "teacher": [kf(S_F, [-5.5, 0, -6.8], 0.5, "idle", "smile", "pointer"), kf(MAYOR, [-5.5, 0, -6.8], 0.5, "idle", "smile", "pointer"),
                        kf(MAYOR + 2, [-5.5, 0, -6.8], 0.7, "idle", "shocked", "pointer"), kf(S_G, [-5.5, 0, -6.8], 0.7, "idle", "shocked", "pointer")],
            "principal": [kf(S_F, [-14, 0, -1.5], HALF, "idle", "deadpan", "clipboard"), kf(B["b9"], [-14, 0, -1.5], HALF, "walk", "deadpan", "clipboard"),
                          kf(B["b9"] + 34, [-2.0, 0, -1.5], HALF, "walk", "deadpan", "clipboard"), kf(B["b9"] + 40, [-2.0, 0, -1.5], 0, "idle", "deadpan", "clipboard"),
                          kf(B["w1"], [-2.0, 0, -1.5], 0.3, "point", "shocked", "clipboard"), kf(S_G, [-2.0, 0, -1.5], 0.3, "point", "shocked", "clipboard")],
        },
    })

    # G. YELLOW HOUSE - bully sweeps the street, mom throws the dye away ----------------
    g = [S_G, S_G + 22, S_G + 26, S_G + 48, S_G + 52, S_H, S_H, S_H]
    scenes.append({
        "id": "scene-mayor-house",
        "location": "house",
        "variant": "yellow",
        "startFrame": S_G,
        "endFrame": S_H,
        "cameraShots": [
            shot(S_G, B["b12"], [0, 6.8, 16], [0, 6.2, 13.5], [0, 4.6, -1.5], [0, 4.5, -1.5], 55),
            shot(B["b12"], S_H, [2.2, 6.0, 13.5], [2.2, 5.6, 11.5], [2.2, 4.6, -2.6], [2.2, 4.6, -2.6], 52),
        ],
        "characters": {
            "hero_mayor": hold(S_G, S_H, [0, 0, -2.6], 0, "idle", "cool"),
            "bully": [kf(g[0], [-6.5, 0, 2.6], HALF, "walk", "deadpan"), kf(g[1], [-3.0, 0, 2.6], HALF, "walk", "deadpan"),
                      kf(g[2], [-3.0, 0, 2.6], -HALF, "walk", "deadpan"), kf(g[3], [-6.5, 0, 2.6], -HALF, "walk", "deadpan"),
                      kf(g[4], [-6.5, 0, 2.6], 0.4, "idle", "deadpan"), kf(g[5], [-6.5, 0, 2.6], 0.4, "idle", "deadpan")],
            "mom": [kf(S_G, [4.5, 0, -3.6], -0.4, "idle", "smile"), kf(B["b12"], [4.5, 0, -3.6], -0.4, "walk", "smile"),
                    kf(B["b12"] + 20, [4.5, 0, -2.6], -0.3, "idle", "laugh"), kf(B["b12"] + 26, [4.5, 0, -2.6], -0.3, "celebrate", "laugh"),
                    kf(S_H, [4.5, 0, -2.6], -0.3, "celebrate", "laugh")],
        },
    })

    # H. LIVING ROOM, NIGHT - the blue-haired baby brother (twist) -----------------------
    BLUE = B["b13"] + 58
    scenes.append({
        "id": "scene-twist",
        "location": "living_room",
        "variant": "yellow",
        "isNight": True,
        "startFrame": S_H,
        "endFrame": END,
        "cameraShots": [
            shot(S_H, BLUE, [0, 7.0, 18.5], [0, 5.8, 15], [0, 3.8, 0], [0, 3.4, 0.5], 56),
            shot(BLUE, END, [0, 3.2, 7.4], [0, 3.0, 6.2], [0, 2.4, 1.2], [0, 2.4, 1.2], 44, 0.05),
        ],
        "characters": {
            "baby": [kf(S_H, [0, 0, 1.2], 0, "idle", "smile"), kf(BLUE, [0, 0, 1.2], 0, "wave", "laugh"), kf(END, [0, 0, 1.2], 0, "wave", "laugh")],
            "hero_mayor": [kf(S_H, [-4.0, 0, 0.4], 0.9, "idle", "smile"), kf(BLUE - 4, [-4.0, 0, 0.4], 0.9, "idle", "smile"),
                           kf(BLUE, [-4.0, 0, 0.4], 0.9, "idle", "shocked"), kf(END, [-4.0, 0, 0.4], 0.9, "idle", "shocked")],
            "mom": [kf(S_H, [4.0, 0, 0.4], -0.9, "idle", "smile"), kf(BLUE - 4, [4.0, 0, 0.4], -0.9, "idle", "smile"),
                    kf(BLUE, [4.0, 0, 0.4], -0.9, "idle", "panic"), kf(END, [4.0, 0, 0.4], -0.9, "idle", "panic")],
        },
    })

    return scenes
