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
model = LogisticRegression(class_weight = "balanced", penalty = "l2", C = 2, solver = "lbfgs", max_iter = 10000, fit_intercept = False)
model.fit(comment_train, label_train)
coef = model.coef_[0]

# Get label for testing data
label_test_pred = np.matmul(comment_test.toarray(), coef)

# Get summary statistics on prediction
def calculate_f1(true, predicted, threshold = 0, out = True):
    """
    Calculates the F1 score

    :param true: the actual labels
    :param predicted: predicted labels
    :return: returns nothing, prints out F1 score
    """
    # Threshold the values
    predicted_values = np.copy(predicted)
    predicted_values[predicted_values > threshold] = 1
    predicted_values[predicted_values <= threshold] = 0
    tp = 0.0
    tn = 0.0
    fp = 0.0
    fn = 0.0

    for idx in range(0, len(true)):
        # tp: both positive
        if true[idx] == 1 and predicted_values[idx] == 1:
            tp += 1
        # tn; both negative
        elif true[idx] == 0 and predicted_values[idx] == 0:
            tn += 1
        # fp: predicted 1 but 0
        elif true[idx] == 0 and predicted_values[idx] == 1:
            fp += 1
        else:
            fn += 1

    # Return f1 score of zero if divide by zero
    if (tp + fn) == 0 or (tp + fp) == 0:
        return 0, threshold
    # Get f1 score
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)

    f1 = 2 / ((1 / recall) + (1 / precision))

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    if out:
        print "F1 Score:", f1
        print "Accuracy:", accuracy
        print int(tp + tn), "correct out of", int(tp + tn + fp + fn)
    return f1, threshold

# Get the maximum F1-score and threshold
max_thresh = 0.0
max_f1 = 0.0

for i in range(0, 600):
    thresh = -3 + i / 100.0
    f1, thresh = calculate_f1(label_test, label_test_pred, thresh, out = False)

    if f1 > max_f1:
        max_f1 = f1
        max_thresh = thresh

print "Results"
print "Highest threshold is", max_thresh
calculate_f1(label_test, label_test_pred, threshold = 0, out = True)


# Get the 20 highest and 20 lowest coefficents, and their respective words
# 1 is republican, 0 is democrat
idx_max = (-coef).argsort()[:20]
idx_min = (coef).argsort()[:20]

words_demo = []
words_repub = []

feature_names = tfidf.get_feature_names()

# Add the highest/ lowest coefficent word to their party prediction
for word_idx in idx_max:
    words_repub.append(feature_names[word_idx])

for word_idx in idx_min:
    words_demo.append(feature_names[word_idx])

print
print "20 Words/ Vectors most associated with Democratic Party: "
print words_demo
print

print "20 Words/ Vectors most associated with Republican Party: "
print words_repub
