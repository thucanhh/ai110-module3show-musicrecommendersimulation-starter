# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name
**VibeMatch 1.0**

## 2. Goal / Task
This recommender suggests songs a user might like based on four things they 
tell it about their taste: favorite genre, favorite mood, a target energy 
level, and whether they like acoustic music. It ranks every song in the 
catalog and shows the top 5 matches.

## 3. Data Used
The catalog has 18 songs (10 starter songs + 8 I added). Each song has: 
genre, mood, energy, tempo, valence, danceability, and acousticness. 
Genres range from pop and rock to lofi, jazz, metal, and folk. Limits: most 
genre/mood combinations only appear once or twice, so there isn't much 
variety within any single taste profile, and there's no data on song 
popularity, artist variety, or listening history.

## 4. Algorithm Summary
Every song gets points added up: 2 points if the genre matches what the 
user said they like, 1 point if the mood matches, up to 1 point based on 
how close the song's energy is to the user's target energy (closer = more 
points, not just "higher energy"), and half a point if the song's acoustic 
level matches whether the user said they like acoustic music. All songs get 
scored this way, then they're sorted highest to lowest, and the top 5 are 
shown with a plain-language reason for each.

## 5. Observed Behavior / Biases
Genre matches dominate the results. In one test, a song scored highest 
purely because its genre matched, even though the user's mood preference 
("sad") didn't match that song at all — the system doesn't notice when a 
user's own preferences contradict each other, it just adds up whatever 
points are available. Because genre is worth 2x more than mood and roughly 
2x the max energy score, mood ends up being the weakest signal in the whole 
system even though it's often what people mean when they describe a "vibe."

## 6. Evaluation Process
I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and 
a deliberately contradictory "Conflicted Mood" profile (rock + sad mood + 
high energy + likes acoustic). I also ran one experiment removing the 
energy score entirely, which caused several songs to tie at the same score 
— showing that energy is actually doing most of the work to tell similar 
songs apart, not mood.

## 7. Intended Use and Non-Intended Use
**Intended use:** classroom exploration of how content-based recommenders 
work, and demonstrating how scoring weights shape which songs get suggested.
**Not intended for:** real-world music recommendations. The catalog is too 
small, preferences are typed in manually instead of learned from behavior, 
and the system has no way to detect when someone's stated preferences 
contradict each other.

## 8. Ideas for Improvement
- Let related genres (like "pop" and "indie pop") get partial credit 
  instead of zero, instead of requiring an exact match.
- Rebalance the weights so mood can't be completely overridden by genre 
  and energy alone.
- Add more songs per genre/mood combination so the top 5 actually has 
  variety to choose from, instead of near-identical options.

---

## 9. Personal Reflection

My biggest learning moment was realizing that a "wrong-feeling" 
recommendation isn't necessarily a bug — every point "Storm Runner" earned 
in the Conflicted Mood test was awarded correctly by the rules I wrote, yet 
the result still felt off, because the math can't tell the difference 
between "some things match" and "this actually fits the vibe." That 
reframed how I think about real apps like Spotify: a recommendation I don't 
like might just be a weighting choice working exactly as intended, not a 
mistake.

Using AI tools helped me move fast on the scoring formula and catch edge 
cases I wouldn't have thought to test myself, like the conflicting-mood 
profile. I had to double-check it most when it suggested code that changed 
behavior silently — like when removing one scoring term caused several 
songs to tie, which wasn't obvious until I actually ran it and compared 
outputs, not just read the code.

What surprised me most is how much a simple weighted-points system can 
"feel" like a real recommendation, even though there's no learning or 
personalization happening at all — it's just arithmetic run against a 
spreadsheet. If I extended this project, I'd want to try letting the 
system learn weights from user feedback (like skips or likes) instead of 
me hardcoding the genre/mood/energy weights by hand.