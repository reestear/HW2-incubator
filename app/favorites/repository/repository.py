# from typing import Optional

# import uuid
# from typing import Any, Optional

from bson.objectid import ObjectId
from pymongo.database import Database


class FavoritesRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_to_favorites(self, shanyrak_id: str, user_id: str):
        address = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})[
            "address"
        ]

        payload = {"shanyrak_id": shanyrak_id, "user_id": user_id, "address": address}
        self.database["favorites"].insert_one(payload)

    def get_favorites(self, user_id: str):
        return self.database["favorites"].find({"user_id": user_id})

    def delete_favorite(self, shanyrak_id: str, user_id: str):
        self.database["favorites"].delete_one(
            {"shanyrak_id": shanyrak_id, "user_id": user_id}
        )
