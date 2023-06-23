from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters,
)
from booster.callbacks import (
    start,
    add_word,
    start_learning,
    check_answer,
)
from settings import (
    TOKEN,
)


def main():
    # create updater
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo, add_word))
    dp.add_handler(MessageHandler(Filters.text('📚 Start learning'), start_learning))
    dp.add_handler(MessageHandler(Filters.text, check_answer))
    
    # start polling
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()