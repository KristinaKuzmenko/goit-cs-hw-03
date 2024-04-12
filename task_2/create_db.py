from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb://localhost:27017"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

db = client.test

try:
    db.cats.insert_many(
        [
            {
                "name": "Garfield",
                "age": 7,
                "features": ["big", "fat", "loud", "loves meow", "gray"],
            },
            {
                "name": "Martin",
                "age": 5,
                "features": ["small", "tiny", "loves milk", "gray"],
            },
            {
                "name": "Rex",
                "age": 3,
                "features": ["big", "tiny", "loves meow", "white"],
            },
            {
                "name": "Scooby",
                "age": 8,
                "features": ["big", "fat", "loves milk", "loves meow", "black"],
            },
            {
                "name": "Snoopy",
                "age": 12,
                "features": ["small", "tiny", "loves meow", "white"],
            },
        ]
    )
except Exception as e:
    print(e)
