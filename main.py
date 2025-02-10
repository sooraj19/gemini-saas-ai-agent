import json
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from prompts import add_totals, write_to_mongo, get_from_mongo
from tracker_gemini_ai import execute_gemini_prompt, generate_and_execute_code
from pydantic.json import pydantic_encoder
from fastapi import Response

class Entry(BaseModel):
    income: str
    amount: int
class Income(BaseModel):
    username: str
    entries: List[Entry]


app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.post("/incomes/")
async def incomes(incomes: Income):
    print("Request start...")
    process_input_prompt = add_totals

    # update prompt with input json and get the totals
    process_input_prompt = process_input_prompt.replace("INPUTS_JSON", json.dumps(incomes, default=pydantic_encoder))
    json_response = Response(content=execute_gemini_prompt(process_input_prompt), media_type="application/json")

    # update and generate the prompt to write to mongodb
    write_to_db_prompt = write_to_mongo.replace("JSON_DOCUMENT", json.dumps(incomes, default=pydantic_encoder))

    # generate and execute python code
    generate_and_execute_code(write_to_db_prompt)

    # finally, return the json response back to the client
    return json_response


@app.get("/income/{username}")
async def get_expenses(username: str):
    get_from_db_prompt = get_from_mongo
    get_from_db_prompt = get_from_db_prompt.replace("USERNAME", username)

    # generate and execute python code
    code_execution_output = generate_and_execute_code(get_from_db_prompt)

    # return response to client
    return Response(content=code_execution_output, media_type="application/json")
