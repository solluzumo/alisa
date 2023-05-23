import dbAPI as db
from flask import Flask, request
import json
import logging
import openai
import os
openai.api_key = os.getenv("GPT_API")
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_data_gpt(message):
    message_text = f'у меня есть строка "{message}" . вытащи из неё номер группы и дату.Никаких лишних слов, ' \
                   f'чистые данные'+'в json формате {"group":"","date":""}'
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message_text,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )

    if len(response.choices) > 0:
        return response.choices[0].text.strip()
    else:
        return False

@app.route("/",methods=["POST"])
def main():
    logging.info(request.json)

    req = request.json
    response = {
        'version': req['version'],
        'session': req['session'],
        "response":{
            "end_session":False,
        }
    }
    hooker = 5
    #Если диалог новый, то мы приветствуем пользователя
    if req['session']['new']:
        response["response"]["text"] = "Привет, чтобы получить расписание, скажи мне номер группы и дату!"
    else:
        while hooker>0:
            #получаем из ответа пользователя нужные данные используя chat gpt
            request_text = get_data_gpt(req['request']['original_utterance'])
            #преобразуем данные в строку
            try:
                response_json = json.loads(request_text)
                response_gpt = f"{response_json['group']} {response_json['date']}"
                hooker -=1
            except:
                print(f"Bad format:{request_text}")

        try:  #пытаемся достать из базы данных расписание
            db_response = db.fetchall("lesson", f"{response_gpt[0]};{response_gpt[1]}",
                                      ["audience", "teacher", "start", "end"])
            text = ""
            for s in db_response:
                for i in s:
                    text += f"{i} "
            response["response"]["text"] = text
        except:
            response["response"][
                "text"] = "Не удалось найти группу в базе данных.Проверь свой запрос, может там ошибка?"
    return json.dumps(response)