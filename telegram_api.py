# direct work with Telegram API
import const
import requests
import json


def query_to_bot():
    # queries to the Telegram Bot API
    # use this method to receive incoming updates
    url = const.URL.format(token=const.TOKEN, method=const.UPDATE_METH)
    content = requests.get(url)
    data = json.loads(content.text)
    # print(data)
    return parsing_data(data)


def parsing_data(inp_data):
    city = inp_data['result'][-1]['message']['text']
    print(city)
    return get_weather(city)


def get_weather(location):
    url = const.WEATHER_URL.format(city=location, token=const.WEATHER_TOKEN)
    response = requests.get(url)
    data = json.loads(response.content)
    return parsing_weather_data(data)


def parsing_weather_data(w_data):
    city = w_data['name']
    temp_c = round(w_data['main']['temp'] - 273.5, 2)
    print(f'It`s {temp_c} degrees Celsius in {city} now.')


if __name__ == '__main__':
    query_to_bot()
