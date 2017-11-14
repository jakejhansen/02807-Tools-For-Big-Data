import sqlite3
import time
from collections import defaultdict

def bodyToWords(body, words):
    #Davids script that takes a body of text and returns all the words in it
    symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']
    body = body.lower()
    for sym in symbols:
        body = body.replace(sym, " ")

    for w in body.split(" "):
        if len(w.replace(" ","")) > 0:
            words.add(w)
        
    return words


start = time.time()
conn = sqlite3.connect('reddit.db')

query = """
SELECT id, name FROM subreddits 
"""
cursor = conn.execute(query)

subreddit_ids = [] #list of subreddits
names_d = defaultdict() #dictionary for the names
for row in cursor:
    subreddit_ids.append(row[0])
    names_d[row[0]] = row[1]


vocabulary_size = defaultdict(int)

query = """
SELECT subreddit_id, body FROM comments order by subreddit_id
"""
cursor = conn.execute(query)
subred_prev = 't5_1a8ah' #starting point

words = set()
i = 0
for row in cursor:
    if row[0] != subred_prev: #new subreddit
        vocabulary_size[subred_prev] += len(words) #add voc size to dict
        words = set()
        subred_prev = row[0]
        pass
    
    bodyToWords(row[1], words)
    
    i += 1
    if i % 530000 == 0:
        print("Progress: ", i/530000, "%  || time: ", time.time()-start)
    
print("Time", time.time()-start)


t = sorted(vocabulary_size, key=vocabulary_size.get, reverse = True) #sort based on size
print("Time: {} min".format((time.time()-start)/60))
print("Size:   id:       Name:") 
for x in range(10):
    print("{}  {}  {}".format(vocabulary_size[t[x]], t[x], names_d[t[x]]))