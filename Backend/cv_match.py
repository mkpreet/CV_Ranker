import numpy as np
import pymongo
from sklearn.metrics.pairwise import cosine_similarity
import torch
from sentence_transformers import SentenceTransformer
import os
import json
import time


client = pymongo.MongoClient(
    "mongodb+srv://backenddatabase2:Duj2B959bdr24pwB@cluster0.kmyon.mongodb.net/Applicant?retryWrites=true&w=majority&appName=Cluster0"
)

# Database and Collection
db = client["cuDatabase"]
cvdata = db["applicants"]
jddata=db["jddatas"]

# Fetch all documents

documents = cvdata.find()

documents2=jddata.find()
# Convert MongoDB documents to a list of dictionaries
# data_list = [doc for doc in documents]
# for doc in documents:
#     data_list=doc

#cv_data
data_list = [doc for doc in documents]

#jd_data
data_list2=[]
for idx, doc in enumerate(documents2):
    data_list2.append(doc)
    if idx == 0:  # After the second iteration (0-based index)
        break

# File to save the data
file_name = "cvdata.json"
file_name2="jddata.json"

# Write to JSON file
with open(file_name, "w") as json_file:
    json.dump(data_list, json_file, indent=4, default=str)


with open(file_name2, "w") as json_file:
    json.dump(data_list2, json_file, indent=4, default=str)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
roberta_model = SentenceTransformer('roberta-base-nli-stsb-mean-tokens', cache_folder=os.path.join(os.getcwd(), 'embedding')).to(device)


def embedding(documents,embedding_model='roberta'):

    if embedding_model == 'roberta':
    
        document_embeddings = roberta_model.encode(documents)
        return document_embeddings

def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


# def save_embeddings(data, filename):
#     """
#     Compute embeddings and save them to a file.
#     """
#     print("data",data)
#     print(type(data))
#     embeddings = {key: embedding(value) for key, value in data.items()}
#     np.save(filename, embeddings)


def load_embeddings(filename):
    """
    Load precomputed embeddings from a file.
    """
    return np.load(filename, allow_pickle=True).item()



def flatten_data(data, parent_key=''):
    """
    Recursively flatten nested dictionaries or lists into descriptive strings.
    """
    flattened = {}

    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}_{key}" if parent_key else key
            if isinstance(value, (dict, list)):
                flattened.update(flatten_data(value, full_key))
            else:
                # Convert primitive types to strings
                flattened[full_key] = str(value) if value is not None else ''
    elif isinstance(data, list):
        # Concatenate list items into a single string
        combined_list = []
        for item in data:
            if isinstance(item, (dict, list)):
                combined_list.append(json.dumps(flatten_data(item)))
            else:
                combined_list.append(str(item))
        flattened[parent_key] = " ".join(combined_list)
    else:
        # Base case for primitive types
        flattened[parent_key] = str(data) if data is not None else ''


    if 'skills_hardSkills' in flattened and 'skills_softSkills' in flattened:
        flattened['skills'] = flattened['skills_hardSkills'] + " " + flattened['skills_softSkills']
    
    return flattened


def save_embeddings(data, filename):
    """
    Compute embeddings for nested data and save them to a file.
    """
    flattened_data = flatten_data(data)  # Flatten the entire document
    embeddings = {key: embedding([value]) for key, value in flattened_data.items() if value}


    if 'hardSkills' in embeddings and 'softSkills' in embeddings and 'experienceSkills' in embeddings and 'preferredQualification' in embeddings:
        embeddings['skills'] = embeddings['hardSkills'] + embeddings['softSkills']+embeddings['experienceSkills']+embeddings['preferredSkills']

    if 'essentialQualification' in embeddings and 'preferredQualification' in embeddings:
        embeddings['education'] = embeddings['essentialQualification'] + embeddings['preferredQualification']

    if 'overallExperience' in embeddings and 'relevantExperience' in embeddings:
        embeddings['experience'] = embeddings['overallExperience'] + embeddings['relevantExperience']

    # if 'certificates'in embeddings and 'experience' in embeddings:
    #     embeddings['experience']= embeddings['certificates']+embeddings['experience']
         

    np.save(filename, embeddings)
    #print(embeddings)


# Load JD and CV data from JSON files
jd_texts = load_json_file('jddata.json')
cv_texts = load_json_file('cvdata.json')

first_names = [entry['firstName'] for entry in cv_texts]
#print(first_names)

jd_embeddings_file = 'jd_embeddings.npy'
cv_embeddings_file = 'cv_embeddings.npy'



if not os.path.exists(jd_embeddings_file):
    # save_embeddings(jd_texts, jd_embeddings_file)
    jd_embeddings_list=[save_embeddings(jd,'jd_embeddings.npy') for jd in jd_texts]
    

if not os.path.exists(cv_embeddings_file):
    cv_embeddings_list = [save_embeddings(cv, f'cv_embeddings_{idx}.npy') for idx, cv in enumerate(cv_texts)]

    

# Load precomputed embeddings
start=time.time()
# jd_embeddings = load_embeddings(jd_embeddings_file)
jd_embeddings_list = [load_embeddings('jd_embeddings.npy')for _ in jd_texts]
#print(jd_embeddings)
end=time.time()



cv_embeddings_list = [load_embeddings(f'cv_embeddings_{idx}.npy') for idx, _ in enumerate(cv_texts)]

def weighted_cosine_similarity(jd_embeddings, cv_embeddings, weights):
    total_score = 0.0
    for component in weights:
        if component in jd_embeddings and component in cv_embeddings:
        #print("components",component)
            jd_vector = jd_embeddings[component]
            cv_vector = cv_embeddings[component]
            cosine_sim = cosine_similarity(jd_vector.reshape(1, -1), cv_vector.reshape(1, -1))[0][0]

            
            weighted_score = cosine_sim * weights[component]
            total_score += weighted_score
    return total_score

def print_score(weights):

    # total_weight = sum(weights.values())
    # weights = {k: v / total_weight for k, v in weights.items()}

    scores = []
    start2=time.time()
    for jd_embeddings in jd_embeddings_list:
        for idx, cv_embeddings in enumerate(cv_embeddings_list):
            #print(cv_embeddings)
            match_score = weighted_cosine_similarity(jd_embeddings, cv_embeddings, weights)
            scores.append((first_names[idx], float(match_score)))
            end2=time.time()
            # cv_embeddings = {component: embedding(text) for component, text in cv.items()}
            # cv_embeddings_list.append(cv_embeddings) 

            # match_score = weighted_cosine_similarity(jd_embeddings, cv_embeddings, weights)
            # scores.append((f"Applicant {idx + 1}", float(match_score)))

        scores.sort(key=lambda x: x[1], reverse=True)

        print("\nMatch Scores:")
        for cv_id, score in scores:
            print(f"{cv_id} Match Score: {score:.4f}")
        return scores


# weights = {
#     "skills":0.35,
#     "experience": 0.35,
#     "education": 0.30,
#     "project": 0.0,
#     "courses": 0.0,
#     "certificates": 0,
#     "languages": 0,
#     "awards": 0,
#     "achievement":0,
#     "internships":0,
#     "researchPapers":0,
#     "portfolio":0,
#  }

# print_score(weights)


 