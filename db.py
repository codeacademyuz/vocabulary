from tinydb import TinyDB, Query
from tinydb.table import Document


class VocabularyDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = TinyDB(db_path, indent=4)

    def get_topics(self):
        return self.db.tables()

    def add(self, word, meaning, topic):
        topic = self.db.table(topic)
        # add word to topic
        return topic.insert({'word': word, 'meaning': meaning})
    
    def get_first(self, topic):
        topic = self.db.table(topic)
        return topic.all()[0]
    
    def get_word(self, topic, word_id):
        topic = self.db.table(topic)
        return topic.get(doc_id=word_id)
    
    def all_words(self, topic):
        topic = self.db.table(topic)
        return topic.all()
