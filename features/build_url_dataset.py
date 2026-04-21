import pandas as pd
import os
from features.url_features import extract_url_features

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

phish_path = os.path.join(BASE_DIR, 'data', 'urls', 'phishing_urls.csv')
legit_path = os.path.join(BASE_DIR, 'data', 'urls', 'legit_urls.csv')

phish_df = pd.read_csv(phish_path, encoding='utf-16')
legit_df = pd.read_csv(legit_path, encoding='utf-16')

phish_df.columns = phish_df.columns.str.strip().str.lower()
legit_df.columns = legit_df.columns.str.strip().str.lower()

phish_urls = phish_df['url']
legit_urls = legit_df['url']

data = []

# phishing → label 1
for url in phish_urls:
    f = extract_url_features(str(url))
    f['label'] = 1
    data.append(f)

# legit → label 0
for url in legit_urls:
    f = extract_url_features(str(url))
    f['label'] = 0
    data.append(f)

df = pd.DataFrame(data)
df.to_csv(os.path.join(BASE_DIR, 'data', 'processed', 'url_dataset.csv'), index=False)

print("Dataset ready!")