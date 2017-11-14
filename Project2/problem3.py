import sqlite3
from collections import defaultdict
import numpy as np
import itertools
import time

conn = sqlite3.connect('reddit.db')

start = time.time()

conn.row_factory = sqlite3.Row

query = """
SELECT id, name FROM subreddits 
"""
cursor = conn.execute(query)

names_d = defaultdict() #dictionary for the names
subreddit_ids = [] #list of subreddits
for row in cursor:
    subreddit_ids.append(row[0])
    names_d[row[0]] = row[1]
    
query = """
SELECT id, parent_id, subreddit_id FROM comments ORDER BY id DESC
"""

cursor = conn.execute(query)

#Construct dictionary placeholder
sub_red = defaultdict(dict)
for sub in subreddit_ids:
    sub_red[sub] = defaultdict(int)

i = 0
start = time.time()
cursor = conn.execute(query)
for row in cursor:
    #id = max(id, subcomment + 1)
    sub_red[row[2]][row[1]] = max(sub_red[row[2]][row[1]], sub_red[row[2]][row[0]] + 1)
    sub_red[row[2]].pop(row[0])
    
    i += 1
    if i % 5300000 == 0:
        print("Progress: ", i/530000, "%  || time: ", time.time()-start)

print("Time", time.time()-start)

avg_depth = []
for i in range(len(subreddit_ids)):
    res = []
    for k, v in sub_red[subreddit_ids[i]].items():
        if k[:2] == "t3":
            res.append(v-1)
    if len(res) > 0:
        avg_depth.append(np.mean(res))
    else:
        avg_depth.append(0)
        
        
index = np.array(avg_depth).argsort()[-10:][::-1]

print("Final Time: {} sec".format(time.time()-start))
print("Avg Depth     id           name")
for x in index:
    print("{:.1f}         {}     {}".format(avg_depth[x], subreddit_ids[x], names_d[subreddit_ids[x]]))
    