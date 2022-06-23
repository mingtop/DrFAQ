import sys, os

sys.path.insert(0, os.path.dirname('/Users/yanming/Desktop/git/FAQ/DrFAQ-master/'))
import pandas as pd
from match.similarity import Match


class FAQ:
    def __init__(self, excel_file):
        self.df = pd.read_csv(excel_file)
        print(len(self.df))
        self.match = Match()
        self.token_list = [self.match.nlp(s) for s in self.df['Question']]

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
        temp = []
        for i, q in enumerate(self.token_list):
            s = self.match.compare2(token_text, q)
            temp.append((q, i, s))
            if s > max_score:
                max_score = s
                question_idx = i
        if max_score > threshold:
            return self.df['Answer'][question_idx]
        else:
            return None

    def get_ranks(self, text, threshold=0.8):
        """Returns FAQ answer if similarity score exceeds threshold"""
        max_score = 0
        question_idx = 0

        token_text = self.match.nlp(text)
        temp = []
        for i, q in enumerate(self.token_list):
            s = self.match.compare2(token_text, q)
            if s > threshold:
                temp.append((i, s))
            if s > max_score:
                max_score = s
                
                question_idx = i
        rank = sorted(temp, key=lambda i: i[-1], reverse=True)
        # print(rank[:3], "FAQ score:", max_score)
        if max_score > threshold:
            return rank
        else:
            return None


if __name__ == "__main__":
    faq = FAQ("../chat/trainDataFinal.csv")
    answer = faq.ask_faq("What is Covid?")
    print(answer)
