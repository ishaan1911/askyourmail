import json
from embeddings import generate_email_embeddings

# Load the dataset (assuming it's a JSON file)
with open("dataset1.json", "r") as file:
    dataset = json.load(file)

# Directly assign the emails from the dataset (since it's a list)
emails = dataset

# Generate email embeddings
email_embeddings = generate_email_embeddings(emails)

# Optionally, print or inspect the embeddings
print(email_embeddings)




