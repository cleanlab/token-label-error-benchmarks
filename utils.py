import numpy as np

entities = [
    "O",
    "B-MISC",
    "I-MISC",
    "B-PER",
    "I-PER",
    "B-ORG",
    "I-ORG",
    "B-LOC",
    "I-LOC",
]
entity_map = {entity: i for i, entity in enumerate(entities)}


def readfile(filepath, sep=" "):
    """
    Reads file in CoNLL format (IOB2)
    """
    lines = open(filepath)

    data, sentence, label = [], [], []
    for line in lines:
        if len(line) == 0 or line.startswith("-DOCSTART") or line[0] == "\n":
            if len(sentence) > 0:
                data.append((sentence, label))
                sentence, label = [], []
            continue
        splits = line.split(sep)
        word = splits[0]
        if len(word) > 0 and word[0].isalpha() and word.isupper():
            word = word[0] + word[1:].lower()
        sentence.append(word)
        label.append(entity_map[splits[-1][:-1]])

    if len(sentence) > 0:
        data.append((sentence, label))

    given_words = [d[0] for d in data]
    given_labels = [d[1] for d in data]

    return given_words, given_labels


def get_probs(pipe, sentence):
    """
    @parameter pipe
    @parameter sentence: string

    @return probs: np.array of shape (n, m)
        where n is the number of tokens in the sentence and m is the number of classes.
        probs[i][j] is the probability that the i'th sentence belongs to entity j. The
        first and last probs are excluded because the first and last tokens are always
        [CLS] and [SEP], to represent the start and end of the sentence, respectively.
    """

    def softmax(logit):
        return np.exp(logit) / np.sum(np.exp(logit))

    forward = pipe.forward(pipe.preprocess(sentence))
    logits = forward["logits"][0].numpy()
    probs = np.array([softmax(logit) for logit in logits])
    probs = probs[1:-1]
    return probs


def get_pred_probs(scores, tokens, given_token, weighted=False):
    """
    Obtain `pred_probs` for one particular sentence. Maps and reduces subword-level tokens to the given
    word-level tokens in the original dataset.
    Parameters
    ----------
    scores: np.array
        np.array with shape `(N', K)`, where N' is the number of tokens of the sentence generated by the
        tokenizer, and K is the number of classes of the model prediction. `scores[i][j]` indicates the
        model-predicted probability that the i'th token belongs to class j.
    tokens: list
        list of tokens with length N' generated by the tokenizer.
    given_token: list
        list of given tokens with length N, where N is the number of tokens of the sentence from the
        original dataset.
    weighted: bool, default=False
        whether to merge the probabilities using a weighted average (or unweighted average). The weight
        is proportional to the length of the subword-level token.
    Returns
    ---------
    pred_probs: np.array
        np.array with shape `(N, K)`, where `pred_probs[i][j]` is the model-predicted probability that the
        i'th token belongs to class j after processing (reducing subwords to words, and spliting words
        merged by the tokenizers).
    """
    i, j = 0, 0
    pred_probs = []
    for token in given_token:
        i_new, j_new = i, j
        acc = 0

        weights = []
        while acc != len(token):
            token_len = len(tokens[i_new][j_new:])
            remain = len(token) - acc
            weights.append(min(remain, token_len))
            if token_len > remain:
                acc += remain
                j_new += remain
            else:
                acc += token_len
                i_new += 1
                j_new = 0

        if i != i_new:
            probs = np.average(
                scores[i:i_new], axis=0, weights=weights if weighted else None
            )
        else:
            probs = scores[i]
        i, j = i_new, j_new

        pred_probs.append(probs)

    return np.array(pred_probs)
