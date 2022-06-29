import torch
from sentence_transformers import SentenceTransformer, util
import pandas as pd

class QA:
    """
    HuggingFace BERT language model pre-trained on SQUAD.
    Ref: https://huggingface.co/transformers/index.html

    How does BERT answer questions?
    Ref: https://openreview.net/pdf?id=SygMXE2vAE
    """
    def __init__(self, excel_file):
        #self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = SentenceTransformer('carlosaguayo/features_and_usecases')
        self.df = pd.read_csv(excel_file)
        self.token_list = [self.model.encode(s) for s in self.df['Question']]

    def ask(self, question, threshold=0.6):
        """Ask question to QA."""
        score, answer = self.query(question)
        print("NLP score:", score)
        print("Answer:", answer)

        if score > threshold:
            return answer
        else:
            return None

    def query(self, question):
        """
        Query question with reference to the previously given passage.
        Returns (score, answer)
        Ref: https://huggingface.co/transformers/model_doc/bert.html#bertforquestionanswering
        """
        #input_text = "[CLS] " + question + " [SEP] " + self.passage + " [SEP]"
        #print(input_text)
        #input_ids = self.tokenizer.encode(input_text)
        #token_type_ids = [0 if i <= input_ids.index(102) else 1 for i in range(len(input_ids))]
        #start_scores, end_scores = self.model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
        #all_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
        #score = self.compute_score(start_scores, end_scores)
        #answer = ' '.join(all_tokens[torch.argmax(start_scores): torch.argmax(end_scores) + 1])
        #return score, answer
        max_score = 0
        question_idx = 0
        token_text = self.model.encode(question)
        temp = []
        for i, q in enumerate(self.token_list):
            s = self.compare(token_text, q)
            temp.append((q, i, s))
            if s > max_score:
                max_score = s
                question_idx = i
        return max_score, self.df['Answer'][question_idx]

    def get_ranks(self, question, threshold=0.8):
        """Returns FAQ answer if similarity score exceeds threshold"""
        max_score = 0
        token_text = self.model.encode(question)
        temp = []
        for i, q in enumerate(self.token_list):
            s = self.compare(token_text, q)
            temp.append((i, s))
            if s > threshold:
                temp.append((i, s))
            if s > max_score:
                max_score = s       
        rank = sorted(temp, key=lambda i: i[-1], reverse=True)
        # print(rank[:3], "FAQ score:", max_score)
        if max_score > threshold:
            return rank
        else:
            return None
    
    def compare(self, embedding1, embedding2):
        return util.pytorch_cos_sim(embedding1, embedding2).item()
        

if __name__ == "__main__":
    """Example"""
    qa = QA("../chat/trainDataFinal.csv")
    #score, answer = qa.query("What is Covid?")
    #print("Answer:", answer)
    #print("Score:", score)
    print(qa.query("What is Covid?"))
    