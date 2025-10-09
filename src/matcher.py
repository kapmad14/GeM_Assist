import pandas as pd, json, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_tender(tender_path, catalogue_path, top_k=5):
    # load tender JSON
    tender = json.load(open(tender_path))
    tender_text = " ".join([p["description"] for p in tender["products"]])

    # load catalogue
    cat = pd.read_csv(catalogue_path)
    cat["text"] = cat["description"] + " " + cat["hsn"].astype(str)

    # TF-IDF similarity
    vect = TfidfVectorizer(stop_words="english", max_features=2000)
    tfidf = vect.fit_transform(cat["text"])
    tender_vec = vect.transform([tender_text])
    scores = cosine_similarity(tender_vec, tfidf).flatten()

    # price & state filter (simple)
    matches = []
    for idx, score in enumerate(scores):
        row = cat.iloc[idx]
        matches.append({
            "sku": row.sku,
            "score": round(score, 3),
            "description": row.description,
            "price_ok": True,  # TODO: real price check
            "state_ok": True   # TODO: real state check
        })
    matches = sorted(matches, key=lambda x: x["score"], reverse=True)[:top_k]
    return matches