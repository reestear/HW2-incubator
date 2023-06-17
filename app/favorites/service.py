from app.config import database

from ..favorites.repository.repository import FavoritesRepository


class Service:
    def __init__(self):
        self.repository = FavoritesRepository(database)


def get_service():
    return Service()
