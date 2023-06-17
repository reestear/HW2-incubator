# from typing import Optional

# import uuid
from typing import Any, Optional

from bson.objectid import ObjectId
from pymongo.database import Database


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any], coords: dict):
        # inserting user_id to the current data
        data["user_id"] = ObjectId(user_id)
        data["media"] = []
        data["comments"] = []
        data["location"] = {"latitude": coords["lat"], "longitude": coords["lng"]}
        new_data = self.database["reviews"].insert_one(data)
        return new_data.inserted_id

    def get_shanyrak_by_id(self, shanyrak_id: str) -> Optional[dict]:
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
        return shanyrak

    def get_review(self, offset, limit):
        review = self.database["reviews"].find({})
        total = self.database["reviews"].count_documents({})

        if offset is not None:
            review = review.skip(offset)
        if limit is not None:
            review = review.limit(limit)

        return {"total": total, "review": review}

    def approve_shanyrak_by_id(self, shanyrak_id: str):
        shanyrak = self.database["reviews"].find_one({"_id": ObjectId(shanyrak_id)})
        self.database["reviews"].delete_one({"_id": ObjectId(shanyrak_id)})
        self.database["shanyraks"].insert_one(shanyrak)

    def decline_shanyrak_by_id(self, shanyrak_id: str):
        self.database["reviews"].delete_one({"_id": ObjectId(shanyrak_id)})

    def filter_shanyraks(self, filtering: Any):
        query_filter = {}

        if filtering["type"] is not None:
            query_filter["type"] = filtering["type"]
        if filtering["room_count"] is not None:
            query_filter["room_count"] = filtering["room_count"]
        if filtering["price_from"] is not None:
            query_filter["price"] = {"$gte": filtering["price_from"]}
        if filtering["price_untill"] is not None:
            query_filter.setdefault("price", {})["$lte"] = filtering["price_untill"]
        if (
            filtering["longitude"] is not None
            and filtering["latitude"] is not None
            and filtering["radius"] is not None
        ):
            radius_converted_approximately = (
                filtering["radius"] * 3.2535313808
            )  # 6371 is the approximate radius of the Earth in kilometers

            query_filter["location"] = {
                "$geoWithin": {
                    "$centerSphere": [
                        [filtering["longitude"], filtering["latitude"]],
                        radius_converted_approximately,
                    ]
                }
            }

        total = self.database["shanyraks"].count_documents(query_filter)
        cursor = self.database["shanyraks"].find(query_filter).sort("created_at", -1)

        if filtering["offset"] is not None:
            cursor = cursor.skip(filtering["offset"])
        if filtering["limit"] is not None:
            cursor = cursor.limit(filtering["limit"])

        shanyraks = []
        for item in cursor:
            shanyraks.append(item)
        return {"total": total, "shanyraks": shanyraks}

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
