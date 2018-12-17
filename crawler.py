# Web crawler for comment data
# Goal of data is to make model that differentiates
# between the two main American parties, the Democratic Party
# and the Republican Party

# Saves each comment in JSON format with relevant data
# text, upvotes, date, length

import praw
import json
import os

# Global variables
output_dir = "data"
# Output files
fp_data_demo = os.path.join(output_dir, "data_demo_full.json")
fp_data_repub = os.path.join(output_dir, "data_repub_full.json")

# Loads token information for the crawler
reddit = praw.Reddit(client_id = 'PLACEHOLDER',
                     client_secret = 'PLACEHOLDER',
                     user_agent = 'PLACEHOLDER')

# List of subreddits for each party
srd_names_demo = ["SandersForPresident", "liberal", "Political_Revolution", "democrats", "progressive"]
srd_names_repub = ["the_donald", "conservative", "republican", "conservatives", "new_right"]
srd_demo = []
srd_repub = []

# Turn subreddit list into subreddit
for srd in srd_names_demo:
    srd_demo.append(reddit.subreddit(srd))

for srd in srd_names_repub:
    srd_repub.append(reddit.subreddit(srd))

# Comment data for each party
com_demo = {}
com_repub = {}

# Counter for total number of comments parsed
counter = 0

# Crawl subreddits for both parties
# Save the ones with > a threshold of upvotes
for subreddit in srd_demo:
    # Iterate through the top posts of subreddit
    for srd in subreddit.top(limit = 1):
        # Repalce "More Comment" objects with comments
        # Tree depth limited to 5
        srd.comments.replace_more(limit = 5)
        for comment in srd.comments.list():

            counter += 1

            # Get all comments with >= 50 upvotes
            if comment.score < 50:
                continue

            # Create dictionary to store properties
            # of current comment: body text, num upvotes, time posted
            com_prop = {}
            com_prop["text"] = comment.body
            com_prop["score"] = comment.score
            com_prop["time"] = comment.created_utc
            com_prop["srd"] = comment.subreddit.display_name

            # Stored in party-corresponding dictionary by id
            com_demo[str(comment.id)] = com_prop

for subreddit in srd_repub:
    # Iterate through the top posts of subreddit
    for srd in subreddit.top(limit = 1):
        # Repalce "More Comment" objects with comments
        # Tree depth limited to 5
        srd.comments.replace_more(limit = 5)
        for comment in srd.comments.list():

            counter += 1

            # Get all comments with >= 50 upvotes
            if comment.score < 50:
                continue

            # Create dictionary to store properties
            # of current comment: body text, num upvotes, time posted
            com_prop = {}
            com_prop["text"] = comment.body
            com_prop["score"] = comment.score
            com_prop["time"] = comment.created_utc
            com_prop["srd"] = comment.subreddit.display_name

            # Stored in party-corresponding dictionary by id
            com_repub[str(comment.id)] = com_prop

# Write data to JSON
with open(fp_data_demo, "w+") as json_file:
    json.dump(com_demo, json_file, indent = 4)
    json_file.close()

with open(fp_data_repub, "w+") as json_file:
    json.dump(com_repub, json_file, indent = 4)
    json_file.close()

print "Number of comments for demo:"
print len(com_demo)
print

print "Number of comments for repub:"
print len(com_repub)
print

print "Total Comments Parsed:"
print counter