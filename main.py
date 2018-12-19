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
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing
from sklearn.metrics import classification_report


# Global variables
output_dir = "data"
# Input data files
fp_data_clean_demo = os.path.join(output_dir, "data_demo_clean.json")
fp_data_clean_repub = os.path.join(output_dir, "data_repub_clean.json")
coef_out = os.path.join(output_dir, "coef.csv")

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
tfidf = TfidfVectorizer(stop_words = 'english', ngram_range = (1, 2), max_features = 5000)
corpus = tfidf.fit_transform(corpus_raw.values())

# Normalize each feature
# Model performs better without normalization
# corpus_scaled = preprocessing.scale(corpus.toarray())

# Get a test-train split
comment_train, comment_test, label_train, label_test = train_test_split(corpus, label, test_size = 0.2)

# Run logistic regression, get coefficents
model = LogisticRegression(penalty = "l2", C = 0.5, solver = "sag", max_iter = 1000, tol = 10e-8 , fit_intercept = False)
model.fit(comment_train, label_train)

# Get Scoring Metrics
label_predicted = model.predict(comment_test)

print classification_report(label_test, label_predicted)
print "Accuracy: ", sk.metrics.accuracy_score(label_test, label_predicted)
print "F1 Score: ", sk.metrics.f1_score(label_test, label_predicted, pos_label = 0)

# Get top 50 coresponding to Democrats, Republicans
coef = model.coef_[0]
idx_max = (-coef).argsort()[:50]
idx_min = (coef).argsort()[:50]

words_demo = []
words_repub = []

feature_names = tfidf.get_feature_names()

# Add the highest/ lowest coefficent word to their party prediction
for word_idx in idx_max:
    words_repub.append(feature_names[word_idx])

for word_idx in idx_min:
    words_demo.append(feature_names[word_idx])

print
print "Words/ Phrases most associated with Democratic Party: "
print words_demo
print

print "Words/ Phrases most associated with Republican Party: "
print words_repub

# Create a dictionary for output of words
output_words = []

# Put all coef in a table
# coefficent, value
for idx in range(0, len(coef)):
    row = [feature_names[idx], coef[idx]]
    output_words.append(row)

# Write coefficent to spreadsheet
with open(coef_out, "w+") as csv_file:
    spreadsheet = csv.writer(csv_file, delimiter=',')

    for row in output_words:
        spreadsheet.writerow(row)

    csv_file.close()
# Grid search for best model
# grid = [
#     {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000], 'solver' : ['sag'], 'class_weight': ["balanced", None],
#      'max_iter' : [10000], "fit_intercept" : [False], 'n_jobs': [-1]},
# ]
#
# clf = GridSearchCV(LogisticRegression(), grid, cv=4, n_jobs = 3)
# clf.fit(comment_train, label_train)
#
# print "Best parameters set found on development set:"
# print
# print clf.best_params_
# print
# print "Grid scores on development set:"
# print
# print "Detailed classification report:"
# print
# y_true, y_pred = label_test, clf.predict(comment_test)
# print classification_report(y_true, y_pred)
# print
#
