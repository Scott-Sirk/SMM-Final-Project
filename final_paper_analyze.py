
#analyize data for paper 2

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import pandas as pd
import nltk
import os
import re

class Twitter_ML(object):

    def __init__(self, file_locn):
        self._file_locn = file_locn

    def load_data(self):
        raw_data = []
        df = pd.read_csv(self._file_locn)
        return df

    def process_strings(self, string):
        copy = string
        copy = copy.lower()
        #remove symbols
        copy = re.sub('[^a-z ]', ' ', copy)
        #string to tokens
        tokens = nltk.word_tokenize(copy)
        tokens = [word for word in tokens if word not in stopwords.words('english')]
        ss = SnowballStemmer('english')
        tokens = [ss.stem(word) for word in tokens]
        #rebuild string
        copy = ' '.join(tokens)

        return copy

    def data_to_vector(self, data, vocab = None):
        text_only = data['text']
        answers = data['sentiment']
        cv = CountVectorizer(ngram_range = (1, 3)
                                 , vocabulary = vocab
                                 , preprocessor = self.process_strings
                                 , tokenizer = nltk.word_tokenize
                                 , binary = True
                                 )
        X = cv.fit_transform(text_only)
        return X, answers, cv.vocabulary_

    def create_model(self, X, y):
        model = SGDClassifier(loss = 'log')
        model.fit(X, y)
        return model

    def test_model(self, model, X, y):
        print(model.score(X, y))

    def use_model(self, model, X):
        predictions = model.predict(X)
        return predictions


def main():

    train_file = r'data/states/train.csv'

    train_obj = Twitter_ML(train_file)
    train_data = train_obj.load_data()
    X_train, y_train, vocab = train_obj.data_to_vector(train_data)
    model = train_obj.create_model(X_train, y_train)

    #-----------------------------------------------#

    test_files = r'data/states/test.csv'

    test_obj = Twitter_ML(test_files)
    test_data = test_obj.load_data()
    X_test, y_test, vocab_test = test_obj.data_to_vector(test_data, vocab)
    test_obj.test_model(model, X_test, y_test)
    

    #-----------------------------------------------#

    real = r'data/states/new_mexico.csv'
    real_obj = Twitter_ML(real)
    real_data = real_obj.load_data()
    X, y, vocab_real = real_obj.data_to_vector(real_data, vocab)
    predictions = real_obj.use_model(model, X)

    df = pd.DataFrame()

    for idx, row in real_data.iterrows():

        row['sentiment'] = predictions[idx]
        df = df.append(row)

    df.to_csv(r'data/states/new_mexico_pred.csv')


if __name__ == '__main__':
    main()
