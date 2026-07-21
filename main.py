"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""
from src.recommender import load_songs, recommend_songs, recommend_songs_diverse, print_recommendations_table

def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.40,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.95,
            "likes_acoustic": False,
        },
        "Conflicted Mood": {
            "favorite_genre": "rock",
            "favorite_mood": "sad",
            "target_energy": 0.9,
            "likes_acoustic": True,
        },
    }

    for name, user_prefs in profiles.items():
        print(f"\n=== Profile: {name} ===")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print("\nTop recommendations:\n")
        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()

    # Try different scoring modes on the same profile
    test_profile = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }
    for mode in ["default", "genre_first", "mood_first", "energy_focused"]:
        print(f"\n=== Mode: {mode} ===")
        results = recommend_songs(test_profile, songs, k=3, mode=mode)
        for song, score, explanation in results:
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")

    # Diversity-aware recommendations
    print("\n=== Diversity-Aware Recommendations (High-Energy Pop) ===")
    diverse_results = recommend_songs_diverse(profiles["High-Energy Pop"], songs, k=5, diversity_penalty=1.0)
    for song, score, explanation in diverse_results:
        print(f"{song['title']} ({song['artist']}) - Score: {score:.2f}")
        print(f"Because: {explanation}")

    # Diversity test with a profile likely to surface repeat artists
    print("\n=== Diversity Penalty Test (Deep Intense Rock) ===")
    diverse_test = recommend_songs_diverse(profiles["Deep Intense Rock"], songs, k=5, diversity_penalty=1.0)
    for song, score, explanation in diverse_test:
        print(f"{song['title']} ({song['artist']}) - Score: {score:.2f}")
        print(f"Because: {explanation}")

    # Table view of the same diversity-aware results
    print("\n=== Diversity Penalty Test (Deep Intense Rock) — Table View ===")
    print_recommendations_table(diverse_test)


if __name__ == "__main__":
    main()