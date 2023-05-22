import dbAPI as db
from flask import Flask, request, render_template
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route("/",methods=["POST"])
def main():
    logging.info(request.json)
    #текст ответа, предпологается, что ответ будет в виде 'Расписание номер_группы дата'
    request_text = request.json['request']['original_utterance'].lower().split()[1::]
    db_response = db.fetchall("lesson", f"{request_text[0]};{request_text[1]}",["audience","teacher","start","end"])
    text = ""
    for s in db_response:
        for i in s:
            text += f"{i} "
    response = {
        'version': request.json['version'],
        'session': request.json['session'],
        "response":{
            "end_session":False,
            "text" : text,
        }
    }
    return json.dumps(response)