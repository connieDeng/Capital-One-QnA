from tabulate import tabulate
import math
import urllib.request  
import bs4 as BeautifulSoup
import nltk
import re
import numpy as np
from string import punctuation
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer
from scipy import spatial

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer


# from sklearn.metrics.pairwise import cosine_similarity


# from flask import Flask,request,jsonify
# from flask_cors import CORS
# from word2vec_similarity import *
# from bert import QA


# app = Flask(__name__)
# CORS(app)

# model = QA("model")
    
'''
  CHECKLIST
    - question_content: gets the content of the question
      - removing of question words (who, what, where, where, why, how)

    - question_vec(question_content): word2vec representation of the question given by user

    - get_bank_paragraphs: gets the paragraphs of legal bank document using beautiful soup 
      - default Capital One
      - add a cleaning/filter function to filter out unwanted paragraphs (future implementation of def cleaning_paragraphs)
      - some paragraphs contains symbols
    
    - paragraph_vec: word2vec representation of paragraph

    - legal_bank_vec_dict: for each paragraph, create dictionary that pairs paragraph to their vectorized represntation

    - similar_question_and_paragraph: return matrix of [cos_similarity, paragraph]
'''
# URL is hardcoded right now, default capital one bank; change this later for other banks
# returns array of paragraphs
def get_bank_paragraphs():
    text = urllib.request.urlopen('https://www.capitalone.com/bank/savings-accounts/online-performance-savings-account/disclosures/')

    article = text.read()
    article_parsed = BeautifulSoup.BeautifulSoup(article,'html.parser')    

    paragraphs = article_parsed.find_all('p')

    article_paragraphs = []
    for p in paragraphs:  
        article_paragraphs.append(p.text.lower())

    return article_paragraphs

# vectorized representation of question
def question_vec(question):
  question_vec = []
  question_words = ["who", "what", "when", "where", "how", "why"]

  question = re.sub(r'[^\w\s]','',question).lower()
  tokens = question.split()

  for q in question_words:
    if q in tokens:
      tokens.remove(q)
      
  for word in tokens:
    question_vec.append(glove_vectors[word])

  question_vec = np.asarray(question_vec)
  question_vec_avg = np.mean(question_vec, axis = 0)

  return question_vec_avg


def custom_tokenizer(str_input):
    str_input = re.sub(r'[^\w\s]','',str_input).lower()
    tokens = str_input.split()
    return tokens

def tf_idf(sentences):
    l2_vectorizer = TfidfVectorizer(stop_words='english', tokenizer=custom_tokenizer, use_idf=True)
    X = l2_vectorizer.fit_transform(sentences)
    print(X)
    l2_df = pd.DataFrame(X.toarray(), columns=l2_vectorizer.get_feature_names_out())
    return l2_df

# @app.route("/predict",methods=['POST'])
# def predict():
#     bank = request.json["bank"]
#     question = request.json["question"]
    
#     paragraphs = get_bank_paragraphs()
    
#     question = "When can I close my account?"
#     question_vec_avg = question_vec(question)

#     # vector, paragraph
#     legal_bank_dict = legal_bank_vec_dict(paragraphs)

#     most_similar_paragraphs = top_ten_most_similar(similarilty_question_and_paragraph(question_vec_avg, legal_bank_dict))

#     # return jsonify({
#     #     "question": question,
#     #     "custom_weights": custom_weights,
#     #     "document": document[:60],
#     #     "summary": summary_paragraph
#     #     })

#     possible_ans = []
#     for p in most_similar_paragraphs:
#       # p is [similarity, paragraph]
#       out = model.predict(str(p[1]), question)
#       possible_ans.append(out["answer"])
    
#     return jsonify({"result": possible_ans })
          
    

if __name__ == "__main__":
    # app.run('0.0.0.0',port=8000)
    # print(len(get_bank_paragraphs()))
    # print(create_frequency_matrix(get_bank_paragraphs())
    question = ["When can I close my account?"]

    sentences = get_bank_paragraphs() + question
    tf_idf(sentences)
