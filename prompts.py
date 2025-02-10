add_totals = '''
The following json "INPUTS_JSON"
has the schema "
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "username": {
      "type": "string"
    },
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "income": {
            "type": "string"
          },
          "amount": {
            "type": "number"
          }
        },
        "required": [
          "income",
          "amount"
        ]
      }
    }
  },
  "required": [
    "username",
    "entries"
  ]
}
"

and add all the amounts and provide the total amount back in json format
'''
write_to_mongo = '''
generate executable python code in ".py" with import json and format and encoding to store the json document "JSON_DOCUMENT" into mongodb with connectionstring as "mongodb://localhost:27017/transaction", database name as "transaction" and collection name as "expenses"
'''

get_from_mongo = '''
generate executable python code in ".py" with import json and format and encoding to deserialise the JSON from mongodb BSON format as response by creating python code to get from mongodb with connectionstring as "mongodb://localhost:27017/transaction", database name as "transaction" and collection name as "expenses" where username is "USERNAME"
'''
