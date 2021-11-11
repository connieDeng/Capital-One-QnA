import urllib.request  
import bs4 as BeautifulSoup
import nltk
import re
import gensim.downloader as api
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.models.word2vec import Word2Vec
from tabulate import tabulate

model_google_news = api.load("word2vec-google-news-300")

def returnBankParagraphs():

    model_glove_twitter.wv.most_similar("good",topn=10)
    print(model_google_news)

    # we are using capital one for now
    text = urllib.request.urlopen('https://www.capitalone.com/bank/savings-accounts/online-performance-savings-account/disclosures/')

    article = text.read()
    article_parsed = BeautifulSoup.BeautifulSoup(article,'html.parser')    

    paragraphs = article_parsed.find_all('p')

    article_paragraphs = []
    for p in paragraphs:  
        article_paragraphs.append(p.text.lower())

    return article_paragraphs

'''
changing 
- my --> your
- me --> you?
'''

'''
Closing an Account: You can close your account at any time, for any reason. We can close your account at any time, for any reason and without advance notice.
'''

def findCloseSubstrings(document, question):
    glove_vectors = gensim.downloader.load('glove-twitter-25')
    question_word = ["who", "what", "when", "where", "how", "why"]
    
    for word in word_tokenize(question.lower()):
        print(word)

    return 'end'
        


if __name__ == "__main__":
    document = returnBankParagraphs()
    question = "When can I close my account?"
    print(findCloseSubstrings(document,question))