import pymongo
import json

mongdb_config_path = "scripts\\scripts_secrets.json"

# Allowed operations
# 1 - edit
# 2 - delete
operation = 1

filter_field = "tags"
set_field = "manually_assigned_tags"
set_value = True

filter = {"$and": [{filter_field: {"$ne": None}}, {filter_field: {"$ne": []}}]}

edit = {"$set": {set_field: set_value}}

delete = {"$unset": {set_field: ""}}

with open(mongdb_config_path, "r") as f:
    config = json.load(f)

mongo = pymongo.MongoClient(config.get("server"), config.get("port"))
collection = mongo[config.get("db")][config.get("collection")]

if operation == 1:
    operation = edit
    operation_name = "edit"
elif operation == 2:
    operation = delete
    operation_name = "delete"

num_of_dashes = 68
do_proceed = input(
    "-" * num_of_dashes
    + f"\nYou are going to {operation_name.upper()} documents in "
    + f"'{collection.name}' collection.\nType 'yes' if you are willing "
    + "to proceed and anything else to abort.\n"
)

if do_proceed == "yes":
    collection.update_many(filter, operation)
    print("Operation Succeeded.")

print("-" * num_of_dashes)
