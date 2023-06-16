from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from db import DB
import requests

db = DB()
URL = 'http://127.0.0.1:8000/api/v1/'

def add_word(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # add word to db
    topic_name, word_name = update.message.caption.split(':')
    url = f'{URL}words/'
    data = {
        'topic': topic_name,
        'name': word_name,
        'image': update.message.photo[-1].file_id,
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        update.message.reply_html(
            text=f'Word <b>{word_name}</b> added to <b>{topic_name}</b>!'
        )
    else:
        update.message.reply_html(
            text=f'Error: {response.json()}'
        )
    return 'add_word'

def start(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # set config
    db.set_config(user.id)

    # add user to db
    url = f'{URL}students/'
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'chat_id': user.id
    }
    requests.post(url, json=data)

    # send message
    update.message.reply_html(
        text=f'Assalamu alaikum, <b>{user.first_name}</b>!\n\nWelcome to <b>Vocabulary Booster Bot</b>!\n\n',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='📚 Start learning'),
                    KeyboardButton(text='📝 My words')
                ],
                [
                    KeyboardButton(text='📊 Statistics'),
                    KeyboardButton(text='👨‍💻 About')
                ]
            ],
            resize_keyboard=True
        )
    )
    return 'start'

def start_learning(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # get word from db
    url = f'{URL}get_random_word/{int(user.id)}/'
    response = requests.get(url)
    if response.status_code == 200:
        word = response.json()
        # set config
        db.reset_config(chat_id=user.id, word=word['name'], word_id=word['id'])
        # send word photo
        update.message.reply_photo(
            photo=word['image'],
            caption=f'<b>What is this?</b>',
            parse_mode='HTML',
        )
        return 'learning'
    else:
        return 'error'

def check_answer(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # show config
    config = db.show_config(user.id)
    # get answer
    answer = update.message.text
    # check answer
    url = f'{URL}check_answer/{int(user.id)}/{config["word_id"]}/{answer}/'
    response = requests.get(url)
    if response.status_code == 200:
        word = response.json()
        if word['is_correct']:
            # send message
            update.message.reply_html(
                text=f'<b>🎉 Correct!</b>'
            )
        else:
            # send message
            update.message.reply_html(
                text=f'🙄 Wrong!\n\nCorrect answer: <b>{word["name"]}</b>'
            )
        # start learning
        return start_learning(update, context)