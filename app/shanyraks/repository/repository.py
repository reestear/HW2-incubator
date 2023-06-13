# from typing import Optional

from typing import Any, Optional

from bson.objectid import ObjectId
from pymongo.database import Database


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        # inserting user_id to the current data
        data["user_id"] = ObjectId(user_id)
        new_data = self.database["shanyraks"].insert_one(data)
        return new_data.inserted_id

    def get_shanyrak_by_id(self, shanyrak_id: str) -> Optional[dict]:
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        return shanyrak

    def update_shanyrak_by_id(self, shanyrak_id: str, data: dict[str, Any]):
        self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={"$set": data},
        )

    def delete_shanyrak_by_id(self, shanyrak_id: str):
        self.database["shanyraks"].delete_one({"_id": ObjectId(shanyrak_id)})
