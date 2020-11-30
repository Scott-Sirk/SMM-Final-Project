
#analyize data for paper 2

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

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
        for full_path, sub_dirs, files in os.walk(self._file_locn):
            for file in files:
                answer = full_path.split('\\')[-1]
                with open(full_path + '\\' + file, 'r', encoding = 'utf-8') as f:
                    content = f.read()
                row = [answer, content, file]
                raw_data.append(row)
        return raw_data

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
        text_only = [item[1] for item in data]
        answers = [item[0] for item in data]
        tf_idf = TfidfVectorizer(ngram_range = (1, 3)
                                 , vocabulary = vocab
                                 , preprocessor = self.process_strings
                                 , tokenizer = nltk.word_tokenize
                                 )
        X = tf_idf.fit_transform(text_only)
        bow = X.toarray()
        return bow, answers, tf_idf.vocabulary_

    def create_model(self, X, y):
        model = SVC()
        #SVM has overtaken naive bayes
##        model = MultinomialNB()
        model.fit(X, y)
        return model

    def test_model(self, model, X, y):
        print(model.score(X, y))

    def use_model(self, model, X):
        predictions = model.predict(X)
        return predictions


def main():

    file_locn = r'C:\Users\Scott\Desktop\social_media_mining\SMM-Final-Project\train'

    obj = Twitter_ML(file_locn)
    data = obj.load_data()
    bow, answers, vocab = obj.data_to_vector(data)
    model = obj.create_model(bow, answers)
    #-----------------------------------------------#

    test_files = r'C:\Users\Scott\Desktop\social_media_mining\SMM-Final-Project\test'

    obj2 = Twitter_ML(test_files)
    data2 = obj2.load_data()
    bow2, answers2, vocab2 = obj2.data_to_vector(data2, vocab)

    obj2.test_model(model, bow2, answers2)

    #-----------------------------------------------#
    #create predictions and save the data

    real_files = r'C:\Users\Scott\Desktop\social_media_mining\SMM-Final-Project\real_data'
    obj3 = Twitter_ML(real_files)
    data3 = obj3.load_data()
    bow3, ans_unknown, vocab3 = obj3.data_to_vector(data3, vocab)

    predictions = obj3.use_model(model, bow3)

    print('here')

    df = pd.DataFrame(columns = ['account'
                                 , 'year'
                                 , 'month'
                                 , 'day'
                                 , 'hour'
                                 , 'minute'
                                 , 'second'
                                 , 'collection_period'
                                 , 'prediction'])
    for i, lst in enumerate(data3):
        date, source_file = lst[2].split('__')[:2]
        source, ext = source_file.split('.')
        year = date[:4]
        month = date[4:6]
        day = date[6:8]
        hour = date[8:10]
        minute = date[10:12]
        second = date[12:]
        predict = predictions[i]
        df = df.append({'account':source
                        , 'year':year
                        , 'month':month
                        , 'day':day
                        , 'hour':hour
                        , 'minute':minute
                        , 'second':second
                        , 'collection_period':year+month+day+hour
                        , 'prediction':predict}
                       , ignore_index = True)

    df = df.drop_duplicates()
    df.to_csv('final_paper_data.csv')



if __name__ == '__main__':
    main()
