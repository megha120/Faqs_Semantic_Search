#Importing the required libraries
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

#Initializing an elastic client
es = Elasticsearch([{'host':'localhost','port':9200}])


#Initializing the required model
model = SentenceTransformer('bert-large-nli-stsb-mean-tokens')


def logic(query):

#The model accepts only list of strings as a parameter
    q= [query]
    query_vec = model.encode(q)

#Converting the vector to a list in order to use the cosine similarity api of elasticsearch
    test_vector = query_vec[0].tolist()


#Query to find out the matching results using cosine similarity
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['vector']) + 1.0",
                "params": {"query_vector": test_vector}
            }
        }
    }


#Fire the query using the elastic client
    response = es.search(
    index='sample',
    body={
        "size": 10,
        "query": script_query,
        "_source": {"includes": ["ques", "ans"]}
    }
)

#Keeping only the required part of the response
    hi = response['hits']['hits']
    r = []


#For relevance point of view, taking only 7 records to display
    for i in range(7):
        r.append(hi[i])
    return r
