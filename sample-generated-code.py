import json
import pymongo

# JSON data to be inserted
data = {"username": "user123", "entries": [{"income": "salary", "amount": 10000}, {"income": "stocks", "amount": 500}, {"income": "rental", "amount": 2000}]}

# MongoDB connection string
connection_string = "mongodb://localhost:27017/"

# Database and collection names
database_name = "transaction"
collection_name = "expenses"

# Establish connection
client = pymongo.MongoClient(connection_string)
database = client[database_name]
collection = database[collection_name]

# Insert the JSON data
result = collection.insert_one(data)

# Print the inserted ID
print(f"Inserted document ID: {result.inserted_id}")

# Close the connection
client.close()
