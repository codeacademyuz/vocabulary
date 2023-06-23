


def start_learning(update: Update, context: CallbackContext):
    # get user from update
    user = update.effective_user
    # get word from vdb
    word = vdb.get_random_word(user.id)
    if word is None:
        url = f'{URL}random-word/{user.id}/'
        response = requests.get(url)
        if response.status_code == 200:
            words = response.json()
            # add word to vdb
            vdb.add_words(user.id, words)
            # get word from vdb
            word = vdb.get_random_word(user.id)
            # get word image
            url = f'{URL}word/{word["id"]}/'
            update.message.reply_photo(
                photo=word['image'],
                caption=f'<b>Topic:</b> {word["topic"]}\n<b>Word:</b> {word["name"]}',
                parse_mode='HTML',
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text='👍'),
                            KeyboardButton(text='👎')
                        ]
                    ],
                    resize_keyboard=True
                )
            )
        else:
            update.message.reply_html(
                text=f'<b>Error</b>: {response.status_code}'
            )
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

