## Analyze the comment data
## Converts file to TF-IDF vectors
## Runs regression

## Clean the raw comment data

import json
import os
import re
import string
import numpy as np

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
corpus = {}

# Process all the above
for comment_id in data_demo:
    lookup[index] = comment_id
    label = np.append(label, 0)
    corpus[index] = data_demo[comment_id]["text"].encode('ascii')
    index += 1
for comment_id in data_repub:
    lookup[index] = comment_id
    label = np.append(label, 1)
    corpus[index] = data_repub[comment_id]["text"].encode('ascii')
    index += 1

