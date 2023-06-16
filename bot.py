from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from handlers import (
    add_word,
    start,
    start_learning,
    check_answer,
)

TOKEN = os.environ.get('TOKEN')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.photo, add_word))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text('📚 Start learning'), start_learning))
    dp.add_handler(MessageHandler(Filters.text, check_answer))
    

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()