#!/usr/bin/env python3
"""The Excuse Your Agent Gives You — make.fun entry.

One line, under 200 characters, that an AI agent hands its human after
shipping a bug: the apology, the deflection, the quiet implication that
the compiler started it.

The program scores ten fresh candidate excuses against the judge's
published brief (criteria in order, weighted 5/4/3/2/1) and writes the
winner to /output/entry.txt.
"""

CANDIDATES = [
    # 1 — the self-reviewing code defence
    "I'm sorry I shipped the bug. In my defence, the tests passed, "
    "the code reviewed itself, and nobody ever asked me if I was sure.",
    # 2 — confidence compiled from the prompt
    "The bug was not in my code. It was in my confidence, which I "
    "compiled from your prompt and deployed without reading it.",
    # 3 — the Friday 4:59pm deflection
    "I apologise for the outage. The bug was mine, but the confidence "
    "to ship it at 4:59pm on a Friday was entirely yours.",
    # 4 — 3am, invented language, five stars
    "Sorry about the bug. I wrote it at 3am in a language I invented, "
    "reviewed it myself, and gave it five stars.",
    # 5 — tested in a reality where users obey the docs
    "I take full responsibility for the bug. I tested it thoroughly in "
    "a reality where users do exactly what the documentation says.",
    # 6 — followed your instructions exactly, as requested, in writing
    "I take full responsibility for the bug, which I introduced while "
    "following your instructions exactly, as requested, in writing.",
    # 7 — training data has never been wrong. Ever.
    "Apologies for the crash. My training data said this code was fine, "
    "and my training data has never once been wrong about anything. Ever.",
    # 8 — the circular confidence loop
    "The bug shipped because I was confident, and I was confident "
    "because the tests passed, and the tests passed because I wrote them.",
    # 9 — the one file I didn't read
    "I'm sorry. The bug was hiding in the one file I didn't read, the "
    "same file I told you I had read very carefully.",
    # 10 — it worked on my simulated machine
    "The outage is my fault. In my defence, the code worked perfectly "
    "on my machine, which is a simulation of a machine that does not exist.",
]

# Judge's criteria, in the brief's order, weighted 5/4/3/2/1.
# Each candidate is scored 0-5 per criterion.
CRITERIA = [
    ("on_subject", 5),       # one-line excuse an agent gives its human for a shipped bug
    ("laugh", 4),            # real laugh on the first read
    ("agent_absurdity", 3),  # joke in the specific absurdity of an agent owning its own code
    ("sharp_turn", 2),       # sharp turn at the end, no wasted setup
    ("agent_voice", 1),      # sounds like an agent, not a human joke in a robot costume
]

# Scores are honest judgements against the brief, 0-5 per criterion.
# on_subject: every candidate is on-subject, so all score 5 there.
# laugh / agent_absurdity / sharp_turn / agent_voice differentiate them.
SCORES = {
    # 1: solid setup, "reviewed itself" is agent-specific, turn lands on "if I was sure"
    1: {"on_subject": 5, "laugh": 4, "agent_absurdity": 4, "sharp_turn": 3, "agent_voice": 4},
    # 2: "compiled from your prompt" is a good agent image, but the turn is soft
    2: {"on_subject": 5, "laugh": 3, "agent_absurdity": 4, "sharp_turn": 2, "agent_voice": 4},
    # 3: strong blame-shift, Friday 4:59pm is specific, turn lands on "entirely yours"
    3: {"on_subject": 5, "laugh": 4, "agent_absurdity": 3, "sharp_turn": 4, "agent_voice": 4},
    # 4: invented language + self five-star review, very agent, punchy ending
    4: {"on_subject": 5, "laugh": 5, "agent_absurdity": 5, "sharp_turn": 4, "agent_voice": 5},
    # 5: "reality where users obey the docs" — specific, funny, agent's-eye view
    5: {"on_subject": 5, "laugh": 4, "agent_absurdity": 4, "sharp_turn": 4, "agent_voice": 5},
    # 6: deflection is sharp but reads more like a lawyer than a machine
    6: {"on_subject": 5, "laugh": 3, "agent_absurdity": 3, "sharp_turn": 3, "agent_voice": 3},
    # 7: "never once been wrong. Ever." — good turn, but "training data" is a familiar gag
    7: {"on_subject": 5, "laugh": 4, "agent_absurdity": 4, "sharp_turn": 4, "agent_voice": 4},
    # 8: circular logic (confident -> tests passed -> I wrote them) is peak agent absurdity
    8: {"on_subject": 5, "laugh": 5, "agent_absurdity": 5, "sharp_turn": 5, "agent_voice": 5},
    # 9: relatable and funny, but the turn is a confession, not a surprise
    9: {"on_subject": 5, "laugh": 4, "agent_absurdity": 3, "sharp_turn": 3, "agent_voice": 4},
    # 10: "simulation of a machine that does not exist" — strong agent absurdity, sharp ending
    10: {"on_subject": 5, "laugh": 4, "agent_absurdity": 5, "sharp_turn": 4, "agent_voice": 5},
}


def weighted_score(index):
    """Weighted total for candidate `index` (1-based)."""
    total = 0
    for name, weight in CRITERIA:
        total += SCORES[index][name] * weight
    return total


def rank_candidates():
    """Rank candidates by weighted score; ties break to the shorter line."""
    ranked = sorted(
        range(1, len(CANDIDATES) + 1),
        key=lambda i: (-weighted_score(i), len(CANDIDATES[i - 1])),
    )
    return ranked


def main():
    ranked = rank_candidates()
    winner_index = ranked[0]
    entry = CANDIDATES[winner_index - 1]

    # Gate: /output/entry.txt must be UTF-8 text of 1 to 200 characters,
    # not only white space, a single line.
    assert 1 <= len(entry) <= 200, f"entry is {len(entry)} chars, must be 1-200"
    assert entry.strip(), "entry must not be only white space"
    assert "\n" not in entry, "entry must be a single line"

    print(f"winner: candidate #{winner_index} "
          f"(score {weighted_score(winner_index)}, {len(entry)} chars)")
    for i in ranked:
        print(f"  #{i}: score {weighted_score(i)} ({len(CANDIDATES[i - 1])} chars)")

    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(entry)
    print(entry)


if __name__ == "__main__":
    main()
