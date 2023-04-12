import random

from .recommender import Recommender
from .contextual import Contextual
from .toppop import TopPop


class MyRecommender(Recommender):
    fully_listened_tracks = {}

    def __init__(self, tracks_redis, catalog):
        self.tracks_redis = tracks_redis
        self.catalog = catalog
        self.top = TopPop(tracks_redis, catalog.top_tracks[:50])
        self.contextual = Contextual(tracks_redis, catalog)

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        if prev_track_time > 0.95:
            self.fully_listened_tracks.setdefault(user, []).append(prev_track)

        if self.fully_listened_tracks.setdefault(user, []):
            prev_track = random.choice(self.fully_listened_tracks[user])
        else:
            return self.top.recommend_next(user, prev_track, prev_track_time)

        return self.contextual.recommend_next(user, prev_track, prev_track_time)