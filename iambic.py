#!/usr/bin/env python3
"""
Iambic Pentameter Poem Generator
=================================
Generates poems in iambic pentameter (da-DUM × 5, 10 syllables per line)
using a vocabulary tagged with stress patterns and grammatical templates
to produce semi-coherent, metrically correct verse.

Stress notation:  0 = unstressed,  1 = stressed
Iambic pentameter target: 0 1 0 1 0 1 0 1 0 1
"""

import random
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Vocabulary: each word is tagged with its stress pattern and part of speech.
# Pattern uses 0 (unstressed) and 1 (stressed).
# ---------------------------------------------------------------------------

@dataclass
class Word:
    text: str
    stress: str          # e.g. "01" for iambic disyllable
    pos: str             # part-of-speech tag

# Shorthand builder
def _w(text, stress, pos):
    return Word(text, stress, pos)

# --- Articles / Determiners (mostly unstressed) ---
DETERMINERS = [
    _w("the",    "0", "det"),
    _w("a",      "0", "det"),
    _w("my",     "0", "det"),
    _w("your",   "0", "det"),
    _w("her",    "0", "det"),
    _w("his",    "0", "det"),
    _w("our",    "0", "det"),
    _w("their",  "0", "det"),
    _w("this",   "0", "det"),
    _w("that",   "0", "det"),
    _w("each",   "0", "det"),
    _w("no",     "0", "det"),
    _w("some",   "0", "det"),
]

# --- Prepositions (mostly unstressed) ---
PREPOSITIONS = [
    _w("in",      "0",  "prep"),
    _w("of",      "0",  "prep"),
    _w("to",      "0",  "prep"),
    _w("with",    "0",  "prep"),
    _w("by",      "0",  "prep"),
    _w("from",    "0",  "prep"),
    _w("on",      "0",  "prep"),
    _w("at",      "0",  "prep"),
    _w("for",     "0",  "prep"),
    _w("through", "1",  "prep"),
    _w("past",    "1",  "prep"),
    _w("down",    "1",  "prep"),
    _w("near",    "1",  "prep"),
    _w("like",    "1",  "prep"),
    _w("round",   "1",  "prep"),
    _w("since",   "1",  "prep"),
    _w("toward",  "01", "prep"),
    _w("among",   "01", "prep"),
    _w("upon",    "01", "prep"),
    _w("across",  "01", "prep"),
    _w("above",   "01", "prep"),
    _w("below",   "01", "prep"),
    _w("beyond",  "01", "prep"),
    _w("beside",  "01", "prep"),
    _w("beneath", "01", "prep"),
    _w("between", "01", "prep"),
    _w("before",  "01", "prep"),
    _w("within",  "01", "prep"),
    _w("without", "01", "prep"),
    _w("around",  "01", "prep"),
    _w("behind",  "01", "prep"),
]

# --- Pronouns ---
PRONOUNS = [
    _w("I",     "1", "pron"),
    _w("we",    "1", "pron"),
    _w("you",   "1", "pron"),
    _w("they",  "1", "pron"),
    _w("he",    "1", "pron"),
    _w("she",   "1", "pron"),
    _w("it",    "0", "pron"),
    _w("who",   "1", "pron"),
    _w("what",  "1", "pron"),
    _w("all",   "1", "pron"),
    _w("none",  "1", "pron"),
]

# --- Conjunctions ---
CONJUNCTIONS = [
    _w("and",  "0", "conj"),
    _w("but",  "0", "conj"),
    _w("or",   "0", "conj"),
    _w("yet",  "1", "conj"),
    _w("nor",  "1", "conj"),
    _w("for",  "0", "conj"),
    _w("so",   "1", "conj"),
    _w("while","1", "conj"),
    _w("though","1","conj"),
    _w("since","1", "conj"),
    _w("when", "1", "conj"),
]

# --- Adjectives ---
ADJECTIVES = [
    # monosyllabic (stressed)
    _w("dark",     "1",   "adj"),
    _w("bright",   "1",   "adj"),
    _w("cold",     "1",   "adj"),
    _w("warm",     "1",   "adj"),
    _w("soft",     "1",   "adj"),
    _w("deep",     "1",   "adj"),
    _w("pale",     "1",   "adj"),
    _w("sweet",    "1",   "adj"),
    _w("lost",     "1",   "adj"),
    _w("old",      "1",   "adj"),
    _w("young",    "1",   "adj"),
    _w("wide",     "1",   "adj"),
    _w("fair",     "1",   "adj"),
    _w("wild",     "1",   "adj"),
    _w("true",     "1",   "adj"),
    _w("still",    "1",   "adj"),
    _w("slow",     "1",   "adj"),
    _w("bold",     "1",   "adj"),
    _w("vast",     "1",   "adj"),
    _w("long",     "1",   "adj"),
    _w("brief",    "1",   "adj"),
    _w("frail",    "1",   "adj"),
    _w("fierce",   "1",   "adj"),
    _w("proud",    "1",   "adj"),
    _w("green",    "1",   "adj"),
    _w("grey",     "1",   "adj"),
    _w("bare",     "1",   "adj"),
    # disyllabic
    _w("gentle",   "10",  "adj"),
    _w("silent",   "10",  "adj"),
    _w("golden",   "10",  "adj"),
    _w("silver",   "10",  "adj"),
    _w("crimson",  "10",  "adj"),
    _w("ancient",  "10",  "adj"),
    _w("hollow",   "10",  "adj"),
    _w("bitter",   "10",  "adj"),
    _w("broken",   "10",  "adj"),
    _w("woven",    "10",  "adj"),
    _w("lonely",   "10",  "adj"),
    _w("weary",    "10",  "adj"),
    _w("slender",  "10",  "adj"),
    _w("tender",   "10",  "adj"),
    _w("distant",  "10",  "adj"),
    _w("secret",   "10",  "adj"),
    _w("heavy",    "10",  "adj"),
    _w("mortal",   "10",  "adj"),
    _w("sombre",   "10",  "adj"),
    _w("eternal",  "010", "adj"),
    _w("serene",   "01",  "adj"),
    _w("divine",   "01",  "adj"),
    _w("alone",    "01",  "adj"),
    _w("unseen",   "01",  "adj"),
    _w("forlorn",  "01",  "adj"),
    _w("unknown",  "01",  "adj"),
    _w("immense",  "01",  "adj"),
    _w("profound",  "01", "adj"),
    _w("sublime",  "01",  "adj"),
    _w("obscure",  "01",  "adj"),
    _w("remote",   "01",  "adj"),
    _w("complete", "01",  "adj"),
    _w("entire",   "01",  "adj"),
    _w("alive",    "01",  "adj"),
    _w("awake",    "01",  "adj"),
    _w("immense",  "01",  "adj"),
    _w("forgotten","010", "adj"),
    _w("beautiful","100", "adj"),
    _w("delicate", "100", "adj"),
    _w("luminous", "100", "adj"),
]

# --- Nouns ---
NOUNS = [
    # monosyllabic
    _w("night",    "1",   "noun"),
    _w("light",    "1",   "noun"),
    _w("dream",    "1",   "noun"),
    _w("flame",    "1",   "noun"),
    _w("moon",     "1",   "noun"),
    _w("sun",      "1",   "noun"),
    _w("star",     "1",   "noun"),
    _w("wind",     "1",   "noun"),
    _w("rain",     "1",   "noun"),
    _w("fire",     "1",   "noun"),
    _w("earth",    "1",   "noun"),
    _w("stone",    "1",   "noun"),
    _w("bone",     "1",   "noun"),
    _w("sea",      "1",   "noun"),
    _w("sky",      "1",   "noun"),
    _w("heart",    "1",   "noun"),
    _w("mind",     "1",   "noun"),
    _w("soul",     "1",   "noun"),
    _w("song",     "1",   "noun"),
    _w("time",     "1",   "noun"),
    _w("rose",     "1",   "noun"),
    _w("leaf",     "1",   "noun"),
    _w("tree",     "1",   "noun"),
    _w("wave",     "1",   "noun"),
    _w("shore",    "1",   "noun"),
    _w("path",     "1",   "noun"),
    _w("dawn",     "1",   "noun"),
    _w("dusk",     "1",   "noun"),
    _w("dust",     "1",   "noun"),
    _w("ghost",    "1",   "noun"),
    _w("shade",    "1",   "noun"),
    _w("vale",     "1",   "noun"),
    _w("gate",     "1",   "noun"),
    _w("crown",    "1",   "noun"),
    _w("throne",   "1",   "noun"),
    _w("blood",    "1",   "noun"),
    _w("breath",   "1",   "noun"),
    _w("stream",   "1",   "noun"),
    _w("field",    "1",   "noun"),
    _w("world",    "1",   "noun"),
    _w("grace",    "1",   "noun"),
    _w("storm",    "1",   "noun"),
    _w("frost",    "1",   "noun"),
    _w("spring",   "1",   "noun"),
    _w("cliff",    "1",   "noun"),
    _w("peak",     "1",   "noun"),
    # disyllabic
    _w("shadow",   "10",  "noun"),
    _w("river",    "10",  "noun"),
    _w("forest",   "10",  "noun"),
    _w("garden",   "10",  "noun"),
    _w("mountain", "10",  "noun"),
    _w("ocean",    "10",  "noun"),
    _w("winter",   "10",  "noun"),
    _w("summer",   "10",  "noun"),
    _w("morning",  "10",  "noun"),
    _w("evening",  "10",  "noun"),
    _w("silence",  "10",  "noun"),
    _w("sorrow",   "10",  "noun"),
    _w("spirit",   "10",  "noun"),
    _w("ember",    "10",  "noun"),
    _w("temple",   "10",  "noun"),
    _w("mirror",   "10",  "noun"),
    _w("feather",  "10",  "noun"),
    _w("flower",   "10",  "noun"),
    _w("wonder",   "10",  "noun"),
    _w("thunder",  "10",  "noun"),
    _w("whisper",  "10",  "noun"),
    _w("meadow",   "10",  "noun"),
    _w("slumber",  "10",  "noun"),
    _w("voyage",   "10",  "noun"),
    _w("kingdom",  "10",  "noun"),
    _w("heaven",   "10",  "noun"),
    _w("desire",   "01",  "noun"),
    _w("despair",  "01",  "noun"),
    _w("delight",  "01",  "noun"),
    _w("regret",   "01",  "noun"),
    _w("eclipse",  "01",  "noun"),
    _w("embrace",  "01",  "noun"),
    _w("refrain",  "01",  "noun"),
    _w("lament",   "01",  "noun"),
    _w("decay",    "01",  "noun"),
    _w("resolve",  "01",  "noun"),
    # trisyllabic
    _w("memory",   "100", "noun"),
    _w("solitude", "100", "noun"),
    _w("interval", "100", "noun"),
    _w("canopy",   "100", "noun"),
    _w("melody",   "100", "noun"),
    _w("reverie",  "100", "noun"),
    _w("infinity", "0100","noun"),
    _w("horizon",  "010", "noun"),
    _w("tomorrow",  "010","noun"),
    _w("obsidian", "0100","noun"),
]

# --- Verbs ---
VERBS = [
    # monosyllabic
    _w("flows",    "1",   "verb"),
    _w("burns",    "1",   "verb"),
    _w("falls",    "1",   "verb"),
    _w("fades",    "1",   "verb"),
    _w("turns",    "1",   "verb"),
    _w("grows",    "1",   "verb"),
    _w("shines",   "1",   "verb"),
    _w("breaks",   "1",   "verb"),
    _w("calls",    "1",   "verb"),
    _w("dreams",   "1",   "verb"),
    _w("sleeps",   "1",   "verb"),
    _w("wakes",    "1",   "verb"),
    _w("weeps",    "1",   "verb"),
    _w("sighs",    "1",   "verb"),
    _w("sings",    "1",   "verb"),
    _w("moves",    "1",   "verb"),
    _w("waits",    "1",   "verb"),
    _w("holds",    "1",   "verb"),
    _w("flies",    "1",   "verb"),
    _w("stands",   "1",   "verb"),
    _w("bends",    "1",   "verb"),
    _w("gleams",   "1",   "verb"),
    _w("blooms",   "1",   "verb"),
    _w("knows",    "1",   "verb"),
    _w("rests",    "1",   "verb"),
    _w("dwells",   "1",   "verb"),
    _w("kept",     "1",   "verb"),
    _w("found",    "1",   "verb"),
    # disyllabic (iambic)
    _w("begins",   "01",  "verb"),
    _w("becomes",  "01",  "verb"),
    _w("returns",  "01",  "verb"),
    _w("remains",  "01",  "verb"),
    _w("reveals",  "01",  "verb"),
    _w("descends", "01",  "verb"),
    _w("ascends",  "01",  "verb"),
    _w("awaits",   "01",  "verb"),
    _w("endures",  "01",  "verb"),
    _w("recalls",  "01",  "verb"),
    _w("unfolds",  "01",  "verb"),
    _w("forgives", "01",  "verb"),
    _w("devours",  "01",  "verb"),
    _w("persists", "01",  "verb"),
    _w("ignites",  "01",  "verb"),
    _w("consumes", "01",  "verb"),
    _w("suspends", "01",  "verb"),
    _w("dissolves", "01", "verb"),
    _w("embraces", "010", "verb"),
    _w("surrenders","010","verb"),
    _w("remembers","010", "verb"),
    _w("abandons", "010", "verb"),
    # disyllabic (trochaic)
    _w("wanders",  "10",  "verb"),
    _w("whispers", "10",  "verb"),
    _w("gathers",  "10",  "verb"),
    _w("lingers",  "10",  "verb"),
    _w("trembles", "10",  "verb"),
    _w("echoes",   "10",  "verb"),
    _w("flickers", "10",  "verb"),
    _w("falters",  "10",  "verb"),
    _w("glimmers", "10",  "verb"),
    _w("scatters",  "10", "verb"),
    _w("withers",  "10",  "verb"),
    _w("murmurs",  "10",  "verb"),
    _w("shimmers", "10",  "verb"),
    _w("follows",  "10",  "verb"),
    _w("carries",  "10",  "verb"),
]

# --- Adverbs ---
ADVERBS = [
    _w("still",     "1",   "adv"),
    _w("now",       "1",   "adv"),
    _w("here",      "1",   "adv"),
    _w("there",     "1",   "adv"),
    _w("once",      "1",   "adv"),
    _w("then",      "0",   "adv"),
    _w("so",        "1",   "adv"),
    _w("yet",       "1",   "adv"),
    _w("far",       "1",   "adv"),
    _w("near",      "1",   "adv"),
    _w("ever",      "10",  "adv"),
    _w("never",     "10",  "adv"),
    _w("always",    "10",  "adv"),
    _w("gently",    "10",  "adv"),
    _w("softly",    "10",  "adv"),
    _w("slowly",    "10",  "adv"),
    _w("sweetly",   "10",  "adv"),
    _w("only",      "10",  "adv"),
    _w("solely",    "10",  "adv"),
    _w("alone",     "01",  "adv"),
    _w("again",     "01",  "adv"),
    _w("away",      "01",  "adv"),
    _w("below",     "01",  "adv"),
    _w("above",     "01",  "adv"),
    _w("perhaps",   "01",  "adv"),
    _w("forever",   "010", "adv"),
]

# --- Auxiliary / linking ---
AUXILIARIES = [
    _w("shall",  "1",  "aux"),
    _w("will",   "1",  "aux"),
    _w("may",    "1",  "aux"),
    _w("must",   "1",  "aux"),
    _w("can",    "1",  "aux"),
    _w("could",  "1",  "aux"),
    _w("would",  "1",  "aux"),
    _w("might",  "1",  "aux"),
    _w("has",    "1",  "aux"),
    _w("had",    "1",  "aux"),
    _w("was",    "0",  "aux"),
    _w("is",     "0",  "aux"),
    _w("are",    "0",  "aux"),
    _w("were",   "0",  "aux"),
    _w("do",     "1",  "aux"),
    _w("does",   "1",  "aux"),
    _w("not",    "1",  "aux"),
    _w("have",   "1",  "aux"),
]

# --- Relative / subordinating ---
RELATIVES = [
    _w("that",   "0",  "rel"),
    _w("which",  "0",  "rel"),
    _w("where",  "1",  "rel"),
    _w("when",   "1",  "rel"),
    _w("while",  "1",  "rel"),
    _w("whose",  "1",  "rel"),
    _w("as",     "0",  "rel"),
    _w("if",     "0",  "rel"),
]

# Combine into a flat pool indexed by stress pattern
ALL_WORDS: list[Word] = (
    DETERMINERS + PREPOSITIONS + PRONOUNS + CONJUNCTIONS +
    ADJECTIVES + NOUNS + VERBS + ADVERBS + AUXILIARIES + RELATIVES
)

WORDS_BY_STRESS: dict[str, list[Word]] = {}
for w in ALL_WORDS:
    WORDS_BY_STRESS.setdefault(w.stress, []).append(w)

WORDS_BY_POS: dict[str, list[Word]] = {}
for w in ALL_WORDS:
    WORDS_BY_POS.setdefault(w.pos, []).append(w)


# ---------------------------------------------------------------------------
# Line templates: sequences of (pos, stress_pattern) tuples.
# Each template's stress patterns must concatenate to "0101010101".
# ---------------------------------------------------------------------------

LINE_TEMPLATES = [
    # "the DARK and SILent RIVer FLOWS aLONE"
    # det(0) adj(1) conj(0) adj(10) noun(10) verb(1) adv(01)
    [("det","0"), ("adj","1"), ("conj","0"), ("adj","10"), ("noun","10"), ("verb","1"), ("adv","01")],

    # "beLOW the GOLDen SHAD-ows OF the NIGHT"
    # prep(01) det(0) adj(10) noun(10) prep(0) det(0) noun(1)
    # stress: 01 0 10 10 0 0 1 → 0101010 01 → need to fix
    # Let me recalculate...
    # prep(01)=01, det(0)=0, adj(1)=1, noun(10)=10, verb(1)=1, prep(0)=0, det(0) ... hmm

    # "upon the golden river winter calls"
    # prep(01) det(0) adj(10) noun(10) noun(10) verb(1) — that's only 0+1+0+10+10+10+1 = 01010 10101 nope

    # Simpler reliable patterns:

    # det adj noun prep det adj noun   (0 1 1 0 0 1 1 — no)
    # Let me be very systematic.  Target: 0 1 0 1 0 1 0 1 0 1

    # Pattern A:  0  1  0  1  0  1  0  1  0  1
    #            det adj det adj det adj det adj det noun
    # e.g. "the dark, the cold, the deep, the pale, the night"
    # Too repetitive. Let's use more natural templates.

    # Template: det(0) noun(1) verb(1) — wait, need unstressed between stresses

    # I'll spell out the 10-beat pattern explicitly:
    # pos:    0    1    0    1    0    1    0    1    0    1

    # T1: det  adj  prep det  adj  noun verb prep det  noun
    #     the  dark  of  the  wild  wind  blows through the  night
    [("det","0"),("adj","1"),("prep","0"),("det","0"),("adj","1"),("noun","1"),("verb","1"),("prep","0"),("det","0"),("noun","1")],
    # stress check: 0+1+0+0+1+1+1+0+0+1 = 0100111001 — NO, not iambic

    # OK let me think more carefully. The key insight: I need to pick words
    # whose stress patterns concatenate to exactly "0101010101".
    # So I need template combos summing to length 10 matching that pattern.

    # Easiest reliable approach: use the pattern as a constraint and
    # greedily pick words that match the remaining pattern.

    # Approach: TEMPLATE-FREE greedy/backtracking assembly
]

# ---------------------------------------------------------------------------
# Pattern-matching line builder (greedy with restarts)
# ---------------------------------------------------------------------------

IAMBIC_PENTAMETER = "0101010101"

# Grammar transition weights: which POS can follow which
# This prevents nonsensical sequences
TRANSITIONS: dict[str, list[tuple[str, float]]] = {
    "__start__": [
        ("det", 3), ("prep", 2), ("pron", 3), ("adv", 2),
        ("adj", 1), ("conj", 0.3), ("rel", 1), ("aux", 0.5),
    ],
    "det":  [("adj", 5), ("noun", 5), ("adv", 0.5)],
    "adj":  [("noun", 6), ("adj", 1.5), ("conj", 1)],
    "noun": [("verb", 6), ("prep", 2), ("conj", 2), ("rel", 1.5), ("aux", 1.5)],
    "verb": [("det", 3), ("prep", 2), ("adv", 3), ("adj", 2),
             ("noun", 2), ("pron", 1.5), ("rel", 1)],
    "prep": [("det", 5), ("adj", 3), ("noun", 3), ("pron", 1.5)],
    "pron": [("verb", 5), ("aux", 3), ("adv", 1.5)],
    "adv":  [("verb", 3), ("adj", 2.5), ("prep", 1), ("det", 1.5),
             ("conj", 1.5), ("noun", 0.5)],
    "conj": [("det", 3), ("adj", 2), ("noun", 2), ("pron", 3),
             ("adv", 1.5), ("prep", 1)],
    "rel":  [("det", 3), ("pron", 2.5), ("noun", 2), ("adj", 1.5),
             ("adv", 1.5), ("aux", 1.5)],
    "aux":  [("verb", 4), ("adv", 2.5), ("adj", 1.5), ("noun", 1)],
}


def _weighted_choice(options: list[tuple[str, float]]) -> str:
    """Pick from weighted options."""
    total = sum(w for _, w in options)
    r = random.uniform(0, total)
    cumulative = 0.0
    for item, weight in options:
        cumulative += weight
        if r <= cumulative:
            return item
    return options[-1][0]


def _pick_word(pos: str, stress_needed: str, used_recently: set[str]) -> Word | None:
    """Find a word with the given POS whose stress matches stress_needed."""
    candidates = [
        w for w in WORDS_BY_POS.get(pos, [])
        if w.stress == stress_needed and w.text not in used_recently
    ]
    if not candidates:
        # Relax the "recently used" constraint
        candidates = [
            w for w in WORDS_BY_POS.get(pos, [])
            if w.stress == stress_needed
        ]
    return random.choice(candidates) if candidates else None


def build_line(target: str = IAMBIC_PENTAMETER, max_attempts: int = 500) -> list[Word]:
    """
    Build one line of iambic pentameter by greedily selecting words
    whose stress patterns tile the target pattern.
    Uses POS transitions to encourage grammatical coherence.
    Tracks POS history to prevent repetitive structures.
    """
    for _ in range(max_attempts):
        words: list[Word] = []
        remaining = target
        prev_pos = "__start__"
        used = set()
        pos_history: list[str] = []
        stuck = False

        while remaining:
            # Choose a POS based on transition weights
            transitions = TRANSITIONS.get(prev_pos, TRANSITIONS["__start__"])

            placed = False
            # Build weighted order with penalties for recent POS repetition
            weighted = []
            for pos, base_weight in transitions:
                weight = base_weight
                # Penalize if this POS appeared in the last 2 words
                if pos in pos_history[-2:]:
                    weight *= 0.1
                # Penalize verb-adverb-verb loops
                if pos == "verb" and len(pos_history) >= 2 and pos_history[-1] == "adv" and pos_history[-2] == "verb":
                    weight *= 0.05
                if pos == "adv" and len(pos_history) >= 2 and pos_history[-1] == "verb" and pos_history[-2] == "adv":
                    weight *= 0.05
                # Bonus for underrepresented POS in this line
                if pos in ("noun", "det") and pos not in pos_history[-3:]:
                    weight *= 1.5
                weighted.append((pos, weight))

            random.shuffle(weighted)
            weighted.sort(key=lambda x: x[1] + random.uniform(0, x[1] * 0.5),
                          reverse=True)
            pos_order = [p for p, _ in weighted]

            tried_pos = set()
            for pos in pos_order:
                if pos in tried_pos:
                    continue
                tried_pos.add(pos)

                # Try stress patterns, alternating preference for length
                available_stresses = list(set(
                    w.stress for w in WORDS_BY_POS.get(pos, [])
                ))
                # Randomly prefer either longer or shorter patterns
                # to avoid always picking the same tiling
                if random.random() < 0.4:
                    # Prefer shorter (more words = more variety)
                    available_stresses.sort(key=lambda s: len(s))
                else:
                    # Prefer longer (fewer words, different rhythm)
                    available_stresses.sort(key=lambda s: len(s), reverse=True)
                for stress in available_stresses:
                    if remaining.startswith(stress):
                        word = _pick_word(pos, stress, used)
                        if word:
                            words.append(word)
                            remaining = remaining[len(stress):]
                            prev_pos = pos
                            pos_history.append(pos)
                            used.add(word.text)
                            placed = True
                            break
                if placed:
                    break

            if not placed:
                stuck = True
                break

        if not stuck and len(remaining) == 0:
            return words

    # Fallback — should rarely happen with a decent vocabulary
    return []


def stress_repr(words: list[Word]) -> str:
    """Show the stress pattern of a line."""
    return "".join(w.stress for w in words)


def scan_line(words: list[Word]) -> str:
    """Pretty-print the scansion marks (˘ = unstressed, / = stressed)."""
    pattern = stress_repr(words)
    return " ".join("/" if c == "1" else "˘" for c in pattern)


# ---------------------------------------------------------------------------
# Rhyme helpers (approximate: match last stressed vowel onward)
# ---------------------------------------------------------------------------

# Group words by their ending sounds for approximate rhyming
RHYME_GROUPS: dict[str, list[str]] = {}

def _build_rhyme_groups():
    """Build rhyme groups from actual vocabulary, curated for true rhymes."""
    vocab = set(w.text.lower() for w in ALL_WORDS)

    # Hand-curated rhyme families (only using words in our vocabulary)
    families = {
        "-ight":  ["night", "light", "bright", "delight", "might"],
        "-eam":   ["dream", "stream", "gleams"],
        "-oon":   ["moon"],
        "-ire":   ["fire", "desire", "entire"],
        "-ose":   ["rose", "flows", "grows", "knows"],
        "-ine":   ["divine", "shine"],
        "-old":   ["cold", "bold", "old"],
        "-one":   ["stone", "bone", "alone", "throne", "unknown"],
        "-ade":   ["shade"],
        "-ain":   ["rain", "refrain"],
        "-ear":   ["near", "here"],
        "-ay":    ["away", "decay", "grey", "day"],
        "-ee":    ["sea", "tree"],
        "-ound":  ["found", "profound", "around", "round"],
        "-all":   ["calls", "falls", "recalls"],
        "-eep":   ["deep", "sleeps", "weeps"],
        "-ing":   ["spring", "sings"],
        "-art":   ["heart", "start"],
        "-eath":  ["breath", "beneath"],
        "-ust":   ["dust", "must"],
        "-ame":   ["flame", "name"],
        "-ace":   ["grace", "embrace"],
        "-ong":   ["song", "long", "among"],
        "-orm":   ["storm", "warm"],
        "-orn":   ["forlorn", "dawn"],
        "-own":   ["crown", "down", "unknown"],
        "-air":   ["bare", "fair", "despair"],
        "-ime":   ["time", "sublime"],
        "-ow":    ["below", "slow", "shadow", "meadow", "sorrow"],
        "-ide":   ["wide", "beside"],
        "-ake":   ["awake", "breaks"],
        "-est":   ["rests", "rest"],
        "-oam":   ["home", "alone"],
    }

    for key, words in families.items():
        present = [w for w in words if w in vocab]
        if len(present) >= 2:
            RHYME_GROUPS[key] = present


_build_rhyme_groups()

# Reverse lookup: word → rhyme group key
WORD_TO_RHYME: dict[str, str] = {}
for group_key, members in RHYME_GROUPS.items():
    for member in members:
        WORD_TO_RHYME[member] = group_key


def get_rhyme_group(word_text: str) -> str | None:
    return WORD_TO_RHYME.get(word_text.lower())


def find_rhyming_word(target_word: str, exclude: set[str] | None = None) -> str | None:
    """Find a word that rhymes with target_word."""
    group = get_rhyme_group(target_word)
    if not group:
        return None
    candidates = [
        w for w in RHYME_GROUPS[group]
        if w != target_word and (exclude is None or w not in exclude)
    ]
    return random.choice(candidates) if candidates else None


# ---------------------------------------------------------------------------
# Poem builder
# ---------------------------------------------------------------------------

def build_line_ending_with(end_word_text: str,
                           max_attempts: int = 300) -> list[Word] | None:
    """Build an iambic pentameter line that ends with a specific word."""
    # Find the Word object
    end_word = None
    for w in ALL_WORDS:
        if w.text.lower() == end_word_text.lower():
            end_word = w
            break
    if end_word is None:
        return None

    target = IAMBIC_PENTAMETER
    end_stress = end_word.stress
    if not target.endswith(end_stress):
        return None

    prefix_target = target[:-len(end_stress)]

    for _ in range(max_attempts):
        line = build_line(prefix_target)
        if line and stress_repr(line) == prefix_target:
            line.append(end_word)
            return line
    return None


@dataclass
class PoemConfig:
    title: str = ""
    stanza_count: int = 3
    lines_per_stanza: int = 4
    rhyme_scheme: str = "abab"  # or "aabb", "abba", "none"
    show_scansion: bool = False


def generate_poem(config: PoemConfig | None = None) -> str:
    """Generate a complete poem in iambic pentameter."""
    if config is None:
        config = PoemConfig()

    stanzas: list[list[str]] = []

    for _ in range(config.stanza_count):
        stanza_lines: list[str] = []
        stanza_scans: list[str] = []

        # Determine rhyme pairs based on scheme
        rhyme_map: dict[int, int] = {}  # line_index → line_index it rhymes with
        scheme = config.rhyme_scheme.lower()

        if scheme != "none" and len(scheme) >= config.lines_per_stanza:
            # Map letter → first line index with that letter
            letter_to_first: dict[str, int] = {}
            for i, ch in enumerate(scheme[:config.lines_per_stanza]):
                if ch in letter_to_first:
                    rhyme_map[i] = letter_to_first[ch]
                else:
                    letter_to_first[ch] = i

        # Track end words for rhyming
        end_words: dict[int, str] = {}
        used_end_words: set[str] = set()

        for line_idx in range(config.lines_per_stanza):
            line = None

            if line_idx in rhyme_map:
                # This line needs to rhyme with an earlier line
                partner_idx = rhyme_map[line_idx]
                partner_end = end_words.get(partner_idx)
                if partner_end:
                    rhyme_word = find_rhyming_word(partner_end, used_end_words)
                    if rhyme_word:
                        line = build_line_ending_with(rhyme_word)
                        if line:
                            end_words[line_idx] = rhyme_word
                            used_end_words.add(rhyme_word)

            if line is None:
                # Build a free line
                for _attempt in range(50):
                    line = build_line()
                    if line:
                        end_text = line[-1].text
                        if end_text not in used_end_words:
                            end_words[line_idx] = end_text
                            used_end_words.add(end_text)
                            break
                else:
                    line = build_line()

            if line:
                text = " ".join(w.text for w in line)
                # Capitalize first word
                text = text[0].upper() + text[1:]
                stanza_lines.append(text)
                if config.show_scansion:
                    stanza_scans.append(scan_line(line))

        stanzas.append(stanza_lines)
        if config.show_scansion:
            stanzas.append(stanza_scans)

    # Format output
    output_parts: list[str] = []
    if config.title:
        output_parts.append(f"    {config.title}")
        output_parts.append("")

    for i, stanza in enumerate(stanzas):
        for line_text in stanza:
            output_parts.append(line_text)
        if i < len(stanzas) - 1:
            output_parts.append("")

    return "\n".join(output_parts)


# ---------------------------------------------------------------------------
# Themed poem generation
# ---------------------------------------------------------------------------

THEMES = {
    "night": {
        "title": "Nocturne",
        "preferred_nouns": ["night", "moon", "star", "shadow", "dream",
                            "silence", "ghost", "shade", "dusk"],
        "preferred_adjs": ["dark", "pale", "silent", "silver", "deep",
                           "lonely", "cold", "distant", "serene"],
    },
    "nature": {
        "title": "Pastoral",
        "preferred_nouns": ["river", "forest", "mountain", "meadow", "tree",
                            "leaf", "flower", "stream", "field", "dawn"],
        "preferred_adjs": ["green", "golden", "wild", "gentle", "wide",
                           "vast", "bright", "warm", "fair"],
    },
    "time": {
        "title": "On Time",
        "preferred_nouns": ["time", "morning", "evening", "winter", "summer",
                            "dawn", "dusk", "spring", "memory", "dust"],
        "preferred_adjs": ["old", "young", "ancient", "eternal", "brief",
                           "slow", "forgotten", "weary", "distant"],
    },
    "love": {
        "title": "Sonnet",
        "preferred_nouns": ["heart", "soul", "fire", "flame", "rose",
                            "desire", "delight", "embrace", "breath", "grace"],
        "preferred_adjs": ["sweet", "tender", "warm", "gentle", "fair",
                           "divine", "true", "bold", "soft", "bright"],
    },
    "sea": {
        "title": "Maritime",
        "preferred_nouns": ["sea", "wave", "shore", "storm", "wind",
                            "ocean", "voyage", "cliff", "peak", "rain"],
        "preferred_adjs": ["vast", "deep", "wild", "fierce", "cold",
                           "bold", "immense", "grey", "dark", "wide"],
    },
}


def generate_themed_poem(theme: str = "night",
                         stanza_count: int = 3,
                         lines_per_stanza: int = 4,
                         rhyme_scheme: str = "abab",
                         show_scansion: bool = False) -> str:
    """Generate a themed poem. Themes: night, nature, time, love, sea."""
    theme_data = THEMES.get(theme, THEMES["night"])

    # Temporarily boost preferred words by duplicating them in the pool
    saved_pools: dict[str, list[Word]] = {}

    if "preferred_nouns" in theme_data:
        preferred = set(theme_data["preferred_nouns"])
        boosted = [w for w in WORDS_BY_POS["noun"] if w.text in preferred]
        saved_pools["noun"] = WORDS_BY_POS["noun"][:]
        WORDS_BY_POS["noun"] = WORDS_BY_POS["noun"] + boosted * 4

    if "preferred_adjs" in theme_data:
        preferred = set(theme_data["preferred_adjs"])
        boosted = [w for w in WORDS_BY_POS["adj"] if w.text in preferred]
        saved_pools["adj"] = WORDS_BY_POS["adj"][:]
        WORDS_BY_POS["adj"] = WORDS_BY_POS["adj"] + boosted * 4

    # Also rebuild stress index
    for stress_key in list(WORDS_BY_STRESS.keys()):
        WORDS_BY_STRESS[stress_key] = [
            w for w in ALL_WORDS
        ]
    # (We rely on POS pool, stress index isn't used in build_line directly)

    config = PoemConfig(
        title=theme_data["title"],
        stanza_count=stanza_count,
        lines_per_stanza=lines_per_stanza,
        rhyme_scheme=rhyme_scheme,
        show_scansion=show_scansion,
    )

    result = generate_poem(config)

    # Restore pools
    for pos_key, saved in saved_pools.items():
        WORDS_BY_POS[pos_key] = saved

    return result


# ---------------------------------------------------------------------------
# CLI interface
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate poems in iambic pentameter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Default: 3 stanzas, night theme
  %(prog)s --theme love --rhyme aabb # Love poem, couplet rhymes
  %(prog)s --theme sea --stanzas 4 --scansion  # With scansion marks
  %(prog)s --theme nature --lines 2 --rhyme aa  # Short couplet stanzas
        """
    )
    parser.add_argument("--theme", choices=list(THEMES.keys()),
                        default="night", help="Poem theme (default: night)")
    parser.add_argument("--stanzas", type=int, default=3,
                        help="Number of stanzas (default: 3)")
    parser.add_argument("--lines", type=int, default=4,
                        help="Lines per stanza (default: 4)")
    parser.add_argument("--rhyme", default="abab",
                        help="Rhyme scheme: abab, aabb, abba, none (default: abab)")
    parser.add_argument("--scansion", action="store_true",
                        help="Show scansion marks below each stanza")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducibility")
    parser.add_argument("--count", type=int, default=1,
                        help="Number of poems to generate")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    for i in range(args.count):
        if i > 0:
            print("\n" + "=" * 50 + "\n")

        poem = generate_themed_poem(
            theme=args.theme,
            stanza_count=args.stanzas,
            lines_per_stanza=args.lines,
            rhyme_scheme=args.rhyme,
            show_scansion=args.scansion,
        )
        print(poem)


if __name__ == "__main__":
    main()
