from tinydb import TinyDB, Query
from tinydb.table import Document



class DB:
    def __init__(self):
        db = TinyDB('db.json', indent=4)
        self.config = db.table('config')

    def is_user(self, chat_id: str):
        return self.config.contains(doc_id=chat_id)

    def set_config(self, chat_id: str):
        if self.is_user(chat_id):
            self.reset_config(chat_id)
        else:
            doc = Document(value={'status': 'start', 'word': None, 'word_id': None}, doc_id=chat_id)
            return self.config.insert(doc)

    def reset_config(self, chat_id: str, status: str = None,  word: str = None, word_id: int = None):
        if self.is_user(chat_id):
            value = {}
            if status: value['status'] = status
            if word: value['word'] = word
            if word_id: value['word_id'] = word_id
            
            doc = Document(value=value, doc_id=chat_id)
            return self.config.update(doc, doc_ids=[chat_id])
        else:
            return None
    
    def show_config(self, chat_id: str):
        if self.is_user(chat_id):
            return self.config.get(doc_id=chat_id)
        else:
            return None