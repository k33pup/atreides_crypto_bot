import pymongo
import os


class DbManager:
    def __init__(self):
        self.client = pymongo.MongoClient(
            f"mongodb+srv://admin:{os.environ['mongoPass']}@usersdata.xrdsw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        self.db = self.client.Users
        self.collection = self.db.Clients

    def da(self):
        pass


if __name__ == '__main__':
    db = DbManager()
    db.da()
