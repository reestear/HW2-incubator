# from typing import Optional
from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database

from app.shanyraks.service import get_service

# from typing import Any, Optional


class CommentRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_comment(self, user_id: str, shanyrak_id: str, content: str):
        payload = {
            "content": content,
            "created_at": datetime.utcnow(),
            "author_id": user_id,
            "shanyrak_id": shanyrak_id,
        }
        last_comment = self.database["comments"].insert_one(payload)
        payload["_id"] = str(last_comment.inserted_id)

        svc = get_service()
        svc.repository.add_shanyrak_comment_by_id(shanyrak_id, payload)

    def update_comment(self, comment_id: str, content: str):
        comment = self.database["comments"].find_one({"_id": ObjectId(comment_id)})
        comment["content"] = content
        self.database["comments"].update_one(
            filter={"_id": ObjectId(comment_id)}, update={"$set": comment}
        )

    def get_comments(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})[
            "comments"
        ]

    # def get_shanyrak_by_id(self, shanyrak_id: str) -> Optional[dict]:
    #     shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
    #     return shanyrak

    # def update_shanyrak_by_id(self, shanyrak_id: str, data: dict[str, Any]):
    #     self.database["shanyraks"].update_one(
    #         filter={"_id": ObjectId(shanyrak_id)},
    #         update={"$set": data},
    #     )

    # def delete_shanyrak_by_id(self, shanyrak_id: str):
    #     self.database["shanyraks"].delete_one({"_id": ObjectId(shanyrak_id)})

    # def put_shanyrak_media_by_id(self, shanyrak_id: str, file_url: str):
    #     shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
    #     shanyrak["media"].append(file_url)

    #     self.database["shanyraks"].update_one(
    #         filter={"_id": ObjectId(shanyrak_id)},
    #         update={"$set": shanyrak},
    #     )

    # def delete_shanyrak_media_by_id(self, shanyrak_id: str):
    #     shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
    #     shanyrak["media"] = []

    #     self.database["shanyraks"].update_one(
    #         filter={"_id": ObjectId(shanyrak_id)},
    #         update={"$set": shanyrak},
    #     )
