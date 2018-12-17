## Analyze the comment data
## Converts file to TF-IDF vectors
## Runs regression

## Clean the raw comment data

import json
import os
import re
import string
import numpy as np
import sklearn as sk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Global variables
output_dir = "data"
# Input data files
fp_data_clean_demo = os.path.join(output_dir, "data_demo_clean.json")
fp_data_clean_repub = os.path.join(output_dir, "data_repub_clean.json")

data_demo = {}
data_repub = {}

with open(fp_data_clean_demo, "r") as json_file:
    data_demo = json.load(json_file)
    json_file.close()

with open(fp_data_clean_repub, "r") as json_file:
    data_repub = json.load(json_file)
    json_file.close()

# Create lookup dictionary
# Key is a number, comment id is value
lookup = {}

# Create labels
# 0 for democrat, 1 for republican
# indexed by comment number
label = np.array([])
index = 0
# Create corpus
# Key is number in lookup, value is text for repsctive comment
corpus_raw = {}

# Process all the above
for comment_id in data_demo:
    lookup[index] = comment_id
    label = np.append(label, 0)
    corpus_raw[index] = data_demo[comment_id]["text"].encode('ascii')
    index += 1
for comment_id in data_repub:
    lookup[index] = comment_id
    label = np.append(label, 1)
    corpus_raw[index] = data_repub[comment_id]["text"].encode('ascii')
    index += 1

# Create corpus of TF-IDF vectors
# Corpus is a sparse matrix; each row is a different document
tfidf = TfidfVectorizer(stop_words = 'english', ngram_range = (1, 2))
corpus = tfidf.fit_transform(corpus_raw.values())

# Get a test-train split
comment_train, comment_test, label_train, label_test = train_test_split(corpus, label, test_size=0.2)


# Run logistic regression, get coefficents
model = LogisticRegression(penalty = "l2", solver = "lbfgs", max_iter = 100, fit_intercept = False)
model.fit(comment_train, label_train)
coef = model.coef_[0]

# Get label for testing data
label_test_pred = np.matmul(comment_test.toarray(), coef)

# Get summary statistics on prediction
def calculate_f1(true, predicted, threshold = 0):
    """
    Calculates the F1 score

    :param true: the actual labels
    :param predicted: predicted labels
    :return: returns nothing, prints out F1 score
    """
    # Threshold the values
    predicted[predicted > threshold] = 1
    predicted[predicted <= threshold] = 0
    tp = 0.0
    tn = 0.0
    fp = 0.0
    fn = 0.0

    for idx in range(0, len(true)):
        # tp: both positive
        if true[idx] == 1 and predicted[idx] == 1:
            tp += 1
        # tn; both negative
        elif true[idx] == 0 and predicted[idx] == 0:
            tn += 1
        # fp: predicted 1 but 0
        elif true[idx] == 0 and predicted[idx] == 1:
            fp += 1
        else:
            fn += 1

    # Get f1 score
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)

    f1 = 2 / ((1 / recall) + (1 / precision))
    print f1
    print tp
    print tn
    print fp
    print fn
calculate_f1(label_test, label_test_pred)


# Get the 20 highest and 20 lowest coefficents




# feature_names = tfidf.get_feature_names()
# corpus_index = [n for n in corpus_raw]
# rows, cols = corpus.nonzero()
# #for row, col in zip(rows, cols):
# #    print((feature_names[col], corpus_index[row]), corpus[row, col])
