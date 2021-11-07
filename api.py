
import urllib.request  
import bs4 as BeautifulSoup
import nltk
import re
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from flask import Flask,request,jsonify
from flask_cors import CORS

from bert import QA

app = Flask(__name__)
CORS(app)

model = QA("model")

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
    
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    stop_words = stopwords.words('english')
    stop_words += ["us", "account", "may", 'u']
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
    
    print("CUSTOM WEIGHTS", word_frequencies)
    return word_frequencies

def summarizedParagraph(document, custom_weights):
    tokens = word_tokenize(document)
    
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    stop_words = stopwords.words('english')
    stop_words += ["us", "account", "may", 'u']

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

    print("TOP WEIGHTED WORDS: ", list(sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True))[:10])

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency

    # tokenizes by sentence
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
    select_length = 1

    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)

    final_summary = [word for word in summary]
    summary = ' '.join(final_summary)
    
    return summary
    
@app.route("/predict",methods=['POST'])
def predict():
    bank = request.json["bank"]
    question = request.json["question"]
    
    document = selectBankDocument()
    custom_weights = generateWeights(question)
    summary_paragraph = summarizedParagraph(document, custom_weights)

    # return jsonify({
    #     "question": question,
    #     "custom_weights": custom_weights,
    #     "document": document[:60],
    #     "summary": summary_paragraph
    #     })

    try:
        out = model.predict(summary_paragraph, question)
        print("ANSWER", out['answer'])
        return jsonify({"result":out})
    except Exception as e:
        print(e)
        return jsonify({"result":"Model Failed"})

if __name__ == "__main__":
    app.run('0.0.0.0',port=8000)