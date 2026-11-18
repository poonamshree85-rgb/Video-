"""EVERYONE GETS A WORD LIMIT - 9:16 Roblox Short.

Build:   python scripts/make_short.py stories/word_limit.py --stills
Render:  python scripts/make_short.py stories/word_limit.py --skip-tts --render
"""
from shorts.scene import HALF, close_up, cover, face, hold, kf, medium, shot, split_shots, wide  # noqa: F401

TITLE = "EVERYONE GETS A WORD LIMIT"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this town, a floating counter shows every word you have left.", "pause": 0.08},
    {"id": "b2", "text": "Hit zero, and a golden halo locks your voice forever.", "pause": 0.08},
    {"id": "b3", "text": "Rich kids brag all day because they're born with almost a million.", "pause": 0.07},
    {"id": "b4", "text": "At night, I even taped my mouth shut so I wouldn't talk in my sleep.", "pause": 0.09},
    {"id": "b5", "text": "I had a million words, until a glitch at school dropped me to three.", "pause": 0.08},
    {"id": "b6", "text": "The school bully saw my counter and laughed in front of everyone.", "pause": 0.08},
    {"id": "b7", "text": "I stayed completely silent in class, guarding my last three words.", "pause": 0.08},
    {"id": "b8", "text": "After school, the bully cornered my little sister at the park.", "pause": 0.08},
    {"id": "b9", "text": "Three words meant silence forever, so I took a deep breath.", "pause": 0.08},
    {"id": "b10", "text": "Everyone froze as I stepped forward and shouted...", "pause": 0.14},
    {"id": "w1", "text": "LEAVE!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "HER!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w3", "text": "ALONE!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b11", "text": "The bully ran in terror, and my golden halo locked in.", "pause": 0.08},
    {"id": "b12", "text": "That night, my mom cried because she thought I'd never speak again.", "pause": 0.14},
    {"id": "b13", "text": "Until midnight, when my golden halo cracked, and turned bright red.", "pause": 0.25},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b10+0.3", "w3.end")],
}

SFX = [
    ("b1", "whoosh"),
    ("b1+0.9", "sparkle"),
    ("b2+0.6", "bell_low"),
    ("b3+0.5", "pop", {"f": 700}),
    ("b4+0.8", "swish"),
    ("b5+1.4", "thud"),
    ("b5+1.6", "bell_low"),
    ("b6+1.2", "laugh"),
    ("b7", "ding_dong"),
    ("b8+1.1", "bell_low"),
    ("b9+0.6", "sad"),
    ("b10", "riser", {"dur": 2.2}),
    ("w1", "impact"),
    ("w2", "impact"),
    ("w3", "reveal"),
    ("b11+0.3", "whoosh"),
    ("b12+0.9", "sad"),
    ("b13+1.8", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
CAST = {
    "hero": {
        "extends": "kid_boy",
        "skin": "light",
        "hair": {"style": "messyFringe", "color": "brown"},
        "top": {"style": "hoodie", "color": "royal", "secondary": "white"},
        "bottom": {"style": "jeans", "color": "denim"},
        "shoes": {"style": "sneakers", "color": "white", "sole": "white"},
    },
    "silent_kid": {
        "extends": "schoolboy",
        "hair": {"style": "sidePart", "color": "black"},
        "top": {"style": "sweater", "color": "gray", "secondary": "white"},
    },
    "rich_kid": {
        "extends": "cool_kid",
        "hair": {"style": "fluffySwept", "color": "goldenBlonde"},
        "top": {"style": "jacket", "color": "purple", "secondary": "yellow"},
        "accessories": ["sunglasses"],
    },
    "normal_kid": {
        "extends": "schoolgirl",
        "hair": {"style": "ponytail", "color": "auburn"},
    },
    "mom": {
        "extends": "real_mom",
        "hair": {"style": "bun", "color": "darkBrown"},
    },
    "bully": "bully",
    "teacher": {
        "extends": "teacher_woman",
        "hair": {"style": "bob", "color": "blonde"},
    },
    "sister": {
        "extends": "kid_girl",
        "hair": {"style": "pigtails", "color": "brown"},
        "top": {"style": "dress", "color": "pink", "secondary": "white"},
        "scale": 0.8,
    },
}


# 4. SCENES --------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S_B = B["b2"] - 1     # street: zero = golden halo
    S_C = B["b3"] - 1     # shop: rich kid vs normal kid
    S_D = B["b4"] - 1     # bedroom night: mouth tape
    S_E = B["b5"] - 1     # school exterior: counter glitches to 3
    S_F = B["b6"] - 1     # hallway: bully laughs
    S_G = B["b7"] - 1     # classroom: silent in class
    S_H = B["b8"] - 1     # playground: bully corners sister -> LEAVE HER ALONE -> bully runs
    S_I = B["b12"] - 1    # living room night: mom cries, golden halo turns red

    GLITCH = B["b5"] + 42
    RED = B["b13"] + 46

    out = []

    # A. TOWN OVERVIEW - hook
    out.append({
        "id": "scene-hook",
        "location": "town_overview",
        "startFrame": 0,
        "endFrame": S_B,
        "cameraShots": cover(0, S_B, [
            lambda a, b: shot(a, b, [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55),
        ], target_sec=2.4),
        "characters": {},
    })

    # B. STREET - silent kid with counter_0 vs normal kid
    SILENT_P = [-2.4, 0, 0.5]
    NORM_P = [2.3, 0, 0.5]
    out.append({
        "id": "scene-street",
        "location": "street",
        "startFrame": S_B,
        "endFrame": S_C,
        "cameraShots": split_shots(S_B, S_C, [
            lambda a, b: medium(a, b, [-0.05, 0, 0.5], dist=16.5, fov=56),
            lambda a, b: close_up(a, b, SILENT_P, dist=7.6),
        ]),
        "characters": {
            "silent_kid": hold(S_B, S_C, SILENT_P, 0.25, "idle", "deadpan", "counter_0"),
            "normal_kid": hold(S_B, S_C, NORM_P, -0.4, "wave", "smile", "counter_mid"),
        },
    })

    # C. SHOP - rich kid bragging with counter_high
    RICH_P = [-2.3, 0, 0.5]
    N_SHOP_P = [2.3, 0, 0.5]
    out.append({
        "id": "scene-shop",
        "location": "shop",
        "startFrame": S_C,
        "endFrame": S_D,
        "cameraShots": split_shots(S_C, S_D, [
            lambda a, b: medium(a, b, [0.0, 0, 0.5], dist=16.8, fov=56),
            lambda a, b: close_up(a, b, RICH_P, dist=7.6),
        ]),
        "characters": {
            "rich_kid": hold(S_C, S_D, RICH_P, 0.25, "celebrate", "laugh", "counter_high"),
            "normal_kid": hold(S_C, S_D, N_SHOP_P, -0.5, "idle", "deadpan", "counter_mid"),
        },
    })

    # D. BEDROOM, NIGHT - mouth tape
    HERO_BED_P = [-1.2, 0, 0.8]
    MOM_BED_P = [3.4, 0, -0.5]
    out.append({
        "id": "scene-bedroom",
        "location": "bedroom",
        "variant": "blue",
        "isNight": True,
        "startFrame": S_D,
        "endFrame": S_E,
        "cameraShots": cover(S_D, S_E, [
            lambda a, b: medium(a, b, [1.1, 0, 0.2], dist=16.8, fov=56),
            lambda a, b: close_up(a, b, HERO_BED_P, dist=7.4),
        ], target_sec=2.0),
        "characters": {
            "hero": hold(S_D, S_E, HERO_BED_P, 0.1, "idle", "deadpan", "mouth_tape"),
            "mom": hold(S_D, S_E, MOM_BED_P, -0.7, "idle", "smile", "counter_mid"),
        },
    })

    # E. SCHOOL EXTERIOR - counter glitches from 912,450 down to 3
    K1_P = [-4.5, 0, 0.0]
    K2_P = [0.0, 0, 0.0]
    HERO_SCH_P = [4.5, 0, 1.5]
    out.append({
        "id": "scene-glitch",
        "location": "school_exterior",
        "schoolName": "WORDVILLE HIGH",
        "startFrame": S_E,
        "endFrame": S_F,
        "cameraShots": [
            shot(S_E, GLITCH, [0.0, 8.0, 24.0], [0.5, 7.6, 22.0], [0.0, 4.6, 0.5], [0.5, 4.6, 0.5], 60),
            close_up(GLITCH, S_F, HERO_SCH_P, dist=7.6, shake=0.05),
        ],
        "characters": {
            "rich_kid": [
                kf(S_E, K1_P, 0.1, "idle", "cool", "counter_high"),
                kf(GLITCH, K1_P, face(K1_P, HERO_SCH_P), "idle", "shocked", "counter_high"),
                kf(S_F, K1_P, face(K1_P, HERO_SCH_P), "idle", "shocked", "counter_high"),
            ],
            "normal_kid": [
                kf(S_E, K2_P, 0.0, "wave", "smile", "counter_mid"),
                kf(GLITCH, K2_P, face(K2_P, HERO_SCH_P), "idle", "shocked", "counter_mid"),
                kf(S_F, K2_P, face(K2_P, HERO_SCH_P), "idle", "shocked", "counter_mid"),
            ],
            "hero": [
                kf(S_E, [7.5, 0, 4.0], -0.6, "walk", "smile", "counter_high"),
                kf(GLITCH - 8, HERO_SCH_P, -0.4, "walk", "smile", "counter_high"),
                kf(GLITCH - 2, HERO_SCH_P, 0.0, "idle", "smile", "counter_high"),
                kf(GLITCH, HERO_SCH_P, 0.0, "idle", "shocked", "counter_3"),
                kf(S_F, HERO_SCH_P, 0.0, "idle", "panic", "counter_3"),
            ],
        },
    })

    # F. HALLWAY - bully laughs
    HERO_HALL_P = [1.8, 0, 1.5]
    BULLY_HALL_P = [-3.0, 0, 1.5]
    out.append({
        "id": "scene-hallway",
        "location": "hallway",
        "startFrame": S_F,
        "endFrame": S_G,
        "cameraShots": split_shots(S_F, S_G, [
            lambda a, b: wide(a, b, [0, 0, 0.5], dist=22.0, fov=60),
            lambda a, b: close_up(a, b, HERO_HALL_P, dist=7.6),
        ]),
        "characters": {
            "hero": [
                kf(S_F, HERO_HALL_P, -0.4, "idle", "deadpan", "counter_3"),
                kf(B["b6"] + 24, HERO_HALL_P, -0.7, "idle", "panic", "counter_3"),
                kf(S_G, HERO_HALL_P, -0.7, "idle", "panic", "counter_3"),
            ],
            "bully": [
                kf(S_F, [-9.0, 0, 1.5], HALF, "walk", "angry", "counter_bully"),
                kf(B["b6"] + 22, BULLY_HALL_P, HALF, "walk", "angry", "counter_bully"),
                kf(B["b6"] + 26, BULLY_HALL_P, face(BULLY_HALL_P, HERO_HALL_P), "point", "laugh", "counter_bully"),
                kf(S_G, BULLY_HALL_P, face(BULLY_HALL_P, HERO_HALL_P), "point", "laugh", "counter_bully"),
            ],
            "rich_kid": hold(S_F, S_G, [5.8, 0, -2.5], -0.8, "celebrate", "laugh", "counter_high"),
            "normal_kid": hold(S_F, S_G, [-1.5, 0, -3.5], 0.3, "dance", "laugh", "counter_mid"),
        },
    })

    # G. CLASSROOM - silent in class
    out.append({
        "id": "scene-classroom",
        "location": "classroom",
        "boardText": ["WORD RULES", "SPEAK WISELY", "0 WORDS =", "SILENT FOREVER"],
        "startFrame": S_G,
        "endFrame": S_H,
        "cameraShots": split_shots(S_G, S_H, [
            lambda a, b: wide(a, b, [0, 0, 0.5], dist=26.5, fov=60),
            lambda a, b: close_up(a, b, [1.0, 0, 2.5], dist=7.6),
        ]),
        "characters": {
            "teacher": hold(S_G, S_H, [-5.5, 0, -6.8], 0.4, "point", "deadpan", "pointer"),
            "hero": hold(S_G, S_H, [1.0, 0, 2.5], 0.0, "idle", "deadpan", "counter_3"),
            "normal_kid": hold(S_G, S_H, [-5.5, 0, 3.0], 0.5, "idle", "smile", "counter_mid"),
            "bully": hold(S_G, S_H, [5.5, 0, 3.0], -0.6, "idle", "laugh", "counter_bully"),
        },
    })

    # H. PLAYGROUND - bully corners sister -> hero shouts LEAVE HER ALONE -> bully runs
    SIS_P = [4.6, 0, 1.5]
    BULLY_P = [0.0, 0, 1.5]
    HERO_PARK_P = [-4.8, 0, 0.8]
    out.append({
        "id": "scene-climax",
        "location": "playground",
        "startFrame": S_H,
        "endFrame": S_I,
        "cameraShots": [
            wide(S_H, B["b9"], center=[0.0, 0, 1.3], dist=23.5, fov=60),
            medium(B["b9"], B["b10"], center=[-2.4, 0, 1.2], dist=16.2, fov=56),
            shot(B["b10"], B["w1"], [-0.5, 5.0, 7.2], [-1.2, 4.8, 6.2], [-4.8, 4.4, 0.8], [-4.8, 4.4, 0.8], 46),
            shot(B["w1"], B["b11"], [1.8, 5.6, 15.5], [1.2, 5.4, 14.0], [-2.2, 4.4, 1.2], [-2.0, 4.4, 1.2], 54, 0.09),
            *split_shots(B["b11"], S_I, [
                lambda a, b: wide(a, b, center=[0.0, 0, 1.0], dist=23.5, fov=60),
                lambda a, b: close_up(a, b, HERO_PARK_P, dist=7.6),
            ]),
        ],
        "characters": {
            "sister": [
                kf(S_H, SIS_P, face(SIS_P, BULLY_P), "idle", "panic", "counter_mid"),
                kf(B["w3"], SIS_P, face(SIS_P, HERO_PARK_P), "idle", "shocked", "counter_mid"),
                kf(B["b11"], SIS_P, face(SIS_P, HERO_PARK_P), "celebrate", "laugh", "counter_mid"),
                kf(S_I, SIS_P, face(SIS_P, HERO_PARK_P), "celebrate", "laugh", "counter_mid"),
            ],
            "bully": [
                kf(S_H, BULLY_P, face(BULLY_P, SIS_P), "point", "angry", "counter_bully"),
                kf(B["w1"], BULLY_P, face(BULLY_P, HERO_PARK_P), "idle", "shocked", "counter_bully"),
                kf(B["w3"], BULLY_P, face(BULLY_P, HERO_PARK_P), "idle", "panic", "counter_bully"),
                kf(B["b11"], BULLY_P, 3.14, "sprint", "panic", "counter_bully"),
                kf(B["b11"] + 36, [0.0, 0, -14.0], 3.14, "sprint", "panic", "counter_bully"),
                kf(S_I, [0.0, 0, -14.0], 3.14, "sprint", "panic", "counter_bully"),
            ],
            "hero": [
                kf(S_H, [-6.2, 0, 1.5], HALF, "walk", "shocked", "counter_3"),
                kf(B["b9"] - 4, HERO_PARK_P, 0.9, "walk", "shocked", "counter_3"),
                kf(B["b9"], HERO_PARK_P, 0.9, "idle", "deadpan", "counter_3"),
                kf(B["w1"], HERO_PARK_P, 0.95, "point", "angry", "counter_2"),
                kf(B["w2"], HERO_PARK_P, 0.95, "point", "angry", "counter_1"),
                kf(B["w3"], HERO_PARK_P, 0.95, "point", "shocked", "counter_0"),
                kf(B["b11"], HERO_PARK_P, 0.2, "idle", "smile", "counter_0"),
                kf(S_I, HERO_PARK_P, 0.2, "idle", "smile", "counter_0"),
            ],
        },
    })

    # I. LIVING ROOM, NIGHT - mom cries, then golden halo cracks and turns RED
    HERO_LR_P = [0.0, 0, 1.2]
    MOM_LR_P = [4.5, 0, 0.8]
    SIS_LR_P = [-4.5, 0, 0.8]
    out.append({
        "id": "scene-twist",
        "location": "living_room",
        "variant": "blue",
        "isNight": True,
        "startFrame": S_I,
        "endFrame": END,
        "cameraShots": [
            wide(S_I, B["b13"], center=[0, 0, 1.0], dist=23.5, fov=60),
            medium(B["b13"], RED, center=[0, 0, 1.2], dist=11.0, fov=50),
            close_up(RED, END, HERO_LR_P, dist=6.8, shake=0.06),
        ],
        "characters": {
            "hero": [
                kf(S_I, HERO_LR_P, 0.0, "idle", "deadpan", "counter_0"),
                kf(RED, HERO_LR_P, 0.0, "idle", "shocked", "halo_red"),
                kf(END, HERO_LR_P, 0.0, "idle", "shocked", "halo_red"),
            ],
            "mom": [
                kf(S_I, MOM_LR_P, face(MOM_LR_P, HERO_LR_P), "idle", "panic", "counter_mid"),
                kf(RED, MOM_LR_P, face(MOM_LR_P, HERO_LR_P), "idle", "shocked", "counter_mid"),
                kf(END, MOM_LR_P, face(MOM_LR_P, HERO_LR_P), "idle", "shocked", "counter_mid"),
            ],
            "sister": [
                kf(S_I, SIS_LR_P, face(SIS_LR_P, HERO_LR_P), "idle", "deadpan", "counter_mid"),
                kf(RED, SIS_LR_P, face(SIS_LR_P, HERO_LR_P), "idle", "shocked", "counter_mid"),
                kf(END, SIS_LR_P, face(SIS_LR_P, HERO_LR_P), "idle", "shocked", "counter_mid"),
            ],
        },
    })

    return out
