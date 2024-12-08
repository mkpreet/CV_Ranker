import json
from sklearn.metrics.pairwise import cosine_similarity
import torch
from sentence_transformers import SentenceTransformer
import os
import json
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
roberta_model = SentenceTransformer('roberta-base-nli-stsb-mean-tokens', cache_folder=os.path.join(os.getcwd(), 'embedding')).to(device)


def embedding(documents,embedding_model='roberta'):

    if embedding_model == 'roberta':
    
        document_embeddings = roberta_model.encode(documents)
        return document_embeddings



def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def flatten_and_concatenate(data, parent_key=''):
    """
    Recursively flatten a nested JSON object, concatenate all values into a single string,
    and assign the concatenated string to the parent key.
    """
    result = []  # Store all the concatenated string values
    
    if isinstance(data, dict):
        for key, value in data.items():
            # Traverse deeper with the current key as parent
            result.extend(flatten_and_concatenate(value, parent_key=parent_key))
    elif isinstance(data, list):
        for item in data:
            # Traverse each item in the list
            result.extend(flatten_and_concatenate(item, parent_key=parent_key))
    else:
        # If it's a base value, add it to the result as a string
        result.append(str(data))
    
    # Combine all the strings under the parent_key
    return [f"{parent_key}: {' '.join(result)}"] if parent_key else result

# Usage example


# Generate the combined string
flattened_data = flatten_and_concatenate(load_json_file('abc.json'), parent_key="skills")

# The result will be a single string concatenated under the "skills" key
print(flattened_data)  # ['skills: JAVA 10 Communication dhkfjhjk']

# Embedding
combined_value = flattened_data[0].split(": ", 1)[1]  # Extract the concatenated string
embedding_result = embedding([combined_value])  # Generate embedding
print("Embedding:", embedding_result)

