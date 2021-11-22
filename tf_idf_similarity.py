# from gensim.models.word2vec import Word2Vec
# import gensim.downloader as api
from tabulate import tabulate
import math
import urllib.request  
import bs4 as BeautifulSoup
import nltk
import re
import numpy as np
from string import punctuation
from nltk.corpus import stopwords

from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.stem import WordNetLemmatizer
from scipy import spatial
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

#  pretrained word2vec model; using wiki dataset; (experiment with different pretrained datasets)
# glove_vectors = api.load("glove-wiki-gigaword-50")

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

def _create_frequency_matrix(sentences):
  frequency_matrix = {}
  stopWords = set(stopwords.words("english"))
  ps = PorterStemmer()

  for sent in sentences:
      freq_table = {}
      words = word_tokenize(sent)
      for word in words:
          word = word.lower()
          word = ps.stem(word)
          if word in stopWords:
              continue

          if word in freq_table:
              freq_table[word] += 1
          else:
              freq_table[word] = 1

      frequency_matrix[sent[:15]] = freq_table

  return frequency_matrix

def _create_tf_matrix(freq_matrix):
  tf_matrix = {}

  for sent, f_table in freq_matrix.items():
      tf_table = {}

      count_words_in_sentence = len(f_table)
      for word, count in f_table.items():
          tf_table[word] = count / (count_words_in_sentence + 1)

      tf_matrix[sent] = tf_table

  return tf_matrix

def _create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table

def _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix

def _create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix

def _score_sentences(tf_idf_matrix) -> dict:
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        sentenceValue[sent] = total_score_per_sentence / (count_words_in_sentence + 1)

    return sentenceValue
  
def _find_average_score(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original summary_text
    average = (sumValues / len(sentenceValue))

    return average

def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:15] in sentenceValue and sentenceValue[sentence[:15]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary
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
  sentences = get_bank_paragraphs()
  # 2 Create the Frequency matrix of the words in each sentence.
  freq_matrix = _create_frequency_matrix(get_bank_paragraphs())
  #print(freq_matrix)

  # 3 Calculate TermFrequency and generate a matrix
  tf_matrix = _create_tf_matrix(freq_matrix)
  #print(tf_matrix)

  # 4 creating table for documents per words
  count_doc_per_words = _create_documents_per_words(freq_matrix)
  #print(count_doc_per_words)

  total_documents = len(get_bank_paragraphs())

  '''
  Inverse document frequency (IDF) is how unique or rare a word is.
  '''
  # 5 Calculate IDF and generate a matrix
  idf_matrix = _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
  #print(idf_matrix)

  # 6 Calculate TF-IDF and generate a matrix
  tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)
  #print(tf_idf_matrix)

  # 7 Important Algorithm: score the sentences
  sentence_scores = _score_sentences(tf_idf_matrix)
  #print(sentence_scores)

  # 8 Find the threshold
  threshold = _find_average_score(sentence_scores)
  #print(threshold)

  # 9 Important Algorithm: Generate the summary
  summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)
  print(summary)
    