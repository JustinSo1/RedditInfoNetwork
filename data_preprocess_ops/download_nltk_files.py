import nltk


def download_nltk_files():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('stopwords')
