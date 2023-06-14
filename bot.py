from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import os
from handlers import start, start_vocabulary, next_word, back_word, close

TOKEN = os.environ.get('TOKEN')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(start_vocabulary, pattern='topic:'))
    dp.add_handler(CallbackQueryHandler(next_word, pattern='next:'))
    dp.add_handler(CallbackQueryHandler(back_word, pattern='back:'))
    dp.add_handler(CallbackQueryHandler(close, pattern='X'))
    

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()