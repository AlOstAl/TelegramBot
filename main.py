# work with pyTelegramAPI


import telebot
import const
import json
import requests

bot = telebot.TeleBot(const.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Enter the name of the city")


@bot.message_handler(func=lambda message: True)
def answer_weather(message):
    city = message.json['text']
    weather = get_weather(city)
    bot.reply_to(message, weather)


def get_weather(location):
    url = const.WEATHER_URL.format(city=location, token=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        answer = parsing_weather_data(data)
    elif response.status_code == 404:
        answer = "Enter the correct city name"
    return answer


def parsing_weather_data(w_data):
    city = w_data['name']
    temp_c = round(w_data['main']['temp'] - 273.5, 2)
    answer = f'It`s {temp_c} degrees Celsius in {city} now.'
    print(answer)
    return answer


bot.infinity_polling()
