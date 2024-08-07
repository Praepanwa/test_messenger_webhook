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
base_url = "https://graph.facebook.com/v11.0/"
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


# @app.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == 'GET':
#         if request.args.get("hub.verify_token") == VERIFY_TOKEN:
#             return request.args.get("hub.challenge")
#         else:
#             return 'token is invalid'
#     if request.method == 'POST':
#         output = request.get_json()
#         print('-----input json object--------')
#         print(output)
#         saveobj(output)
#         for event in output['entry']:
#             message = event['messaging']
#             for data in message:
#                 if data.get('message'):
#                     recipient_id = data['sender']['id']
#                     if data['message'].get('text'):
#                         message_text = data['message']['text']
#                         # input_messages.append(message_text)
#                         print('-------message text--------')
#                         print(message_text)
#                         print('------------------------')
#                         print('sender_id: ',recipient_id,'with msg : ',message_text)
#                         # bot.send_text_message(recipient_id, "how can i help you?")
#                     elif data['message'].get('attachments'):
#                         for att in data['message'].get('attachments'):
#                             img_url = att['payload']['url']
#                             print('------------------------')
#                             print('customer_img_url : ', img_url)
#                             # bot.send_image_url(recipient_id, img_url)
#                 else:
#                     pass
#         return "ok", 200, {"Access-Control-Allow-Origin": "*"}


# get all conversation only for the first page returned

@app.route("/get-chat-history", methods=["GET"])
def getAllChatHistory():

    response = requests.get(base_url + message_uri, headers=headers)
    print(type(response.status_code))
    response_data = response.json()

    # create participants
    participants = response_data["conversations"]["data"]
    for participant in participants:

        next_page = participant["messages"]["paging"].get("next")

        while next_page:

            next_page_data = requests.get(next_page, headers=headers).json()
            next_page_messages = next_page_data["data"]

            for message in next_page_messages:
                participant["messages"]["data"].append(message)

            print("-------loading in process------")
            # print('link: ', link)
            # response = requests.get(link, headers=headers)
            # data = response.json()
            # paging_data.append(data['data'])
            if next_page_data["paging"].get("next") is not None:
                next_page = next_page_data["paging"]["next"]
            else:
                print("-------loading completed------")
                break
    return participants


# @app.route("/get-paging-link", methods=["GET"])
# # get the next page link
# def getLink():
#     response = requests.get(base_url + message_uri, headers=headers)
#     print(type(response.status_code))
#     data = response.json()
#     list_of_paging_links = []
#     # paging = data["conversations"]["data"][0]["messages"]["paging"]["next"]
#     for i, v in enumerate(data["conversations"]["data"]):

#         if data["conversations"]["data"][i]["messages"]["paging"].get("next"):
#             list_of_paging_links.append(v["messages"]["paging"]["next"])

#     return list_of_paging_links


# paging = "https://graph.facebook.com/v20.0/t_1185312385841189/messages?fields=id%2Cmessage%2Cattachments%7Bfile_url%7D%2Ccreated_time&limit=25&after=QVFIUjRUREpHS1BMRUpnMDQ1QTZA1RGFIMnhUT2ZAMWTVUZA0hKTGJqNFB1TE1kZAkZAkc0UxZAk1wVUhRR3J5Y0RKX2pvYlllLUl5U21kRGhKUjlYYjNLZAWZASblpMN0lHd1VXYlVKM21pZAGJKR2JKck1RWG1sTm1HNUZAqLTdpa2JfZAkNmWjdH"

# get context of the next page
# @app.route("/nextpagedata", methods=["GET"])
# def test_paging():
#     list_of_paging_links = getLink()
#     for i in list_of_paging_links:
#         print(i)
#         response = requests.get(i, headers=headers)
#         print(type(response.status_code))
#         data = response.json()
#         # print(data)
#         # context = data.data
#         # print(type(context))
#         # df = pd.read_json(data)
#         # for i in context[0:1]:
#         # print(i)
#         return data


# 1. start with the first page
# 2. check if there is a next page
# 3. if yes, get the next page
# def flatern_list(arr):
#     return [item for sublist in arr for item in sublist]


# def get_all_paging_context(list_of_paging_links):
#     print("list_of_paging_link : ", list_of_paging_links)
#     paging_data = []
#     for link in list_of_paging_links:
#         print("eiei : ", link)

#         # get data from link
#         data = requests.get(link, headers=headers).json()
#         # get until got the last page context
#         while data["paging"].get("next"):
#             print("-------loading in process------")
#             print("link: ", link)
#             response = requests.get(link, headers=headers)
#             data = response.json()
#             # paging_data.append(data['data'])
#             if data["paging"].get("next") is not None:
#                 link = data["paging"]["next"]
#             else:
#                 print("-------loading completed------")
#                 continue
#     # print(paging_data)
#     formated_data = flatern_list(paging_data)
#     return formated_data


# chats = get_all_paging_context(getLink())
# saveobj(chats)


# the way to get all data is 1. get the first page 2.get the next from get_all_paging_context() 3. save the data
# but the point is idk the way to concat the data from the participants and their next page together.
# there is no relate key or some sharing attributes.
all_chats = getAllChatHistory()
saveobj(all_chats)

if __name__ == "__main__":
    app.run(port=5000)
