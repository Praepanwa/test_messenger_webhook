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
message_uri = "me?fields=conversations{name,participants,messages{id,message,attachments{file_url},created_time}}"
# me?fields=conversations{participants,message_count,name,messages{id,attachments{file_url,id},message,created_time}}

@app.route("/", methods=['GET'])
def index_page():
    return "Healty"

@app.route("/self", methods=['GET'])
def self_check():
    response = requests.get(base_url+self_uri, headers=headers)
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
#                             print('customer_img_url : ',img_url)
#                             # bot.send_image_url(recipient_id,img_url)
#                 else:
#                     pass
#         return "ok", 200, {"Access-Control-Allow-Origin": "*"}


@app.route("/test", methods=["GET", "POST"])
def test():
    response = requests.get(base_url+message_uri, headers=headers)
    print(type(response.status_code))
    data = response.json()

    # context = data["conversations"]["data"]
    # print(type(context))
    # df = pd.read_json(data)
    # for i in context[0:1]:
    # print(i)
    return data


@app.route("/get-paging-link", methods=["GET"])
def getLink():
    response = requests.get(base_url+message_uri, headers=headers)
    print(type(response.status_code))
    data = response.json()
    list_of_paging_links = []
    # paging = data["conversations"]["data"][0]["messages"]["paging"]["next"]
    for i,v in enumerate(data["conversations"]["data"]):
        
        if  data["conversations"]["data"][i]["messages"]["paging"].get("next"):
            print("hihi")
            list_of_paging_links.append(data["conversations"]["data"][i]["messages"]["paging"]["next"])
    
    return list_of_paging_links

paging = "https://graph.facebook.com/v20.0/t_1185312385841189/messages?access_token=EAAOuQnJ2TEgBO50SZCKZAjK273bIacnZCwhFwpaMXtFXVsHvDIg0fmBnuVBVDUCFXZBrlWNv0ZC2kYqXnPeYvDHm7ZBFPsIA3p4xN3D1HJYkdJE3dw74EIEZBWzMsj5BRFUUOZA5zsJWdw84DZBbihZA2ETsLpiriOdo4ZCpJQ9cdl85ugkbmOGqPHmmlgAGibLkN8mEqZCugkUdRuhKkwsJYqIcGnZBb&pretty=0&fields=id%2Cmessage%2Cattachments%7Bfile_url%7D%2Ccreated_time&limit=25&after=QVFIUjRUREpHS1BMRUpnMDQ1QTZA1RGFIMnhUT2ZAMWTVUZA0hKTGJqNFB1TE1kZAkZAkc0UxZAk1wVUhRR3J5Y0RKX2pvYlllLUl5U21kRGhKUjlYYjNLZAWZASblpMN0lHd1VXYlVKM21pZAGJKR2JKck1RWG1sTm1HNUZAqLTdpa2JfZAkNmWjdH"


@app.route("/test-paging", methods=["GET"])
def test_paging():
    response = requests.get(paging, headers=headers)
    print(type(response.status_code))
    data = response.json()
    print(data)
    # context = data.data
    # print(type(context))
    # df = pd.read_json(data)
    # for i in context[0:1]:
    # print(i)
    return data

# 1. start with the first page
# 2. check if there is a next page
# 3. if yes, get the next page
def get_paging_data(list_of_paging_links):
    for link in list_of_paging_links:
        paging_data =[]
        data = requests.get(link, headers=headers).json()             
        while data['paging'].get("next"):
            print('-------loading in process------')
            print('link: ',link)
            response = requests.get(link, headers=headers)
            data = response.json()
            paging_data.append(data['data'])
            # link =  data['paging']['next'] 
            # print(data['paging'].get("next") is None)
            if data['paging'].get("next") is not None:
                link =  data['paging']['next']
            else : 
                print('-------loading completed------')
                break
    # print(paging_data)
    return paging_data

# get_paging_data(getLink())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
