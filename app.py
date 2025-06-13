from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load and preprocess the dataset
df = pd.read_csv('books_enriched.csv').head(2000)
df['title'] = df['title'].astype(str).str.lower()
df['genres'] = df['genres'].astype(str).str.lower()
df['authors'] = df['authors'].astype(str).str.lower()

# TF-IDF and cosine similarity for title-based recommendations
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['title'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Helper to find book index
def get_index_from_title(title):
    matches = df[df['title'].str.contains(title.lower(), na=False)]
    if not matches.empty:
        return matches.index[0]
    return None

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Search route with filter (AI-enhanced for title search)
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    filter_by = request.args.get('filter_by', 'title')

    if not query or filter_by not in ['title', 'author', 'genre']:
        return jsonify({'error': 'Invalid query or filter_by'}), 400

    if filter_by == 'title':
        idx = get_index_from_title(query)
        if idx is None:
            return jsonify({'error': 'Book not found'}), 404
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_indices = [i[0] for i in sim_scores[1:4]]
        results = df.iloc[top_indices]

    elif filter_by == 'author':
        results = df[df['authors'].str.contains(query, na=False)].head(3)

    elif filter_by == 'genre':
        results = df[df['genres'].str.contains(query, na=False)].head(3)

    if results.empty:
        return jsonify({'error': 'No matches found'}), 404

    return jsonify(results[['title', 'authors', 'genres', 'average_rating']].to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
