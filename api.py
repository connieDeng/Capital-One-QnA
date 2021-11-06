import urllib.request  
import bs4 as BeautifulSoup
import nltk
import re
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
# from ghost import Ghost // Tried to use this to run script
# nltk.download('punkt')
# nltk.download("stopwords")

# from flask import Flask,request,jsonify
# from flask_cors import CORS

# from bert import QA

# app = Flask(__name__)
# CORS(app)

# model = QA("model")

# @app.route("/predict",methods=['POST'])

# return document of the correct bank
def selectBankDocument():
    # we are using capital one for now
    text = urllib.request.urlopen('https://www.capitalone.com/bank/savings-accounts/online-performance-savings-account/disclosures/')

    article = text.read()
    article_parsed = BeautifulSoup.BeautifulSoup(article,'html.parser')    

    paragraphs = article_parsed.find_all('p')

    article_content = ''
    for p in paragraphs:  
        article_content += p.text

    return article_content

# generate weights according to the question
def generateWeights(question):
    print("QUESTION:" , question)
    tokens = word_tokenize(question)
    stop_words = stopwords.words('english')
    word_frequencies = {}

    for word in tokens:
        # if re.match('/(\d+)/', word):
        #     print(word)
        if word.lower() not in stop_words:
            if word.lower() not in punctuation:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 100
                else:
                    word_frequencies[word] += 1
    
    return word_frequencies

# select paragraph which has the answer to the question
def summarizedParagraph(document, custom_weights):
    tokens = word_tokenize(document)
    stop_words = stopwords.words('english')
    stop_words += ["us", "account", "may"]

    word_frequencies = {}

    for word in tokens:
        if word.lower() not in stop_words:
            if word.lower() not in punctuation:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

    for word in custom_weights:
        if word in word_frequencies.keys():
            word_frequencies[word] += custom_weights[word]

    max_frequency = max(word_frequencies.values())

    print(list(sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True))[:10])

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency

    sent_token = sent_tokenize(document)
    
    sentence_scores = {}
    for sent in sent_token:
        sentence = sent.split(" ")
        for word in sentence:        
            if word.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.lower()]
    
    from heapq import nlargest
    # select_length = int(len(sent_token)*0.01)
    select_length = 2

    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)

    final_summary = [word for word in summary]
    summary = ' '.join(final_summary)
    
    return summary


def predict():
    # doc = request.json["document"]
    bank_chosen = request.json["bank"]
    question = request.json["question"]

    # question = "Do you charge fees for electronic fund transfer services?"
    document = selectBankDocument()
    custom_weights = generateWeights(question)
    print("CUSTOM WEIGHTS FOR THIS QUESTION: ", custom_weights)
    summarized_paragraph = summarizedParagraph(document, custom_weights)

    print("REQUESTION IS:", summarized_paragraph, question)

    try:
        out = model.predict(summarized_paragraph, question)
        return jsonify({"result":out})
    except Exception as e:
        print(e)
        return jsonify({"result":"Model Failed"})

if __name__ == "__main__":
    app.run('0.0.0.0',port=8000)
    # curl -X POST http://0.0.0.0:8000/predict -H 'Content-Type: application/json' -d '{ "bank": "doesnt matter", "question":"Do you charge fees for electronic fund transfer services?" }'
