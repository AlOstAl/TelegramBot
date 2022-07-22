import telebot
from telebot import types
import const
import json
import requests
from datetime import datetime

bot = telebot.TeleBot(const.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # bot.reply_to(message, f'Hello, {message.from_user.first_name}!')
    bot.send_message(message.chat.id, f'Hello, *{message.from_user.first_name}*\!', parse_mode='MarkdownV2')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('My city')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Enter the name of the city or tup the button.', reply_markup=markup)


@bot.message_handler(content_types='text')
def answer_weather(message):
    city = message.json['text']
    if city == 'My city': city = const.MY_CITY
    print(city)
    now = datetime.now().strftime("%c")
    res = get_weather(city)
    output_text = f'Now: {now}\n' \
                  f'City: {city}\n' + res
    if res is not None:
        bot.send_message(message.chat.id, output_text)
    else:
        bot.reply_to(message, 'Enter the correct city name.')


def get_weather(location):
    url = const.WEATHER_URL.format(city=location, token=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        answer = parsing_weather_data(data)
    elif response.status_code == 404:
        answer = None
    return answer


def parsing_weather_data(w_data):
    city = w_data['name']
    temp_c = round(w_data['main']['temp'] - 273.5, 2)
    # ℉ =(K - 273.15) * 1.8000 + 32.00
    # temp_f = round((w_data['main']['temp'] - 273.5 * 1.8 + 32), 2)
    answer = f'\U0001F321 {temp_c} \u2103'
    print(answer)
    return answer


bot.infinity_polling()
