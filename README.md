# Token Classfication Label Error Detection 
---
Code to product results from the paper: 
[Detecting Label Errors in Token Classification Data](https://arxiv.org/pdf/2210.03920.pdf). *Preprint. Under review.* 

#### Download Datasets 
---
CoNLL-2003: 
- Original paper: [Introduction to the CoNLL-2003 Shared Task:
Language-Independent Named Entity Recognition](https://arxiv.org/pdf/cs/0306050v1.pdf) 
- Original dataset: [Papers with Code](https://paperswithcode.com/dataset/conll-2003). 
- Verified Labels: https://github.com/ZihanWangKi/CrossWeigh/tree/master/data 
- CrossWeigh Paper for CoNLL++: [CrossWeigh: Training Named Entity Tagger from Imperfect Annotations](https://aclanthology.org/D19-1519.pdf) 

#### Experiment 
--- 

`token-classification-benchmark.ipynb`: We experiment 11 different methods of aggregating the label quality scores for each token and obtain sentence label quality score, and evaluate the precision-recall curve for each method. We consider the named entity recognition dataset CoNLL-03, and use CoNLL++ as the ground truth. We propose a simple yet effective method which considers the worst token label in the sentence, which consistently detects sentences that contain errors across three experiments. 

`token-level.ipynb`: We examine the token-level label errors for the same dataset, which revealed numerous label errors in the original CoNLL-03 dataset. We show the distribution of the label errors by class, and experiment different label quality scoring methods on the token-level. Our results show that `self_confidence` is the most effective method to detect label errors. 