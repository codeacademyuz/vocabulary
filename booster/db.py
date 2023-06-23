from tinydb import TinyDB, Query
from tinydb.table import Document
import random


class StudentDB:
    def __init__(self, chat_id):
        db = TinyDB(f'database/{chat_id}.json')
        self.vocavularies = db.table('vocabularies')
        self.config = db.table('config')

    def is_vocabulary(self, id):
        return self.vocavularies.contains(doc_id=id)

    def add(self, id, name, image, attempts, corrects, topic, definition=None):
        if self.is_vocabulary(id):
            return False
        else:
            doc = Document(
                value={
                    "name": name,
                    "image": image,
                    "definition": definition,
                    "attempts": attempts,
                    "corrects": corrects,
                    "topic": topic
                },
                doc_id=id
            )
            return self.vocavularies.insert(doc)

    def get(self, id):
        if self.is_vocabulary(id):
            return self.vocavularies.get(doc_id=id)
        else:
            return False

    def attempt(self, id, is_correct: bool = False) -> list[int]:
        if self.is_vocabulary(id):
            vocabulary = self.get(id)
            return self.vocavularies.update(
                fields={
                    "attempts": vocabulary['attempts'] + 1,
                    "corrects": vocabulary['corrects'] + is_correct,
                },
                doc_ids=[id]
            )
        return False

    def get_all(self):
        return self.vocavularies.all()

    def clear(self):
        self.vocavularies.truncate()
    
    def get_random_word(self):
        q = Query()
        vocabularies = self.get_all()
        
        news = []
        for v in vocabularies:
            if v['attempts'] == 0:
                news.append(v)
            elif v['corrects'] / v['attempts'] < 0.6 and v['corrects'] < 3:
                news.append(v)
        if news:
            word = random.choice(news)
            self.set_config(config='start_learning', word_id=word.doc_id)
            return word

        self.clear()
        return 

    def set_config(self, config, word_id=None):
        self.config.truncate()
        self.config.insert({'stage': config, 'word_id': word_id})
        
    def show(self):
        return self.config.all()[0]