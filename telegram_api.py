# work with Telegram API directly
import const
import requests
import json


def main():
    # queries to the Telegram Bot API
    # use this method to receive incoming updates
    url = const.URL.format(token=const.TOKEN, method=const.UPDATE_METH)
    content = requests.get(url)
    data = json.loads(content.text)
    # print(data)
    return parsing_data(data)


def parsing_data(inp_data):
    city = inp_data['result'][-1]['message']['text']
    return get_weather(city)


def get_weather(location):
    url = const.WEATHER_URL.format(city=location, token=const.WEATHER_TOKEN)
    response = requests.get(url)
    data = json.loads(response.content)
    return parsing_weather_data(data)


def parsing_weather_data(w_data):
    city = w_data['name']
    temp_c = round(w_data['main']['temp'] - 273.5, 2)
    answer = f'It`s {temp_c} degrees Celsius in {city} now.'
    print(answer)
    return answer_user_bot(answer)


def answer_user_bot(data):
    data = {
        'chat_id': const.MY_ID,
        'text': data
    }
    url = const.URL.format(
        token=const.TOKEN,
        method=const.SEND_METH
    )
    response = requests.post(url, data=data)


if __name__ == '__main__':
    main()
