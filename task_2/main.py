import argparse
from bson import ObjectId

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://localhost:27017"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

db = client.test

parser = argparse.ArgumentParser()
parser.add_argument("--action", help="[create, read, update, delete]")
parser.add_argument("--id", help="Id of the cat")
parser.add_argument("--name", help="Name of the cat")
parser.add_argument("--age", help="Age of the cat")
parser.add_argument("--features", nargs="+", help="Features of the cat")

args = vars(parser.parse_args())
action = args["action"]
pk = args["id"]
name = args["name"]
age = args["age"]
features = args["features"]


def read():
    """
    Read data from the 'cats' collection in the database by id or name. Read all data if no args.
    """
    if pk:
        try:
            print(db.cats.find_one({"_id": ObjectId(pk)}))
        except Exception as e:
            print(f"Error: {e}")
    elif name:
        print(db.cats.find_one({"name": name}))
    else:
        for cat in db.cats.find():
            print(cat)


def create():
    """
    Create a new record in the 'cats' collection of the database.
    """

    created = db.cats.insert_one({"name": name, "age": age, "features": features})
    print(created.inserted_id)


def update():
    """
    Update all fields of the cat by id or update age/features by name.
    """
    if pk:
        try:
            updated = db.cats.update_one(
                {"_id": ObjectId(pk)},
                {"$set": {"name": name, "age": age, "features": features}},
            )
            print(f"Updated: {updated.modified_count}")
        except Exception as e:
            print(f"Error: {e}")

    elif name and age:
        updated = db.cats.update_one({"name": name}, {"$set": {"age": age}})
        print(f"Updated: {updated.modified_count}")

    elif name and features:
        updated = db.cats.update_one({"name": name}, {"$set": {"features": features}})
        print(f"Updated: {updated.modified_count}")
    else:
        print("Id or name is required")


def delete():
    """
    Delete cat by id or name. Delete all if no args.
    """
    if pk:
        try:
            deleted = db.cats.delete_one({"_id": ObjectId(pk)})
            print(f"Deleted: {deleted.deleted_count}")
        except Exception as e:
            print(f"Error: {e}")

    elif name:
        deleted = db.cats.delete_one({"name": name})
        print(f"Deleted: {deleted.deleted_count}")

    else:
        db.cats.delete_many({})
        print("Deleted all")


if __name__ == "__main__":
    match action:
        case "read":
            read()
        case "create":
            create()
        case "update":
            update()
        case "delete":
            delete()
        case _:
            print("Unknown action")
