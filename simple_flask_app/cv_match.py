import numpy as np
import pymongo
from sklearn.metrics.pairwise import cosine_similarity
import torch
from sentence_transformers import SentenceTransformer
import os
import json
import time


# client = pymongo.MongoClient(
#     "mongodb+srv://backenddatabase2:Duj2B959bdr24pwB@cluster0.kmyon.mongodb.net/Applicant?retryWrites=true&w=majority&appName=Cluster0"
# )

# # Database and Collection
# db = client["Applicant"]
# col = db["applicants"]

# # Fetch all documents
# #documents = col.find()
# documents = col.find()
# # Convert MongoDB documents to a list of dictionaries
# # data_list = [doc for doc in documents]
# # for doc in documents:
# #     data_list=doc

# data_list = [doc for doc in documents]

# # for idx, doc in enumerate(documents):
# #     data_list.append(doc)
# #     if idx == 1:  # After the second iteration (0-based index)
# #         break

# # File to save the data
# file_name = "CV.json"

# # Write to JSON file
# with open(file_name, "w") as json_file:
#     json.dump(data_list, json_file, indent=4, default=str)

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



def flatten_skills(skills):
    """
    Flatten the nested 'skills' dictionary into descriptive strings.
    """
    flattened = {}
    for skill_type, skill_list in skills.items():
        # Concatenate name and yearsOfExperience for each skill
        descriptions = [
            f"{skill['name']} with {skill['yearsOfExperience']} years of experience"
            for skill in skill_list
        ]
        # Combine all skill descriptions into one string
        flattened[skill_type] = " ".join(descriptions)
    return flattened

def save_embeddings(data, filename):
    """
    Compute embeddings for nested data and save them to a file.
    """
    embeddings = {}
    for key, value in data.items():
        if isinstance(value, dict):
            # Handle nested dictionaries (e.g., 'skills')
            if key == "skills":
                flattened_skills = flatten_skills(value)
                for sub_key, text in flattened_skills.items():
                    embeddings[sub_key] = embedding([text])  # Use sub-key directly
            else:
                # Flatten other dictionaries if needed
                embeddings[key] = embedding([json.dumps(value)])
        elif isinstance(value, list):
            # Handle lists (concatenate items into a single string)
            concatenated_value = " ".join(str(item) for item in value)
            embeddings[key] = embedding([concatenated_value])
        elif isinstance(value, str):
            # Directly compute embedding for the string
            embeddings[key] = embedding([value])
        else:
            # Handle other types (e.g., numbers) if meaningful
            embeddings[key] = embedding([str(value)]) if value else None
    np.save(filename, embeddings)
    # print(embeddings)


# Load JD and CV data from JSON files
jd_texts = load_json_file('JD.json')
cv_texts = load_json_file('CV.json')


jd_embeddings_file = 'jd_embeddings.npy'
cv_embeddings_file = 'cv_embeddings.npy'



if not os.path.exists(jd_embeddings_file):
    save_embeddings(jd_texts, jd_embeddings_file)

if not os.path.exists(cv_embeddings_file):
    cv_embeddings_list = [save_embeddings(cv, f'cv_embeddings_{idx}.npy') for idx, cv in enumerate(cv_texts)]

    

# Load precomputed embeddings
start=time.time()
jd_embeddings = load_embeddings(jd_embeddings_file)
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
    for idx, cv_embeddings in enumerate(cv_embeddings_list):
        #print(cv_embeddings)
        match_score = weighted_cosine_similarity(jd_embeddings, cv_embeddings, weights)
        scores.append((f"Applicant {idx + 1}", float(match_score)))
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
#     "hardSkills":0.35,
#     "experience": 0.35,
#     "education": 0.30,
#     "project": 0.0,
#     "courses": 0,
#     # "certificates": 0,
#     # "languages": 0,
#     # "awards": 0,
#     # "achievement":0,
#     # "internships":0,
#     # "researchPapers":0,
#     # "portfolio":0,
#  }

# print_score(weights)


 