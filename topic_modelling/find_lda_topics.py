import os
from pprint import pprint

from gensim.models import LdaModel

from definitions import ROOT_DIR

if __name__ == "__main__":
    lda_file_path = os.path.join(ROOT_DIR, "LDA_MODEL", "all_users_lda")
    all_users_lda_model = LdaModel.load(lda_file_path)
    topic_words = []
    for index, topic in all_users_lda_model.show_topics(formatted=True):
        topic_words.append(f'Topic: {index}\nWords: {topic}')
    with open(os.path.join(ROOT_DIR, "topic_modelling", "lda_topics.txt"), "w") as log_file:
        pprint(topic_words, log_file)
