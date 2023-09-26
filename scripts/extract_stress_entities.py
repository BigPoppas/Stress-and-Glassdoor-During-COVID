import os
import json
import pandas as pd

# MED-DL is a tool for extracting medical entities, disorders and diseases, from text.
# The official MED-DL reposetory with the source code is available at:
# https://github.com/sanja7s/MED-DL - KUDOS to Sanja and her team!
from MEDDL import meddl 

# Extract medical-related entities from the provided review
def extract_stress_entities(review):
    result = extractor.extract(review)
    entities = result.get("entities", None)

    return entities

# Format the extracted entities into a dictionary format
def get_results(entities) -> dict:
    dic = {}

    if entities is None: return None
    
    for entity in entities:
        text = entity.get("text", None)
        label = str(entity.get("labels", None))

        if text is None or label is None: return None
        
        dic[f"{text}"] = 1
    
    return dic

# Combine results from multiple extractions / reviews
def combine_results(results):
    output = {}

    for result in results:
        if result is None: continue
        if not isinstance(result, dict): continue

        for key, value in result.items():
            output[key] = output.get(key, 0) + value

    return output

# Saves the combined results to a JSON file
def write_to_file(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    # Initialize the MED-DL entity extractor with the AMT model
    model_name = "AMT"
    extractor = meddl.MedDLEntityExtractor(model_name)

    # Specify the path to the CSV file containing the Glassdoor reviews
    path = os.path.join("d:/", "Research Project", "Data")
    fname = "reviews.csv"
    fpath = os.path.join(path, fname)

    # Load the Glassdoor reviews into a Pandas DataFrame
    reviews = pd.read_csv(fpath)
    reviews = reviews[["pros", "cons", "summary"]]
    reviews.dropna(inplace=True)

    # Extract medical-related entities from the summary column of each review
    entities_summary = reviews["summary"].apply(lambda review: extract_stress_entities(review))

    # Convert the extravted entity/ies into a dictionary format
    results = entities_summary.apply(lambda entities: get_results(entities))
    
    # Combine the results to get a dictionary of all medical metnions with their counts
    stress_mentions = combine_results(results)

    # Save the final dictionary of medical mentions to a JSON file
    fjson = os.path.join(path, "medical_entities.json")
    write_to_file(fjson, stress_mentions)