import sys,os
sys.path.insert(0,os.path.dirname('/Users/yanming/Desktop/git/FAQ/DrFAQ-master/'))
import pandas as pd
from match.similarity import Match



class FAQ:
    def __init__(self, excel_file):
        self.df = pd.read_csv(excel_file)
        print(len(self.df))
        self.match = Match()
        self.token_list = [ self.match.nlp(s) for s in self.df['Question']]

    def ask_faq(self, text, threshold=0.8):
        """Returns FAQ answer if similarity score exceeds threshold"""
        max_score = 0
        question_idx = 0
        
#        for i, q in enumerate(self.df['Question']):
#            print(i)
#            if i>750:
#                s = self.match.compare(text, q)
#                if s > max_score:
#                    max_score = s
#                    question_idx = i
        
        
        # self.token_list = [ self.match.nlp(s) for s in self.df['Question'] ]
        token_text = self.match.nlp(text)
       
        for i, q in enumerate(self.token_list):
            s = self.match.compare2(token_text,q)
            if s > max_score:
                max_score = s
                question_idx = i
                
        
        print("FAQ score:", max_score)
        if max_score > threshold:
            return self.df['Answer'][question_idx]
        else:
            return None


if __name__ == "__main__":
    faq = FAQ("../match/faq_covidbert.csv")
    answer = faq.ask_faq("What is Covid?")
    print(answer)
