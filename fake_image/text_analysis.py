import nltk
import os
import pandas as pd
import csv
import numpy as np
import codecs
import re
import collections
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn.feature_extraction import DictVectorizer
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from collections import Counter
from nltk.tokenize import punkt
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import feature_extraction
from sklearn import preprocessing
from sklearn.externals import joblib
from unidecode import unidecode
import unicodedata

from nltk.tokenize import sent_tokenize
import string
from nltk.stem.snowball import FrenchStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize.texttiling import TextTilingTokenizer
import unicodedata
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer


import logging
import numpy as np
from optparse import OptionParser


from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.pipeline import Pipeline
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.cross_validation import train_test_split
import xgboost as xgb



def word_stemmer(mots):
    snowball = SnowballStemmer('english') # for english use Porter stem algo
    preprocessed_docs = []
    for mot in mots:
        preprocessed_docs.append(snowball.stem(mot))   
    return preprocessed_docs

def word_lemmatizer(mots): 
    lemmat = WordNetLemmatizer()
    preprocessed_docs = []
    for mot in mots:
        preprocessed_docs.append(lemmat.lemmatize(mot))   
    return preprocessed_docs 


def clean_text(txt):
    e=str(txt)
    e=unicode(e,'utf-8')
    e=unicodedata.normalize('NFKD', e).encode('ascii', 'ignore')
    e=re.sub("[^a-zA-Z]", " ", e)
    return e

def chunk_mot(phrases):
    """split text to a set of words : bag-of-words"""
    mots = nltk.word_tokenize(phrases) 
    return mots 

def no_punctuation(mots):
    """return the set of words without puntctuation marks """
    regex =  re.compile('[%s]' % re.escape(string.punctuation))
    mots_no_punctuation = []
    for token in mots: 
        new_token = regex.sub(u'', token)
        if not new_token == u'':
            mots_no_punctuation.append(new_token.lower()) #lower pour normaliser le texte
    return mots_no_punctuation

def delete_stop_words(mots):
    """return the set of words without insignifiant words like : le , de, ces, the... 
    """
    stops= set(stopwords.words('french')+stopwords.words('english'))
    mots_no_stopwords = []
    for mot in mots:
        if not mot in stops:
                mots_no_stopwords.append(mot)
    return mots_no_stopwords


    
def nettoyer_texte(text, lemma = False, Stemm = False ): 
    text_chunk = chunk_mot(text)
    text_punct = no_punctuation(text_chunk)
    text_f = delete_stop_words(text_punct)
    #if lemma == True :
        #text_f = word_lemmatizer(text_f)
    #if Stemm == True : 
        #text_f = word_stemmer(text_f)
    #reconstruct the text
    textn = ' '.join(text_f)
    return textn

#----------------------------------#
df = pd.read_csv("data/fake2.csv",sep="|",encoding="latin1")
all_news = pd.read_csv("data/fake1.csv",sep="|",encoding="latin1")

tokenize = lambda doc: doc.split(" ")
sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize) 
tfidf_title = sklearn_tfidf.fit_transform(list(all_news['title']) + list(df["message"]))

#----------------------------------#
#load models

sklearn_tfidf = joblib.load('data/vectorizer.pkl')
le = joblib.load('data/label_encoder.pkl')
ch2 = joblib.load('data/ch2.pkl')
bst = xgb.Booster({'nthread':6}) #init model
bst.load_model("data/title2.model")

#predict function
def pred(test):
    #test is a string
    test = sklearn_tfidf.transform([test])
    test = ch2.transform(test)
    xg_test = xgb.DMatrix(test)
    pred_prob = bst_.predict(xg_test).reshape(test.shape[0], 8)
    pred_label = np.argmax(pred_prob, axis=1)
    return(le.inverse_transform(pred_label)[0])