phishing_db = set()

def add_url(url):
    phishing_db.add(url)

def check_url(url):
    return url in phishing_db