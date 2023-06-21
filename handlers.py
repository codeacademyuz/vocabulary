from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from db import DB
import requests

db = DB()
URL = 'http://vocabboostapi.pythonanywhere.com/api/v1/'


def start(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # set config
    db.set_config(user.id)

    # add user to db
    url = f'{URL}student/'
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'chat_id': user.id
    }
    r = requests.post(url, json=data)
    if r.status_code == 201:
        text = f'Assalamu alaikum, <b>{user.first_name}</b>!\n\nWelcome to <b>Vocabulary Booster Bot</b>!\n\n'
    else:
        text = f'Assalamu alaikum again, <b>{user.first_name}</b>!\n\nWelcome to <b>Vocabulary Booster Bot</b>!\n\n'
    # send message
    update.message.reply_html(
        text=text
    )
    update.message.reply_html(
        text='Please, choose one of the options below:',
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


def add_word(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # check word name
    if update.message.caption is None:
        update.message.reply_html(
            text=f'<b>Error</b>: Please, enter word name with topic name in caption! \n\n(Example: <b>Topic:Word</b>)'
        )
        return 'add_word'
    # add word to db
    topic_word = update.message.caption.split(':')
    # check topic and word
    if len(topic_word) < 2:
        update.message.reply_html(
            text=f'<b>Error</b>: topic or word name is empty. Please, enter word name with topic name in caption! \n\n(Example: <b>Topic:Word</b>)'
        )
        return 'add_word'
    if len(topic_word) == 2:
        topic_name, word_name = topic_word
    elif len(topic_word) == 2:
        topic_name, word_name, definition = topic_word
        data['definition'] = definition.strip()
    else:
        update.message.reply_html(
            text=f'<b>Error</b>: Please, enter word name with topic name in caption! \n\n(Example: <b>Topic:Word</b>)'
        )
        return 'add_word'
    # add word to db
    url = f'{URL}word/'
    data = {
        'topic': topic_name.title().strip(),
        'name': word_name.capitalize().strip(),
        'image': update.message.photo[-1].file_id,
    }
    response = requests.post(url, json=data)
    print(response.status_code)
    if response.status_code == 201:
        update.message.reply_photo(
            photo=update.message.photo[-1].file_id,
            caption=f'Word <b>{word_name}</b> added to topic <b>{topic_name}</b>!',
            parse_mode='HTML',
        )
    else:
        update.message.reply_html(
            text=f'<b>Error</b>: <b>{topic_name}</b> topic not found or word <b>{word_name}</b> already exists!'
        )


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
    else:
        return 'error'
