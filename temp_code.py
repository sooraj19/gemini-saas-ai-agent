import pymongo
import json

# MongoDB connection string
connection_string = "mongodb://localhost:27017/transaction"

# Database and collection names
DatabaseName = "transaction"
CollectionName = "expenses"

# Username
username = "user123"

#Establish connection
client = pymongo.MongoClient(connection_string)
db = client[DatabaseName]
collection = db[CollectionName]

# Find document for user
query = {"username": username}
doc = collection.find_one(query)

#Check if document exists
if doc:
    #Remove the _id field before converting to JSON string
    doc.pop('_id',None)
    jsonString = json.dumps(doc,indent=4)
    #Convert JSON String to python dictionary using json.loads()
    jsonData = json.loads(jsonString)
    print(json.dumps(jsonData,indent=4))
else:
    print(json.dumps({"message":"No document found for the given username"},indent=4)) 

# Close the connection
client.close()
