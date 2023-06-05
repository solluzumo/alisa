import dbAPI as db
from flask import Flask, request
import json
import logging
import openai
import os
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_data_gpt(message):
    openai.api_key = os.getenv("GPT_API")
    now = datetime.now()

    ate_time_str = now.strftime("%d-%m-%Y")
    message_text = f'у меня есть строка "{message}" . представь данные о номере группы и дате в виде json файла, без кода, ты должен сам представить мне данные, например в '+'виде {"group":"201-3", "date":"02.12.2012"},' +f'по возможности слова "завтра", "послезавтра" и т.д преобразуй в конкретную дату, относительно этой даты "{ate_time_str}", то есть если сейчас 12 июня, то завтра это 13 июня и т.д, в дате в качестве разделителя используй точки'

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message_text,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )
    print(response.choices[0].text.strip())
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
                break
            except:
                response["response"]["text"] = "ChatGPT не в духе, попробуй снова"
                return json.dumps(response)

        try:  #пытаемся достать из базы данных расписание
            splited_response = response_gpt.split()
            db_response = [list(el) for el in db.fetchall("lesson", f"{splited_response[0]};{splited_response[1]}",
                                                          ["group_name","name", "audience", "start", "end"])]
            text = ""
            for el in range(len(db_response)):
                text += f"Расписание для {db_response[el][0]}\n" \
                        f"{db_response[el][1]}\n\t\t" \
                        f"Аудитория: {db_response[el][2]}\n\t\t" \
                        f"Время начала: {db_response[el][3]}\n\t\t" \
                        f"Время конца: {db_response[el][4]}\n-------------\n\n"
            response["response"]["text"] = text
        except:
            response["response"][
                "text"] = "Не удалось найти группу в базе данных.Проверь свой запрос, может там ошибка?"
    return json.dumps(response)
