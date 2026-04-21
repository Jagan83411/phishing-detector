from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words='english')

def extract_email_features(texts):
    return vectorizer.fit_transform(texts)