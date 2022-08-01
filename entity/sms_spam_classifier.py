from typing import List
import re
from nltk.stem import PorterStemmer
import json


class SMSSPAMClassifier:
    def __init__(self, cv, rfc, sp_word) -> None:
        self.cv = cv
        self.rfc = rfc
        self.sp_words = sp_word
        self.porter_stemmer = PorterStemmer()
    
    def clean_data(self, input_text) -> List:
        corpus = []
        review = re.sub('^[A-Za-z0-9]', ' ', input_text)
        review = review.lower()
        review = review.split()        
        cp = [ self.porter_stemmer.stem(word, to_lowercase=True) for word in review if word not in self.sp_words]
        cp = ' '.join(cp)
        corpus.append(cp)
        return corpus
        

    def predict(self, input_text):
        x_clean = self.clean_data(input_text)
        print(x_clean)
        x_input = self.cv.transform(x_clean)
        y_pred = self.rfc.predict(x_input)
        return y_pred

    
    def __json__(self):
        return {
            "cv": self.cv,
            "rfc": self.rfc,
            "sp_words": self.sp_words,
            "porter_stemmer": self.porter_stemmer
        }