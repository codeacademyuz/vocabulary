from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from db import VocabularyDB

db = VocabularyDB('db.json')


def start(udpate: Update, context: CallbackContext):
    topics = db.get_topics()
    inline_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(topic, callback_data='topic:{}'.format(topic)) for topic in topics]])
    udpate.message.reply_html(
        text='Hello <b>{}</b>!\n\nselect a topic for vocabulary'.format(udpate.message.from_user.first_name),
        reply_markup=inline_keyboard)


def start_topic(udpate: Update, context: CallbackContext):
    query = udpate.callback_query
    topic = query.data.split(':')[1]

    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Words', callback_data=f'words:{topic}'),InlineKeyboardButton('start', callback_data=f'start:{topic}')],
    ])
    query.message.reply_html(
        text='Topic: <b>{}</b>\n\nselect an action'.format(topic),
        reply_markup=inline_keyboard
    )

def start_vocabulary(udpate: Update, context: CallbackContext):
    query = udpate.callback_query
    topic = query.data.split(':')[1]
    word = db.get_first(topic)

    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('◀️', callback_data=f'back:{topic}:{word.doc_id}'),InlineKeyboardButton('X', callback_data='X'), InlineKeyboardButton('▶️', callback_data=f'next:{topic}:{word.doc_id}')],
    ])
    query.message.reply_html(
        text='<b>{}</b>\n\ndefinition: <i>{}</i>'.format(word['word'], word['meaning']),
        reply_markup=inline_keyboard
    )


def next_word(udpate: Update, context: CallbackContext):
    query = udpate.callback_query
    topic, word_id = query.data.split(':')[1:]
    word = db.get_word(topic, int(word_id)+1)

    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('◀️', callback_data=f'back:{topic}:{word.doc_id}'),InlineKeyboardButton('X', callback_data='X'), InlineKeyboardButton('▶️', callback_data=f'next:{topic}:{word.doc_id}')],
    ])
    # edit message
    query.message.edit_text(
        text='<b>{}</b>\n\ndefinition: <i>{}</i>'.format(word['word'], word['meaning']),
        parse_mode='HTML',
        reply_markup=inline_keyboard
    )


def back_word(udpate: Update, context: CallbackContext):
    query = udpate.callback_query
    topic, word_id = query.data.split(':')[1:]
    word = db.get_word(topic, int(word_id)-1)

    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('◀️', callback_data=f'back:{topic}:{word.doc_id}'),InlineKeyboardButton('X', callback_data='X'), InlineKeyboardButton('▶️', callback_data=f'next:{topic}:{word.doc_id}')],
    ])
    query.message.edit_text(
        text='<b>{}</b>\n\ndefinition: <i>{}</i>'.format(word['word'], word['meaning']),
        parse_mode='HTML',
        reply_markup=inline_keyboard
    )


def close(udpate: Update, context: CallbackContext):
    query = udpate.callback_query
    query.message.delete()


def send_all_words_in_topic(update: Update, context: CallbackContext):
    topic = update.callback_query.data.split(":")[1]
    words = db.all_words(topic)
    
    text = f"<b>{topic}</b>\n\n"
    for i in range(len(words)):
        text += f"{i+1}. {words[i]['word']}\n"
    
    update.callback_query.message.reply_html(text=text)
