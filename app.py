from crypt import methods
from os import stat
from flask import Flask, current_app, render_template, request
import pickle
from entity.sms_spam_classifier import SMSSPAMClassifier
import sys  
import nltk
sys.path.insert(0, '../SMSSpamClassifier/entity/')


nltk.download('stopwords')



app = Flask(__name__)


    
def load_classifier() -> SMSSPAMClassifier:
    sms_classifier = None
    with open('model/smsspamclassifer.pkl','rb') as picker_reader:
        sms_classifier = pickle.load(picker_reader)
    return sms_classifier


model = load_classifier()

@app.route("/smschecker", methods=['GET','POST'])
def index():
    message_status = None
    if request.method == "POST":
        message_status = "Ham"
        status = model.predict(request.form.get('review_msg'))
        
        if status[0] == 1:
            message_status = "Spam"

        #eturn status

    return render_template('index.html',message_status=message_status)



if __name__ == "__main__":
    app.run(debug=True)