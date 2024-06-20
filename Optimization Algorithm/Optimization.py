import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to find the top N most similar Titles
def find_similar_Titles(xlsx_file, input_title, top_n=5):
    # Load the XLSX file into a DataFrame
    df = pd.read_excel(xlsx_file)

    # Replace NaN values in the 'Title' column with empty strings
    df['Title'].fillna('', inplace=True)
    print(type(df['Description']))
    # Extract the 'Title' column from the DataFrame
    Titles = df['Title']

    # Combine the input sentence with the existing Titles
    Titles = pd.concat([Titles, pd.Series([input_title])], ignore_index=True)

    # Initialize the TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Transform the Titles into TF-IDF vectors
    tfidf_matrix = tfidf_vectorizer.fit_transform(Titles)

    # Calculate cosine similarities between the input sentence and all Titles
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Get the indices of the most similar Titles
    similar_indices = cosine_similarities.argsort()[0][-top_n - 1:-1]

    # Retrieve the top N most similar Titles
    similar_Titles = df.iloc[similar_indices]['Title']

    return similar_Titles

# Input parameters
xlsx_file = 'Task (project.task).xlsx'  # Replace with the path to your XLSX file
input_title = "[l10n_ar] Error Code:600 when trying to create an invoice"
top_n = 5
# Find and print the top N most similar Titles
similar_Titles = find_similar_Titles(xlsx_file, input_title, top_n)
print("Top", top_n, "similar Titles:")
for i, Title in enumerate(similar_Titles, 1):
    print(f"{i}. {Title}")

