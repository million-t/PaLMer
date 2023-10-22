import os
import telebot
import google.generativeai as palm
from collections import defaultdict


BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
palm.configure(api_key=os.environ['PALM_API_KEY'])
# model = palm.get_model('chat-bison@001')
memo = defaultdict(list)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Howdy!')


@bot.message_handler(func=lambda msg: True)
def chat(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    last_name = message.from_user.last_name if message.from_user.last_name else ""

    try:
        
        context = f'You are a telegram bot named PaLMer. I am a telegram user. My first name is {first_name}, and my last name is {last_name}. My telegram username is @{username}.'
        memo[chat_id].append(message.text)
        
        response = palm.chat(messages=memo[chat_id] , context=context)
        last = response.last
        memo[chat_id].append(last) 
        bot.send_message(chat_id, last, parse_mode="Markdown")

        while len(memo[chat_id]) > 20:
            memo[chat_id].pop(0)
        
    except:
        bot.send_message(chat_id, ":(", parse_mode="Markdown")

bot.infinity_polling()