import json
import time

file_name = 'msg_'+str(int(time.time()))

def saveobj(jsonobj):
    file_name = 'msg_'+str(int(time.time()))
    print(file_name)
    with open(f'./data/{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(jsonobj, f,ensure_ascii=False)