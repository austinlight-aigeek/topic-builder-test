from sentence_transformers import SentenceTransformer
import os

# Define the directory where you want to store the model
model_path = "./models/all-MiniLM-L6-v2"

# Check if the model exists locally, if not, download it
if not os.path.exists(model_path):
    # Download and save the model to the specified directory
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    model.save(model_path)
else:
    # Load the model from the local directory
    model = SentenceTransformer(model_path)

# Encode your sentences
sentences = ["This is an example sentence", "Each sentence is converted"]
embeddings = model.encode(sentences)
print(embeddings)
