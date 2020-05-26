#Importing the required libraries
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


import pandas as pd

from sentence_transformers import SentenceTransformer


#Initializing an elastic client
es = Elasticsearch([{'host':'localhost','port':9200}])


#Initializing the required model
model = SentenceTransformer('bert-large-nli-stsb-mean-tokens')

def ingest():

#Reading the excel file
    df = pd.read_excel('SampleFAQs.xlsx')


#Separating the questions and answers fields
    X = df.iloc[:,0].values
    Y = df.iloc[:,1].values

    questions = []
    for i in X:
        questions.append(str(i))


    answers = []
    for i in Y:
        answers.append(str(i))


#In order to improve the accuracy of search, consider both the questions and answers to create embeddings

    data = []
    for i in range(len(questions)):
        data.append(questions[i]+ '. ' +answers[i])

#Creating the embeddings using the model
    data_vectors = model.encode(data)


#Creating an object with the required fields in order to ingest
    vector = index(data, data_vectors)

    bulk(es, vector)

def index(data, data_vectors):
    for i in range(len(data)):
        BASE_VECTORS = data_vectors[i].tolist()
        print("done")
        yield {
                "_index": 'sample',
                "ques" : questions[i],
                "ans" : answers[i],
                "vector" : BASE_VECTORS
                 }

if __name__ == '__main__':
    ingest()