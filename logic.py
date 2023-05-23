import openai
import json
# Установите ваш API-ключ
openai.api_key = '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'


def send_chat_request(message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )

    if len(response.choices) > 0:
        return response.choices[0].text.strip()
    else:
        return "Получен пустой ответ от API."


# Пример запроса

user_message = 'у меня есть строка "432-3 24.05" . вытащи из неё номер группы и дату.'+'в виде {"group":"","date":""}'

response = send_chat_request(user_message)
response_json = json.loads(response)
print(response_json["group"],response_json["date"])