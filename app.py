import dbAPI as db
from flask import Flask, request
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route("/", methods=["POST"])
def main(event, context):
    logging.info(request.json)
    #текст ответа, предпологается, что ответ будет в виде 'Расписание номер_группы дата'
    request_text = event['request']['original_utterance'].lower().split()[1::]
    text = db.fetchall("lesson", f"{request_text[0]};{request_text[1]}",["audience","teacher","start","end"])
    response = {
        'version': event['version'],
        'session': event['session'],
        "response":{
            "end_session":False,
            "text" : text,
        }
    }
    return json.dumps(response)