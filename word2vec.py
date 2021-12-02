## for webscraping
import urllib.request  
import bs4 as BeautifulSoup
## for data
import json
import pandas as pd
import numpy as np
## for processing
import re
import nltk
## for word embedding
import gensim
import gensim.downloader as api
from scipy import spatial

from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
from word2vec_similarity import *
from bert import QA


app = Flask(__name__)
CORS(app, supports_credentials=True)

model = QA("model")

#  pretrained word2vec model; using wiki dataset; (experiment with different pretrained datasets)
glove_vectors = api.load("glove-wiki-gigaword-50")
nltk.download('stopwords')
nltk.download('wordnet')
lst_stopwords = nltk.corpus.stopwords.words("english")

# returns array of paragraphs
def get_bank_paragraphs(bank_link):
    text = urllib.request.urlopen(bank_link)
    article = text.read()
    article_parsed = BeautifulSoup.BeautifulSoup(article,'html.parser')    

    paragraphs = article_parsed.find_all('p')

    article_paragraphs = []
    for p in paragraphs:
      if len(p.text.split()) > 3:
        article_paragraphs.append(p.text)

    return article_paragraphs

'''
Preprocess a string.
:parameter
    :param text: string - name of column containing text
    :param lst_stopwords: list - list of stopwords to remove
    :param flg_stemm: bool - whether stemming is to be applied
    :param flg_lemm: bool - whether lemmitisation is to be applied
:return
    cleaned text
'''
def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
            
    ## Tokenize (convert from string to list)
    lst_text = text.split()
    # remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in lst_stopwords]
                
    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
                
    ## Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]
            
    ## back to string from list
    text = " ".join(lst_text)
    return text

def vec_representation(text):
  # print(text)
  vec = []
  tokens = text.split()

  for word in tokens:
    if word in glove_vectors:
      vec.append(glove_vectors[word])

  vec = np.mean(vec, axis = 0)
  return vec

def cos_similarity(list1, list2):
    return 1 - spatial.distance.cosine(list1, list2)

@app.route("/predict", methods=['POST'])
@cross_origin(supports_credentials=True)
def predict():
    bank_link = request.json["bank"]
    question = request.json["question"]

    print("QUESTION HERE:", question)

    question = [question]
    paragraphs = get_bank_paragraphs(bank_link)

    ## create df
    df = pd.DataFrame(question+paragraphs)
    ## rename columns
    df = df.rename(columns={0:"paragraph"})
    df["text_clean"] = df["paragraph"].apply(lambda x: utils_preprocess_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=lst_stopwords))
    df["vectorized"] = df["text_clean"].apply(lambda x: vec_representation(x))
    df["cos_sim"] = df['vectorized'][1:].apply(lambda x: cos_similarity(x,df['vectorized'][0]))

    possible_ans = df.nlargest(10, ["cos_sim"])
    data = list(possible_ans["paragraph"])
    print(data)
    return jsonify({"result": data})

if __name__ == "__main__":
    app.run('0.0.0.0',port=8000)
