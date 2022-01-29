import pymongo
import os
from datetime import datetime


class DbManager:
    def __init__(self):
        self.client = pymongo.MongoClient(
            f"mongodb+srv://admin:{os.environ['mongoPass']}@usersdata.xrdsw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        self.db = self.client.Users
        self.collection = self.db.Clients

    def add_user(self, user_id, licence, chat_id):
        post = {
            "_id": user_id,
            "license": licence,
            "time": datetime.now(),
            "chat_id": chat_id
        }
        self.collection.insert_one(post)
        print(f"Добавлен пользователь {user_id}")

    def get_all_chats_id(self, license_type):
        return [doc['chat_id'] for doc in self.collection.find({'license': license_type})]


if __name__ == '__main__':
    db = DbManager()
