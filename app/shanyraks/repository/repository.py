# from typing import Optional

# import uuid
from typing import Any, Optional

from bson.objectid import ObjectId
from pymongo.database import Database


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        # inserting user_id to the current data
        data["user_id"] = ObjectId(user_id)
        data["media"] = []
        data["comments"] = []
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

    def put_shanyrak_media_by_id(self, shanyrak_id: str, file_url: str):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        shanyrak["media"].append(file_url)

        self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={"$set": shanyrak},
        )

    def delete_shanyrak_media_by_id(self, shanyrak_id: str, file_url: str):
        query = {"_id": ObjectId(shanyrak_id)}
        update = {"$pull": {"media": file_url}}

        self.database["shanyraks"].update_one(query, update)

        # shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        # shanyrak["media"] = []

        # self.database["shanyraks"].update_one(
        #     filter={"_id": ObjectId(shanyrak_id)},
        #     update={"$set": shanyrak},
        # )

    def add_shanyrak_comment_by_id(self, shanyrak_id: str, content: Any):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

        shanyrak["comments"].append(content)

        self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={"$set": shanyrak},
        )

    def update_shanyrak_comment_by_id(
        self, shanyrak_id: str, comment_id: str, content: Any
    ):
        query = {
            "_id": ObjectId(shanyrak_id),
            "comments": {"$elemMatch": {"_id": comment_id}},
        }

        update = {"$set": {"comments.$.content": content}}

        self.database["shanyraks"].update_one(query, update)

    def delete_shanyrak_comment_by_id(self, shanyrak_id: str, comment_id: str):
        query = {"_id": ObjectId(shanyrak_id)}
        update = {"$pull": {"comments": {"_id": comment_id}}}

        self.database["shanyraks"].update_one(query, update)
