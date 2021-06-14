# getUseEmbedding.py

import pandas as pd
import requests
import json
import time
import os
# if calling from DSAlpha
#endpoint = "http://useapi:8501/v1/models/use:predict"
# if calling from outside DSAlpha
endpoint = "https://dsalpha.vmhost.psu.edu/api/use/v1/models/use:predict"

os.chdir("./text/")
data = pd.read_csv("cars_pets.csv")
#print(data.head())
print(data.iloc[:,0])
def getUseEmbedding(text):

    #text = list(text)
    #print("text:",text)
#name of col
text = data['text']
text = list(text)
#print(text)

json_data = {"instances":text}
#print("json_data:",json_data)
result = requests.post(endpoint, json=json_data)
print("result:", result)
embeddings = result.json()['predictions']
string="dim"
header=[string+str(i) for i in range(512)]
emb = pd.DataFrame(embeddings, columns = header)
print(emb)

frames = [data, emb]
result_new = pd.concat(frames, axis = 1)
print(result_new.head())
result_new.to_csv("USE1.csv")
#return(emb)

#getUseEmbedding(data.iloc[:,0])
