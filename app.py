from flask import Flask,request
from pymessenger.bot import Bot
import os
from dotenv import load_dotenv

load_dotenv()

Access_token = os.getenv('Access_token')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

app = Flask(__name__)
Access_token = Access_token
VERIFY_TOKEN = VERIFY_TOKEN
bot = Bot(Access_token)

input_messages=[]

# @app.route("/", methods=['GET', 'POST'])
# def index_page():
#     return "Healty"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'token is invalid'
    if request.method == 'POST':
        output = request.get_json()
        print(output)
        for event in output['entry']:
            message = event['messaging']
            for data in message:
                if data.get('message'):
                    recipient_id = data['sender']['id']
                    if data['message'].get('text'):
                        message_text = data['message']['text']
                        # input_messages.append(message_text)
                        print(message_text)
                        # print('sender_id: ',recipient_id,'with msg : ',message_text)
                        # bot.send_text_message(recipient_id, "how can i help you?")
                    elif data['message'].get('attachments'):
                        for att in data['message'].get('attachments'):
                            img_url = att['payload']['url']
                            print(img_url)
                            # bot.send_image_url(recipient_id,img_url)
                else:
                    pass
        return "ok", 200, {"Access-Control-Allow-Origin": "*"}
                
if __name__ == "__main__":
    app.run(port=5000, debug=True)