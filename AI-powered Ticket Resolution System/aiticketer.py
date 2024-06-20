

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load data
df = pd.read_excel('Task (project.task) copy.xlsx')

# Preprocess text
df['title_preprocessed'] = df['Title']
df['description_preprocessed'] = df['Description']

# Load NLP model
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Encode data
input_encoding = model.encode(['your input sentence'])
df_encodings = model.encode(df[['title_preprocessed', 'description_preprocessed']].values.tolist())

# Calculate cosine similarity
similarities = np.dot(input_encoding, df_encodings.T).squeeze()

# Sort by similarity (descending)
top_indices = np.argsort(similarities)[::-1]

# Display results
for i in top_indices[:5]:  # Adjust 5 to the desired number of results
    title, assignee, description = df.iloc[i]
    print(f"Similarity: {similarities[i]:.4f}\nTitle: {title}\nAssignee: {assignee}\nDescription: {description}\n")