#imports
import os
import pandas as pd
import re
from unidecode import unidecode
import unicodedata


from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel, rpmodel, ldamulticore

from nltk.tokenize import sent_tokenize
import nltk 
import re
import string
from nltk.stem.snowball import FrenchStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize.texttiling import TextTilingTokenizer
from nltk.collocations import *
import unicodedata
from nltk.stem import WordNetLemmatizer



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