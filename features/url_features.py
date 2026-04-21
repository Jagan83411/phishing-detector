import re
import tldextract

def extract_url_features(url):
    features = {}

    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_slashes'] = url.count('/')
    features['has_https'] = 1 if 'https' in url else 0

    # IP address detection
    features['has_ip'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

    # @ symbol
    features['has_at'] = 1 if '@' in url else 0

    # double slash redirect
    features['has_double_slash'] = 1 if '//' in url[7:] else 0

    # domain info
    ext = tldextract.extract(url)
    domain = ext.domain

    features['domain_length'] = len(domain)
    features['num_subdomains'] = len(ext.subdomain.split('.')) if ext.subdomain else 0

    suspicious_words = ['login','verify','secure','account','bank','update','free']
    features['suspicious_words'] = sum(word in url.lower() for word in suspicious_words)

    return features