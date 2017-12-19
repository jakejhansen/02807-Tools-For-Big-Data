import json, glob
import numpy as np

cleaned_data = []

#Load every datafile
for file in glob.glob('full/*'):
    data = json.load(open(file))
    
    for elem in data:
        #Check if the article has both an topic and body-element
        if 'topics' in list(elem.keys()) and 'body' in list(elem.keys()):
            cleaned_data.append(elem)
            
print("Number of articles:", len(cleaned_data))

#Construct dictionary over unique words in all articles
dictionary = set()
for article in cleaned_data:
    for word in article['body'].lower().split():
        dictionary.add(word)
print("Number of unique words:", len(dictionary))

# Make it into a dictioniary, with each word having an index as value
from collections import defaultdict
features = defaultdict(int)
for i, word in enumerate(dictionary):
    features[word] = i



bag_of_words = np.zeros((len(cleaned_data), len(features)))

#Consturct bag-of-words for all articles by looking up the ID of all the words
for i, article in enumerate(cleaned_data):
    for word in article['body'].lower().split():
        bag_of_words[i][features[word]] += 1

print("articles, features")        
print(bag_of_words.shape)



from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

#Prepare data
y = np.zeros(len(cleaned_data))
for i, article in enumerate(cleaned_data):
    if 'earn' in article['topics']:
        y[i] = 1
        
X = bag_of_words

#Split data into test and validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Construct RFC
clf = RandomForestClassifier(n_estimators = 50)
clf.fit(X_train, y_train)

#Test performance
print("Accuracy on train-set =", clf.score(X_train, y_train))
print("Accuracy on test-set =", clf.score(X_test, y_test))

num_bins = 1000
hashed = np.zeros((len(cleaned_data), num_bins))

for i, article in enumerate(cleaned_data):
    for word in article['body'].lower().split():
        #Just hash the features 
        hashed[i][features[word] % num_bins] += 1

print("articles, features")        
print(hashed.shape)

X = hashed


#Split data into test and validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Construct RFC
clf = RandomForestClassifier(n_estimators = 50)
clf.fit(X_train, y_train)

#Test performance
print("Accuracy on train-set = ", clf.score(X_train, y_train))
print("Accuracy on test-set = ", clf.score(X_test, y_test))