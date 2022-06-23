# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:01:22 2022

@author: XUEY0013
"""
import pandas as pd
from match.faq import FAQ
from evaluation.metric import *

class Evaluator:
    def __init__(self, test_file):
        self.df = pd.read_csv(test_file, encoding='unicode_escape')
        
    def evaluate(self, faq):
        q_set = {}
        qid = 1
        for index, row in self.df.iterrows():
            pred_tuples = faq.get_ranks(row["Question"], threshold = 0.5)
            std_q_column = faq.df.loc[faq.df["Question"] == row["corresponding standard question"]]
            if not std_q_column.empty:
                std_qid = std_q_column.iloc[0]["QuestionID"]
                std_cat = std_q_column.iloc[0]["Catergory"]
                top_5_pred = [p[0] for p in pred_tuples[:5]] #pred with top 5 similarity scores
                gt = faq.df.loc[(faq.df["QuestionID"] == std_qid) & (faq.df["Catergory"] == std_cat)].index.tolist() #correct questions
                q_set[qid] = [gt, top_5_pred]
            else:
                q_set[qid] = [[], []]
            qid += 1
        return eval_map_mrr(q_set)
            
if __name__ == "__main__":
    faq = FAQ("../chat/trainDataFinal.csv")
    evaluator = Evaluator("../evaluation/chatbot_testing.csv")
    MAP, MRR = evaluator.evaluate(faq)
    print(f"MAP = {MAP}, MRR = {MRR}")
    #print(rq)