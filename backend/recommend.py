import numpy as np

from supabase_client import supabase


def euclidean_distance(
    user_valence,
    user_arousal,
    song_valence,
    song_arousal
):
    return np.sqrt(
        (user_valence - song_valence) ** 2 +
        (user_arousal - song_arousal) ** 2
    )


def recommend_music(
    user_valence,
    user_arousal,
    top_n=10
):

    response = (
        supabase
        .table("music")
        .select("*")
        .execute()
    )

    songs = response.data

    for song in songs:

        song_valence = float(
            song["valence"]
        )

        song_arousal = float(
            song["arousal"]
        )

        song["distance"] = float(
            euclidean_distance(
                user_valence,
                user_arousal,
                song_valence,
                song_arousal
            )
        )

    recommendations = sorted(
        songs,
        key=lambda x: x["distance"]
    )[:top_n]

    return recommendations