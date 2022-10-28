# Benchmarking methods for label error detection in token classification data

Code to reproduce results from the paper:

[**Detecting Label Errors in Token Classification Data**](https://arxiv.org/abs/2210.03920)  
*NeurIPS 2022 Workshop on Interactive Learning for Natural Language Processing (InterNLP)*

This repository is only for intended for scientific purposes. To find label errors in your own token classification data, you should instead use [the implementation](https://docs.cleanlab.ai/stable/tutorials/token_classification.html) from the official [cleanlab library](https://github.com/cleanlab/cleanlab).


#### Install Cleanlab Package 
--- 
Install the Cleanlab version used for our experiments: `pip install ./cleanlab`

#### Download Datasets 
---
CoNLL-2003: 
- Original paper: [Introduction to the CoNLL-2003 Shared Task:
Language-Independent Named Entity Recognition](https://arxiv.org/pdf/cs/0306050v1.pdf) 
- Original dataset: [Papers with Code](https://paperswithcode.com/dataset/conll-2003). 
- Verified Labels (CoNLL++): https://github.com/ZihanWangKi/CrossWeigh/tree/master/data 

#### Experiments 
--- 

`token-classification-benchmark.ipynb`: We implement 11 different methods of aggregating the label quality scores for each token to obtain an overall score per sentence, and evaluate the precision-recall curve and related label-error detection metrics for each method. We consider the named entity recognition dataset CoNLL-2003, and use CoNLL++ as the ground truth.

`token-level.ipynb`: We examine the token-level label errors for the same dataset (rather than sentence-level). We examine the distribution of the label errors by class, and evaluate different label quality scoring methods on the token-level. 
