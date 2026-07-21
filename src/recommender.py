from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass

class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 0
    release_decade: str = ""
    detailed_mood_tag: str = ""
    explicit: bool = False
    vocal_style: str = ""

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: "lofi"
    favorite_mood: 'chill'
    target_energy: '0.40'
    likes_acoustic: 'True'

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv and returns a list of song dictionaries with numeric fields converted."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "popularity": int(row["popularity"]),
                "release_decade": row["release_decade"],
                "detailed_mood_tag": row["detailed_mood_tag"],
                "explicit": row["explicit"].strip().lower() == "true",
                "vocal_style": row["vocal_style"],
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences and returns (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"Genre match: {song['genre']}")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"Mood match: {song['mood']}")

    energy_similarity = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_similarity
    reasons.append(f"Energy similarity: {energy_similarity:.2f}")

    if user_prefs["likes_acoustic"] and song["acousticness"] > 0.5:
        score += 0.5
        reasons.append("Acoustic bonus (user likes acoustic)")
    elif not user_prefs["likes_acoustic"] and song["acousticness"] <= 0.5:
        score += 0.5
        reasons.append("Non-acoustic bonus (user prefers non-acoustic)")

    preferred_tag = user_prefs.get("preferred_mood_tag")
    if preferred_tag and song.get("detailed_mood_tag") == preferred_tag:
        score += 0.75
        reasons.append(f"Detailed mood tag match: {preferred_tag}")

    min_pop = user_prefs.get("min_popularity")
    if min_pop is not None and song.get("popularity", 0) >= min_pop:
        score += 0.25
        reasons.append(f"Popularity bonus: {song.get('popularity')} >= {min_pop}")

    return score, reasons


def score_song_genre_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song with genre weighted most heavily (Genre-First strategy)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 4.0
        reasons.append(f"Genre match (weighted heavily): {song['genre']}")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 0.5
        reasons.append(f"Mood match: {song['mood']}")

    energy_similarity = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_similarity * 0.5
    reasons.append(f"Energy similarity: {energy_similarity:.2f}")

    return score, reasons


def score_song_mood_first(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song with mood weighted most heavily (Mood-First strategy)."""
    score = 0.0
    reasons = []

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 3.0
        reasons.append(f"Mood match (weighted heavily): {song['mood']}")

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 1.0
        reasons.append(f"Genre match: {song['genre']}")

    energy_similarity = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_similarity * 0.5
    reasons.append(f"Energy similarity: {energy_similarity:.2f}")

    return score, reasons


def score_song_energy_focused(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song with energy closeness weighted most heavily (Energy-Focused strategy)."""
    score = 0.0
    reasons = []

    energy_similarity = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_similarity * 3.0
    reasons.append(f"Energy similarity (weighted heavily): {energy_similarity:.2f}")

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 1.0
        reasons.append(f"Genre match: {song['genre']}")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 0.5
        reasons.append(f"Mood match: {song['mood']}")

    return score, reasons


# Strategy registry: maps mode name to its scoring function
SCORING_STRATEGIES = {
    "default": score_song,
    "genre_first": score_song_genre_first,
    "mood_first": score_song_mood_first,
    "energy_focused": score_song_energy_focused,
}

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "default") -> List[Tuple[Dict, float, str]]:
    """Scores every song using the selected strategy, sorts by score descending, and returns the top k recommendations."""
    scoring_function = SCORING_STRATEGIES.get(mode, score_song)

    scored = []
    for song in songs:
        score, reasons = scoring_function(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]

def recommend_songs_diverse(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "default", diversity_penalty: float = 1.0) -> List[Tuple[Dict, float, str]]:
    """Scores and ranks songs like recommend_songs, but penalizes repeat artists to increase diversity in the top k."""
    scoring_function = SCORING_STRATEGIES.get(mode, score_song)

    scored = []
    for song in songs:
        score, reasons = scoring_function(user_prefs, song)
        scored.append([song, score, reasons])

    scored.sort(key=lambda x: x[1], reverse=True)

    results = []
    seen_artists = set()
    for song, score, reasons in scored:
        if len(results) >= k:
            break
        adjusted_score = score
        adjusted_reasons = list(reasons)
        if song["artist"] in seen_artists:
            adjusted_score -= diversity_penalty
            adjusted_reasons.append(f"Diversity penalty: -{diversity_penalty:.2f} (artist already in list)")

        seen_artists.add(song["artist"])
        explanation = "; ".join(adjusted_reasons)
        results.append((song, adjusted_score, explanation))




    # re-sort after penalty in case it changed the order
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def print_recommendations_table(recommendations: List[Tuple[Dict, float, str]]) -> None:
    """Prints a formatted table of recommendations with title, artist, score, and reasons."""
    from tabulate import tabulate

    table_rows = []
    for song, score, explanation in recommendations:
        table_rows.append([
            song["title"],
            song["artist"],
            f"{score:.2f}",
            explanation,
        ])

    headers = ["Title", "Artist", "Score", "Reasons"]
    print(tabulate(table_rows, headers=headers, tablefmt="grid", maxcolwidths=[20, 15, 8, 50]))