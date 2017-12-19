from PIL import Image
import glob
import numpy as np


images = sorted(glob.glob('*.jpeg'))

features_all = []
width = 9
height = 8

# For every image in the folder
for image in sorted(glob.glob('*.jpeg')):
    #Open and resize
    im = Image.open(image).convert('L')

    img = np.array(im.resize((width,height)))

    #Do differencing
    diff = img[:, :-1] > img[:,1:]

    features = []
    print(image, end = ': ')
    
    #Use Davids script from Aula
    for difference in diff:
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            #If True, fill the position
            if value:
                decimal_value += 2**(index % (width - 1))
            #If reached the end, append it to the string and add it to features
            if (index % (width-1)) == (width-2):
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                features.append(decimal_value)
                decimal_value = 0
        print(''.join(hex_string), end='')
    print()
    
    features_all.append(features)

from pprint import pprint
from sklearn.metrics.pairwise import * 
import pandas as pd

#Compute Cosine Similarity
similarities = cosine_similarity(features_all)
images = sorted(glob.glob('*.jpeg'))

df = pd.DataFrame(similarities, index=images, columns= images)
print(df)


# Try with bigger resize
features_all = []
#Increase number of bins for better precision.
width = 25
height = 24

# For every image in the folder
for image in sorted(glob.glob('*.jpeg')):
    #Open and resize
    im = Image.open(image).convert('L')

    img = np.array(im.resize((width,height)))

    #Do differencing
    diff = img[:, :-1] > img[:,1:]

    features = []
    
    #Use Davids script from Aula
    for difference in diff:
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            #If True, fill the position
            if value:
                decimal_value += 2**(index % (width - 1))
            #If reached the end, append it to the string and add it to features
            if (index % (width-1)) == (width-2):
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                features.append(decimal_value)
                decimal_value = 0
    
    features_all.append(features)
    

similarities = cosine_similarity(features_all)
names = sorted(glob.glob('*.jpeg'))

df = pd.DataFrame(similarities, index=images, columns= images)
print(df)