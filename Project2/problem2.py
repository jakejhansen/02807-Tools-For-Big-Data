import sqlite3
from collections import defaultdict
import numpy as np
import itertools
import time

conn = sqlite3.connect('reddit.db')

start = time.time()

#Get the names of the subreddits
query = """
SELECT id, name FROM subreddits 
"""
cursor = conn.execute(query)

names_d = defaultdict() #dictionary for the names
for row in cursor:
    names_d[row[0]] = row[1]

query = """
SELECT author_id, subreddit_id FROM comments
"""
cursor = conn.execute(query)

sub_red = defaultdict(set)
i = 0
for row in cursor:
    sub_red[row[1]].add(row[0])
        
t2 = sorted(sub_red, key=lambda k: len(sub_red[k]), reverse = True) #sort based on length
combinations = list(itertools.combinations(t2[:15],2)) #find all 2-combinations of 15 biggest subreddits

pairs = [] #differnt possible pairs
for comb in combinations:
    #Intersect set of authors to find how many is in common
    pairs.append(len(sub_red[comb[0]].intersection(sub_red[comb[1]])))
    
    
index = np.array(pairs).argsort()[-10:][::-1]
    
conn.close()