
def eval_map_mrr(q_set):
    MAP = 0.0
    MRR = 0.0
    useful_q_len = 0
    for q in q_set.items():
        correct = 0
        total = 0
        AP = 0.0
        mrr_mark = False
        for p in q[1][1]: #q[1][0]: true answer, q[1][1]: top 5 predictions
            if p in q[1][0]:
                correct += 1
        if correct == 0:
            continue
        useful_q_len += 1
        correct = 0
        for i in range(len(q[1][1])):
            # compute MRR
            if q[1][1][i] in q[1][0] and mrr_mark == False:
                MRR += 1.0 / float(i + 1)
                mrr_mark = True
            # compute MAP
            total += 1
            if q[1][1][i] in q[1][0]:
                correct += 1
                AP += float(correct) / float(total)
        
        AP /= float(correct)
        MAP += AP

    MAP /= useful_q_len
    MRR /= useful_q_len
    print("No of useful question:", useful_q_len)
    return MAP, MRR

def build_embedding(in_file, word_dict):
	# 构建预训练的embedding矩阵
    num_words = max(word_dict.values()) + 1
    dim = int(in_file.split('.')[-2][:-1])
    embeddings = np.zeros((num_words, dim))

    if in_file is not None:
        pre_trained = 0
        initialized = {}
        avg_sigma = 0
        avg_mu = 0
        for line in open(in_file).readlines():
            sp = line.split()
            assert len(sp) == dim + 1
            if sp[0] in word_dict:
                initialized[sp[0]] = True
                pre_trained += 1
                embeddings[word_dict[sp[0]]] = [float(x) for x in sp[1:]]
                mu = embeddings[word_dict[sp[0]]].mean()
                #print embeddings[word_dict[sp[0]]]
                sigma = np.std(embeddings[word_dict[sp[0]]])
                avg_mu += mu
                avg_sigma += sigma
        avg_sigma /= 1. * pre_trained
        avg_mu /= 1. * pre_trained
        for w in word_dict:
            if w not in initialized:
                embeddings[word_dict[w]] = np.random.normal(avg_mu, avg_sigma, (dim,))
        print('Pre-trained: %d (%.2f%%)' %
                     (pre_trained, pre_trained * 100.0 / num_words))
    return embeddings.astype(np.float32)
