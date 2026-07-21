# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add 5 new attributes to the song dataset that weren't in the baseline data 
(popularity, release decade, detailed mood tags, explicit flag, vocal 
style), then update the CSV, the `Song` dataclass, `load_songs()`, and 
`score_song()` so the new attributes are actually usable in scoring — 
without breaking the existing tests.

**Prompts used:**

"Add 5 new attributes to my song dataset that aren't in the baseline data — 
suggest things like popularity, release decade, and detailed mood tags. 
Update the CSV, the Song dataclass, load_songs(), and score_song() so the 
new attributes are actually usable in scoring, without breaking existing 
tests."

**What did the agent generate or change?**

- Added 5 new columns to `data/songs.csv`: `popularity` (0-100), 
  `release_decade`, `detailed_mood_tag`, `explicit` (True/False), and 
  `vocal_style`.
- Updated the `Song` dataclass in `src/recommender.py` with the 5 new 
  fields, using default values so existing code that creates a `Song` 
  without them still works.
- Updated `load_songs()` to parse the new columns, converting `popularity` 
  to int and `explicit` to a real boolean.
- Updated `score_song()` with two new optional scoring rules: a 
  `detailed_mood_tag` match (+0.75) and a `min_popularity` threshold bonus 
  (+0.25), both using `.get()` so profiles without those keys still work.

**What did you verify or fix manually?**

- Ran `pytest tests/` after the changes to confirm the new default values 
  on `Song` didn't break the existing test fixtures.
- Manually checked the updated `songs.csv` to confirm `explicit` was only 
  `True` for the two songs I intended (City Pulse, Iron Veins).
- Verified `load_songs()` correctly converts `"True"`/`"False"` strings 
  into real Python booleans instead of leaving them as truthy strings.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Strategy pattern.

**How did AI help you brainstorm or implement it?**

I asked how to let a user switch between multiple ranking strategies 
(Genre-First, Mood-First, Energy-Focused) without duplicating the whole 
`recommend_songs()` function for each one. The suggestion was to keep 
`score_song()` as the default strategy, write a separate scoring function 
per strategy with the same `(user_prefs, song) -> (score, reasons)` 
signature, and store them in a dictionary (`SCORING_STRATEGIES`) mapping a 
mode name to its function. `recommend_songs()` then just looks up the right 
function by name instead of having different branches of if/else logic.

**How does the pattern appear in your final code?**

In `src/recommender.py`: `score_song`, `score_song_genre_first`, 
`score_song_mood_first`, and `score_song_energy_focused` are interchangeable 
strategy functions, all with the same signature. The `SCORING_STRATEGIES` 
dictionary maps mode names to these functions, and `recommend_songs(user_prefs, 
songs, k, mode)` selects the strategy at runtime with 
`SCORING_STRATEGIES.get(mode, score_song)` before scoring and ranking.

---

## Agentic Workflow (SF8) — Diversity Logic

**What task did you give the agent?**

Implement a diversity penalty that reduces a song's score if its artist is 
already present in the recommendations being built, so the top results 
don't get dominated by one artist.

**Prompts used:**

"Add a diversity-aware ranking function that penalizes a song's score if 
its artist already appears in the top results list being built. Keep the 
original scoring function untouched and build this as a separate function 
that wraps it."

**What did the agent generate or change?**

- Added `recommend_songs_diverse()` to `src/recommender.py`, which scores 
  and sorts songs the same way as `recommend_songs()`, but as it builds the 
  top-k list it tracks which artists have already been added and subtracts 
  a configurable `diversity_penalty` (default 1.0) if a song's artist is a 
  repeat.
- Updated `main.py` to call the new function on the "Deep Intense Rock" 
  profile, which has two songs from the same artist (Fract Union), to make 
  the penalty visible in testing.

**What did you verify or fix manually?**

- Ran the diversity test against "Deep Intense Rock" and confirmed "Iron 
  Veins" (Fract Union) got penalized -1.00 because "Warehouse Riot" (also 
  Fract Union) already appeared earlier in the same list — visible directly 
  in the printed "reasons" explanation.
- Confirmed the list is re-sorted after applying penalties, so a penalized 
  song can drop below songs it originally outscored.