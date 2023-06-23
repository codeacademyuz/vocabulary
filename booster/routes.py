from booster import app
from telegram.ext import (
    Dispatcher, 
    CommandHandler, 
    MessageHandler, 
    Filters,
)
from telegram import Bot, Update
from booster.callbacks import (
    start,
    add_word,
    start_learning,
    check_answer,
)
from settings import (
    TOKEN,
)
from flask import request

bot = Bot(TOKEN)

@app.route('/webhook/', methods=['POST'])
def main():
    dp = Dispatcher(bot, None, workers=0)

    update = Update.de_json(request.get_json(), bot)

    # add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo, add_word))
    dp.add_handler(MessageHandler(Filters.text('📚 Start learning'), start_learning))
    dp.add_handler(MessageHandler(Filters.text, check_answer))
    
    dp.process_update(update)

    return 'ok'


@app.route('/set')
def setting():
    url = 'https://vocabbosterbot.pythonanywhere.com/webhook/'
    return str(bot.set_webhook(url))
    