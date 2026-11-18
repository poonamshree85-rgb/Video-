"""100 WORDS A DAY - 'In this world' Short.

In this world, everyone gets one hundred spoken words a day, shown by a floating
counter above their head. The hero saves every word for a year... until his
little sister needs him.

Build:   python scripts/make_short.py stories/one_hundred_words.py --stills
Render:  python scripts/make_short.py stories/one_hundred_words.py --skip-tts --render
"""
from shorts.scene import HALF, OFF, close_up, cover, face, hold, kf, shot  # noqa: F401

TITLE = "100 WORDS A DAY"

# 1. SCRIPT ------------------------------------------------------------------
BEATS = [
    {"id": "b1", "text": "In this world, everyone gets one hundred words a day.", "pause": 0.08},
    {"id": "b2", "text": "A counter above your head shows every word you have left.", "pause": 0.08},
    {"id": "b3", "text": "Spend them all, and you can't speak until midnight.", "pause": 0.08},
    {"id": "b4", "text": "Rich kids burn theirs on jokes and songs.", "pause": 0.08},
    {"id": "b5", "text": "My teacher makes us raise a finger for every word in class.", "pause": 0.07},
    {"id": "b6", "text": "The bully spends fifty words just to call me names.", "pause": 0.08},
    {"id": "b7", "text": "But me? I don't talk. I save every single word.", "pause": 0.08},
    {"id": "b8", "text": "The whole school calls me the Quiet Kid.", "pause": 0.07},
    {"id": "b9", "text": "Only my little sister thinks I'm saving up for something big.", "pause": 0.08},
    {"id": "b10", "text": "Then yesterday, she fell off the slide, and her counter hit zero.", "pause": 0.10},
    {"id": "b11", "text": "She couldn't even whisper for help.", "pause": 0.12},
    {"id": "w1", "text": "HELP!", "voice": "am_michael", "shout": True, "pause": 0.12},
    {"id": "w2", "text": "NOW!", "voice": "am_michael", "shout": True, "pause": 0.18},
    {"id": "b12", "text": "Mom ran the whole way, and stayed by her side.", "pause": 0.08},
    {"id": "b13", "text": "My counter read ninety-eight. Worth every single word.", "pause": 0.12},
    {"id": "b14", "text": "But last night, she spent her first new word on me... 'hero'.", "pause": 0.30},
]

# 2. MUSIC + SFX ---------------------------------------------------------------
MUSIC = {
    "file": "music/fallen-down.mp3",
    "under_voice": 0.022,
    "gaps": 0.05,
    "dropouts": [("b11+0.2", "w2.end")],   # silence before HELP! NOW!
}

SFX = [
    ("b1", "whoosh"),
    ("b2+0.3", "pop", {"f": 600}),
    ("b2+1.2", "pop", {"f": 720}),
    ("b3+0.6", "bell_low"),
    ("b4+0.8", "laugh"),
    ("b5", "ding_dong"),
    ("b6+1.2", "laugh"),
    ("b7+0.6", "sad"),
    ("b8+0.8", "laugh"),
    ("b9+0.8", "sparkle"),
    ("b10+1.4", "thud"),
    ("b11+0.5", "sad"),
    ("w1", "impact"),
    ("w2", "impact"),
    ("b12+0.4", "whoosh"),
    ("b13+0.8", "reveal"),
    ("b14+1.6", "twist"),
]

# 3. CAST ----------------------------------------------------------------------
HERO = {
    "extends": "kid_boy",
    "hair": {"style": "messyFringe", "color": "black"},
    "top": {"style": "hoodie", "color": "teal", "secondary": "white"},
    "bottom": {"style": "jeans", "color": "denim"},
    "shoes": {"color": "white", "sole": "white"},
    "accessories": ["headphones"],
}
CAST = {
    "hero": HERO,
    "sis": {"extends": "kid_girl", "hair": {"style": "pigtails", "color": "blonde"},
            "top": {"style": "dress", "color": "pink"}, "scale": 0.75},
    "mom": {"extends": "real_mom", "hair": {"style": "ponytail", "color": "brown"}},
    "rich_kid": {"extends": "cool_kid", "accessories": ["sunglasses"]},
    "classmate": {"extends": "schoolboy", "hair": {"style": "curly", "color": "brown"}},
    "bully": "bully",
    "teacher": {"extends": "teacher_woman", "hair": {"style": "bun", "color": "blonde"}},
}


# 4. SCENES ----------------------------------------------------------------------
def scenes(T):
    B, E, END = T.B, T.E, T.END

    S_B = B["b2"] - 1     # street: wasting words
    S_C = B["b5"] - 1     # classroom: teacher + bully
    S_D = B["b7"] - 1     # hallway: the Quiet Kid
    S_E = B["b9"] - 1     # playground: sister falls
    S_F = B["b13"] - 1    # living room, night: ninety-eight + twist

    FALL = B["b10"] + 24  # sister hits the ground
    MOM = B["b12"]        # mom sprints in

    scenes = []

    # A. TOWN OVERVIEW - hook --------------------------------------------------
    scenes.append({
        "id": "hook",
        "location": "town_overview",
        "startFrame": 0,
        "endFrame": S_B,
        "cameraShots": [shot(0, S_B, [-10, 62, 74], [-2, 46, 56], [8, 0, -6], [6, 2, -8], 55)],
        "characters": {},
    })

    # B. STREET - the rich kid burns his words ---------------------------------
    scenes.append({
        "id": "street",
        "location": "street",
        "startFrame": S_B,
        "endFrame": S_C,
        "cameraShots": [
            shot(S_B, B["b3"], [-2.2, 5.8, 13.5], [-2.8, 5.4, 11.8], [-3.5, 4.6, 0.5], [-3.5, 4.5, 0.5], 46),
            shot(B["b3"], B["b4"], [-8.0, 5.6, 12.0], [-8.4, 5.2, 10.6], [-9, 4.4, 0.5], [-9, 4.4, 0.5], 48),
            shot(B["b4"], S_C, [-0.8, 6.4, 15.0], [-2.6, 5.8, 12.8], [-3.5, 4.4, 0.5], [-3.5, 4.4, 0.5], 52),
        ],
        "characters": {
            "rich_kid": [kf(S_B, [-3.5, 0, 0.5], 0.2, "idle", "smile", "counter_12"),
                         kf(B["b4"], [-3.5, 0, 0.5], 0.2, "dance", "laugh", "counter_12"),
                         kf(S_C, [-3.5, 0, 0.5], 0.2, "dance", "laugh", "counter_12")],
            "hero": hold(S_B, S_C, [-9, 0, 0.5], 0.15, "idle", "deadpan", "counter_100"),
        },
    })

    # C. CLASSROOM - finger up for every word, bully spends fifty ----------------
    scenes.append({
        "id": "classroom",
        "location": "classroom",
        "boardText": ["WORD BUDGET", "SPEND WISELY", "100 WORDS A DAY"],
        "startFrame": S_C,
        "endFrame": S_D,
        "cameraShots": [
            shot(S_C, T.f("b5+1.7"), [0, 7.6, 19.5], [0, 7.0, 17.0], [0, 4.6, -2], [0, 4.5, -2], 56),
            shot(T.f("b5+1.7"), B["b6"], [-4.0, 6.0, 14.0], [-3.4, 5.4, 12.0], [-3.0, 4.5, 1], [-3.0, 4.4, 1], 50),
            shot(B["b6"], S_D, [7.0, 5.2, 10.0], [6.4, 4.9, 8.6], [5.5, 4.4, 3], [5.5, 4.4, 3], 46),
        ],
        "characters": {
            "teacher": [kf(S_C, [-5.5, 0, -6.8], 0.4, "idle", "smile", "pointer"),
                        kf(T.f("b5+1.7"), [-5.5, 0, -6.8], 0.4, "point", "smile", "pointer"),
                        kf(S_D, [-5.5, 0, -6.8], 0.4, "point", "smile", "pointer")],
            "classmate": hold(S_C, S_D, [-5.5, 0, 3], 0.5, "point", "cool", "counter_100"),
            "hero": hold(S_C, S_D, [0.5, 0, 2.5], 0.1, "idle", "deadpan", "counter_100"),
            "bully": [kf(S_C, [5.5, 0, 3], -0.4, "idle", "angry", "counter_50"),
                      kf(B["b6"], [5.5, 0, 3], -0.4, "point", "laugh", "counter_50"),
                      kf(S_D, [5.5, 0, 3], -0.4, "point", "laugh", "counter_50")],
        },
    })

    # D. HALLWAY - the Quiet Kid gets laughed at ---------------------------------
    scenes.append({
        "id": "hallway",
        "location": "hallway",
        "startFrame": S_D,
        "endFrame": S_E,
        "cameraShots": [
            close_up(S_D, T.f("b7+1.6"), [1.5, 0, 1.5]),
            shot(T.f("b7+1.6"), B["b8"], [0.2, 6.2, 15.0], [0.6, 5.6, 13.0], [1.5, 4.5, 1.5], [1.5, 4.4, 1.5], 50),
            shot(B["b8"], S_E, [-3.0, 6.4, 17.0], [-2.2, 5.8, 15.0], [-0.5, 4.5, 0], [-0.5, 4.4, 0], 56),
        ],
        "characters": {
            "hero": [kf(S_D, [1.5, 0, 1.5], 0, "idle", "deadpan", "counter_100"),
                     kf(S_E, [1.5, 0, 1.5], 0, "idle", "deadpan", "counter_100")],
            "classmate": [kf(S_D, [-1.0, 0, -3.5], 3.1, "idle", "smile", "counter_100"),
                          kf(B["b8"], [-1.0, 0, -3.5], 3.1, "idle", "cool", "counter_100"),
                          kf(B["b8"] + 12, [-1.0, 0, -3.5], -0.8, "point", "laugh", "counter_100"),
                          kf(S_E, [-1.0, 0, -3.5], -0.8, "point", "laugh", "counter_100")],
            "bully": [kf(S_D, [-12, 0, 1.5], HALF, "idle", "angry", "counter_50"),
                      kf(B["b8"], [-12, 0, 1.5], HALF, "walk", "angry", "counter_50"),
                      kf(B["b8"] + 22, [-3.5, 0, 1.5], HALF, "walk", "angry", "counter_50"),
                      kf(B["b8"] + 26, [-3.5, 0, 1.5], 1.1, "point", "laugh", "counter_50"),
                      kf(S_E, [-3.5, 0, 1.5], 1.1, "point", "laugh", "counter_50")],
        },
    })

    # E. PLAYGROUND - sister falls, her counter hits zero, HELP! -----------------
    scenes.append({
        "id": "playground",
        "location": "playground",
        "startFrame": S_E,
        "endFrame": S_F,
        "cameraShots": [
            shot(S_E, B["b10"], [0, 6.6, 15.5], [0.5, 6.0, 13.0], [0, 4.2, 2], [0, 4.0, 2], 54),
            shot(B["b10"], T.f("b10+2.0"), [2.0, 5.8, 11.5], [3.4, 4.6, 8.8], [4.5, 3.6, 0.5], [4.5, 3.4, 0.5], 50),
            shot(T.f("b10+2.0"), B["b11"], [3.4, 4.6, 8.8], [3.0, 4.2, 7.4], [4.5, 3.4, 0.5], [4.5, 3.3, 0.5], 48),
            shot(B["b11"], B["w1"], [-0.5, 5.2, 8.5], [-1.0, 4.9, 7.0], [-1.5, 4.4, 2.5], [-1.5, 4.3, 2.5], 46),
            shot(B["w1"], B["b12"], [-2.5, 5.4, 9.5], [-2.0, 5.0, 8.0], [-1.5, 4.4, 2.5], [-1.5, 4.4, 2.5], 48, 0.08),
            shot(B["b12"], S_F, [0, 7.2, 17.5], [0, 6.6, 15.5], [0, 4.2, 0], [0, 4.0, 0], 58),
        ],
        "characters": {
            "sis": [kf(S_E, [2.5, 0, 2], -0.55, "wave", "laugh", "counter_100"),
                    kf(B["b10"] - 6, [2.5, 0, 2], -0.55, "idle", "smile", "counter_100"),
                    kf(B["b10"], [2.5, 0, 2], HALF, "walk", "smile", "counter_100"),
                    kf(B["b10"] + 20, [4.5, 0, 0.5], HALF, "walk", "smile", "counter_100"),
                    kf(FALL, [4.5, 0, 0.5], HALF, "knocked", "shocked", "counter_0"),
                    kf(S_F, [4.5, 0, 0.5], HALF, "knocked", "sleeping", "counter_0")],
            "hero": [kf(S_E, [-2.5, 0, 2], 0.55, "idle", "smile", "counter_100"),
                     kf(B["b10"] + 24, [-2.5, 0, 2], 0.55, "idle", "shocked", "counter_100"),
                     kf(B["b10"] + 30, [-2.5, 0, 2], HALF, "walk", "panic", "counter_100"),
                     kf(B["b10"] + 50, [-1.5, 0, 2.5], HALF, "walk", "panic", "counter_100"),
                     kf(B["b10"] + 56, [-1.5, 0, 2.5], 0.3, "idle", "panic", "counter_100"),
                     kf(B["w1"], [-1.5, 0, 2.5], 0.3, "point", "panic", "counter_100"),
                     kf(B["w2"], [-1.5, 0, 2.5], 0.3, "point", "panic", "counter_100"),
                     kf(B["b12"], [-1.5, 0, 2.5], 0.3, "idle", "panic", "counter_100"),
                     kf(S_F, [-1.5, 0, 2.5], 0.3, "idle", "panic", "counter_100")],
            "mom": [kf(S_E, OFF, 0, "idle", "smile"),
                    kf(MOM, OFF, 0, "idle", "smile"),
                    kf(MOM + 2, [-14, 0, 2], HALF, "sprint", "panic"),
                    kf(MOM + 40, [2, 0, -3.5], HALF, "sprint", "panic"),
                    kf(MOM + 46, [2, 0, -3.5], 0.9, "idle", "panic"),
                    kf(S_F, [2, 0, -3.5], 0.9, "idle", "panic")],
        },
    })

    # F. LIVING ROOM, NIGHT - ninety-eight, then 'hero' --------------------------
    WAKE = T.f("b14+1.8")
    scenes.append({
        "id": "twist",
        "location": "living_room",
        "variant": "yellow",
        "isNight": True,
        "startFrame": S_F,
        "endFrame": END,
        "cameraShots": [
            shot(S_F, B["b14"], [-3.0, 5.2, 11.5], [-3.8, 4.8, 9.8], [-4.5, 4.4, 1.5], [-4.5, 4.4, 1.5], 46),
            shot(B["b14"], WAKE, [0, 5.6, 11.0], [0, 4.8, 9.0], [0, 3.4, 0.5], [0, 3.3, 0.5], 46),
            close_up(WAKE, END, [0, 0, 0.5], scale=0.75),
        ],
        "characters": {
            "hero": [kf(S_F, [-4.5, 0, 1.5], 0.6, "idle", "shocked", "counter_98"),
                     kf(B["b14"], [-4.5, 0, 1.5], 0.6, "idle", "shocked", "counter_98"),
                     kf(WAKE, [-4.5, 0, 1.5], 0.6, "idle", "smile", "counter_98"),
                     kf(END, [-4.5, 0, 1.5], 0.6, "celebrate", "laugh", "counter_98")],
            "sis": [kf(S_F, [0, 0, 0.5], 0, "idle", "sleeping", "counter_99"),
                    kf(B["b14"], [0, 0, 0.5], 0, "wave", "laugh", "counter_99"),
                    kf(END, [0, 0, 0.5], 0, "wave", "laugh", "counter_99")],
            "mom": hold(S_F, END, [4.5, 0, 1.5], -0.6, "idle", "smile"),
        },
    })

    return scenes
