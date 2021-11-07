import urllib.request  
import bs4 as BeautifulSoup
import nltk
import re
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer

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

'''
changing 
- my --> your
- me --> you?
'''

def findSubstrings(document, question):
    stop_words = stopwords.words('english')
    tokens = word_tokenize(question)
    substring = []
    for token in tokens:
        if token.lower() not in stop_words:
            substring.append(token)

    print(substring)



if __name__ == "__main__":
    document = selectBankDocument()
    question = "When can I close my account?"
    print(findSubstrings(document,question))