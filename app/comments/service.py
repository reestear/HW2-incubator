from app.config import database

from .repository.repository import CommentRepository


class Service:
    def __init__(self):
        self.repository = CommentRepository(database)


def get_service():
    return Service()
