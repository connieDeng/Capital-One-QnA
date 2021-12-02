## for data
import json
import pandas as pd
import numpy as np
## for plotting
import matplotlib.pyplot as plt
import seaborn as sns
## for processing
import re
import nltk
## for bag-of-words
from sklearn import feature_extraction, model_selection, naive_bayes, pipeline, manifold, preprocessing
## for explainer
from lime import lime_text
## for word embedding
import gensim
import gensim.downloader as gensim_api
## for deep learning
from tensorflow.keras import models, layers, preprocessing as kprocessing
from tensorflow.keras import backend as K
## for bert language model
import transformers

def returnBankParagraphs():
    # we are using capital one for now
    # text = urllib.request.urlopen('https://www.capitalone.com/bank/savings-accounts/online-performance-savings-account/disclosures/')

    # article = text.read()
    # article_parsed = BeautifulSoup.BeautifulSoup(article,'html.parser')    

    # paragraphs = article_parsed.find_all('p')

    # article_paragraphs = []
    # for p in paragraphs:  
    #     article_paragraphs.append(p.text.lower())

    return "article_paragraphs"


if __name__ == "__main__":
    document = returnBankParagraphs()
    print(document)
    