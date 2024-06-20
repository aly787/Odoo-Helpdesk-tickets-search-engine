import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# get the strings of both title and description
#Find similarity of title and description

#For the title
def find_similar_Titles(xlsx_file, input_sentence, top_n=5):
    # Load the XLSX file into a DataFrame
    df = pd.read_excel(xlsx_file)

    # Replace NaN values in the 'Title' column with empty strings
    df['Title'].fillna('', inplace=True)

    # Extract the 'Title' column from the DataFrame
    Titles = df['Title']

    # Combine the input sentence with the existing Titles
    Titles = pd.concat([Titles, pd.Series([input_sentence])], ignore_index=True)

    # Initialize the TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Transform the Titles into TF-IDF vectors
    tfidf_matrix = tfidf_vectorizer.fit_transform(Titles)

    # Calculate cosine similarities between the input sentence and all Titles
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Get the indices of the most similar Titles
    similar_indices = cosine_similarities.argsort()[0][-top_n - 1:-1]

    # Retrieve the top N most similar Titles
    similar_descriptions = df.iloc[similar_indices]['Title']

    return similar_descriptions

#For the description
def find_similar_descriptions(xlsx_file, input_sentence, top_n=5):
    # Load the XLSX file into a DataFrame
    df = pd.read_excel(xlsx_file)

    # Replace NaN values in the 'Title' column with empty strings
    df['Description'].fillna('', inplace=True)

    # Extract the 'Description' column from the DataFrame
    Descriptions = df['Description']

    # Remove HTML tags from the input sentence
    input_sentence = input_sentence.replace('<[^>]*>', '')

    # Combine the input sentence with the existing Description
    Descriptions = pd.concat([Descriptions, pd.Series([input_sentence])], ignore_index=True)

    # Initialize the TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Transform the Description into TF-IDF vectors
    tfidf_matrix = tfidf_vectorizer.fit_transform(Descriptions)

    # Calculate cosine similarities between the input sentence and all Description
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Get the indices of the most similar Description
    similar_indices = cosine_similarities.argsort()[0][-top_n - 1:-1]

    # Retrieve the top N most similar Description
    similar_descriptions = df.iloc[similar_indices]['Title']

    return similar_descriptions

# Input parameters
xlsx_file = 'Task (project.task).xlsx'  # Replace with the path to your XLSX file
input_title = "Unable to download database backup"
input_description = "Missing record. record does not exist or has been deleted"
top_n = 5

# Find and print the top N most similar Titles
similar_Titles = find_similar_Titles(xlsx_file, input_title, top_n)
similar_Description = find_similar_descriptions(xlsx_file, input_description, top_n)

#Print top titles
print("Top", top_n, "similar Titles:")
for i, Title in enumerate(similar_Titles, 1):
    print(f"{i}. {Title}")

#Print top descriptions (Title's of top descriptions)
print("Top", top_n, "similar descriptions:")
for i, Description in enumerate(similar_Description, 1):
    print(f"{i}. {Description}")