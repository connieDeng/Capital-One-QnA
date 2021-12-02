from gensim.models.word2vec import Word2Vec
import gensim.downloader as api
from tabulate import tabulate
import urllib.request  
import bs4 as BeautifulSoup
import nltk
import re
import numpy as np
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity


from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
from word2vec_similarity import *
from bert import QA


app = Flask(__name__)
CORS(app, supports_credentials=True)

model = QA("model")
    
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

#  pretrained word2vec model; using wiki dataset; (experiment with different pretrained datasets)
glove_vectors = api.load("glove-wiki-gigaword-50")

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

# vectorized representation of paragraph
def paragraph_vec(sentence):
  vec = []

  sentence = re.sub(r'[^\w\s]','',sentence).lower()
  tokens = sentence.split()

  for word in tokens:
    if word in glove_vectors:
      vec.append(glove_vectors[word])

  vec = np.mean(vec, axis = 0)
  return vec

def legal_bank_vec_dict(paragraphs):
  legal_bank_dict = {}
  for p in paragraphs:
    legal_bank_dict[p] = paragraph_vec(p)
  return legal_bank_dict

def cos_similarity(list1, list2):
  return 1 - spatial.distance.cosine(list1, list2)

def similarilty_question_and_paragraph(question_vec, paragraphs_dict):
  cos_similarity_dict = []
  for p in paragraphs_dict.keys():
    similarity = cos_similarity(question_vec, paragraphs_dict[p])
    cos_similarity_dict.append([similarity, p])
  return cos_similarity_dict

def top_ten_most_similar(cos_similarity_dict):
  cos_similarity_dict.sort(reverse=True)
  return cos_similarity_dict[3:13]

@app.route("/predict",methods=['POST'])
@cross_origin(supports_credentials=True)
def predict():
    bank = request.json["bank"]
    question = request.json["question"]
    
    paragraphs = get_bank_paragraphs()
    
    question = "When can I close my account?"
    question_vec_avg = question_vec(question)

    # vector, paragraph
    legal_bank_dict = legal_bank_vec_dict(paragraphs)

    most_similar_paragraphs = top_ten_most_similar(similarilty_question_and_paragraph(question_vec_avg, legal_bank_dict))
    print(most_similar_paragraphs)
    # return jsonify({
    #     "question": question,
    #     "custom_weights": custom_weights,
    #     "document": document[:60],
    #     "summary": summary_paragraph
    #     })

    possible_ans = []
    for p in most_similar_paragraphs:
      # p is [similarity, paragraph]
      out = model.predict(str(p[1]), question)
      possible_ans.append(out["answer"])
    
    return jsonify({"result": possible_ans })

if __name__ == "__main__":
    app.run('0.0.0.0',port=8000)
