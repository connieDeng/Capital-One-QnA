from flask import Flask,request,jsonify
from flask_cors import CORS
from word2vec_similarity import *
from bert import QA


app = Flask(__name__)
CORS(app)

model = QA("model")
    
@app.route("/predict",methods=['POST'])
def predict():
    bank = request.json["bank"]
    question = request.json["question"]
    
    # document = return_bank_paragraphs()
    paragraphs = return_bank_paragraphs()
    
    question = "When can I close my account?"
    question_vec_avg = question_vec(question)

    # vector, paragraph
    legal_bank_dict = legal_bank_vec_dict(paragraphs)

    most_similar_paragraphs = similar_question_and_paragraph(question_vec_avg, legal_bank_dict)

    most_similar_paragraphs.sort(reverse=True)
    # print(most_similar_paragraphs[3:13])


    # custom_weights = generateWeights(question)
    # summary_paragraph = summarizedParagraph(document, custom_weights)

    # return jsonify({
    #     "question": question,
    #     "custom_weights": custom_weights,
    #     "document": document[:60],
    #     "summary": summary_paragraph
    #     })

    paragraph = str(most_similar_paragraphs[8][1])
    print(paragraph)
    
    try:
        out = model.predict(paragraph, question)
        # possible_ans.append(out)
        return jsonify({"result":out})
    except Exception as e:
        print(e)
        return jsonify({"result":"Model Failed"})

if __name__ == "__main__":
    app.run('0.0.0.0',port=8000)
