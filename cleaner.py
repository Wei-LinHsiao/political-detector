## Clean the raw comment data

import praw
import json
import os
import re
import string

# Global variables
output_dir = "data"
# Input data files
fp_data_demo = os.path.join(output_dir, "data_demo_full.json")
fp_data_repub = os.path.join(output_dir, "data_repub_full.json")
# Output data files
fp_data_clean_demo = os.path.join(output_dir, "data_demo_clean.json")
fp_data_clean_repub = os.path.join(output_dir, "data_repub_clean.json")


# Comment data for each party
data_demo = {}
data_repub = {}
cleaned_demo = {}
cleaned_repub = {}

with open(fp_data_demo, "r") as json_file:
    data_demo = json.load(json_file)
    json_file.close()

with open(fp_data_repub, "r") as json_file:
    data_repub = json.load(json_file)
    json_file.close()


def clean(input_dict, output_dict):
    """
    Cleans input_dict, saves result in output_dict

    :param input_dict: Dictionary of raw comments
    :param output_dict: Dictionary of cleaned data, modified
    :return: nothing, modifies output_dict
    """
    # Processess all comments
    for comment_id in input_dict:

        text = input_dict[comment_id]["text"]
        # Make sure there are at least 15 words in the comment
        # Has side effect of removing deleted comments
        if len(text.split()) < 15:
            continue

        # Remove all unicode characters
        # Remove non-space punctuation
        text = re.sub(r'[^\w\s]', r'', text)

        # Turn whitespace into spaces
        text = re.sub(r'[\n\s]', r' ', text)

        # Remove double spaces
        text = re.sub(' +', r' ', text)

        # Turn all text to lowercase
        text = text.lower()

        #
        com_prop = {}

        # Modify input_dict to have new properties
        com_prop["text"] = text
        com_prop["score"] = input_dict[comment_id]["score"]
        com_prop["time"] = input_dict[comment_id]["time"]
        com_prop["srd"] = input_dict[comment_id]["srd"]

        # Stored in party-corresponding dictionary by id
        output_dict[comment_id] = com_prop

clean(data_demo, cleaned_demo)
clean(data_repub, cleaned_repub)

# Outputs cleaned data
with open(fp_data_clean_demo, "w+") as json_file:
    json.dump(cleaned_demo, json_file, indent = 4)
    json_file.close()

with open(fp_data_clean_repub, "w+") as json_file:
    json.dump(cleaned_repub, json_file, indent = 4)
    json_file.close()

print "Number of comments for demo:"
print len(cleaned_demo)
print

print "Number of comments for repub:"
print len(cleaned_repub)
print
