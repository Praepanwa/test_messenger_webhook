import os
from flask import Flask, request
from pymessenger.bot import Bot
from dotenv import load_dotenv
from writefile import saveobj
import requests
import pandas as pd

# from requests.auth import
load_dotenv()

Access_token = os.getenv("Access_token")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

app = Flask(__name__)
Access_token = Access_token
VERIFY_TOKEN = VERIFY_TOKEN
bot = Bot(Access_token)

input_messages = []
headers = {"Authorization": "Bearer " + Access_token}
base_url = "https://graph.facebook.com/v20.0/"
self_uri = "me?fields=id,name"
message_uri = (
    "me?fields=conversations{participants,messages{id,message,created_time,from}}"
)


@app.route("/", methods=["GET"])
def index_page():
    return "Healty"


# return self data
@app.route("/self", methods=["GET"])
def self_check():
    response = requests.get(base_url + self_uri, headers=headers)
    response = response.json()
    return response


# @app.route("/getAll", methods=["GET"])
def getAllChats():
    current_page = 1
    response = requests.get(base_url + message_uri, headers=headers)
    first_page = response.json()
    results = []

    participants = first_page["conversations"]["data"]

    results = getParticipantFullMessages(participants)

    next_page = first_page["conversations"]["paging"].get("next")

    while next_page is not None:
        print("current_page : ", current_page)
        print("in while : ", next_page)
        next_page_fetch = requests.get(next_page, headers=headers).json()
        participants = next_page_fetch["data"]

        results.append(getParticipantFullMessages(participants))

        next_page = next_page_fetch["paging"].get("next")
        current_page = current_page + 1
    else:
        print("-------loading customer message completed------")

    saveobj(results)
    return results


def getParticipantFullMessages(participants):
    for participant in participants:
        current_message_page = 1
        print("current_message_page : ", current_message_page)
        print("participant : ", participant["participants"]["data"][0]["name"])
        next_message_page = participant["messages"]["paging"].get("next")
        while next_message_page:
            if current_message_page > 1:
                print("current_message_page : ", current_message_page)
            next_page_message_response = requests.get(
                next_message_page, headers=headers
            ).json()
            next_page_messages = next_page_message_response["data"]

            for message in next_page_messages:
                participant["messages"]["data"].append(message)

            if next_page_message_response["paging"].get("next") is not None:
                current_message_page = current_message_page + 1
                next_message_page = next_page_message_response["paging"]["next"]
            else:
                break
    return participants


getAllChats()

if __name__ == "__main__":
    app.run(port=5000)
