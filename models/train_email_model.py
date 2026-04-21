import os

spam_dir = 'data/emails/spam'
ham_dir = 'data/emails/easy_ham'

texts = []
labels = []

# spam = 1
for file in os.listdir(spam_dir):
    with open(os.path.join(spam_dir, file), encoding='latin-1') as f:
        texts.append(f.read())
        labels.append(1)

# ham = 0
for file in os.listdir(ham_dir):
    with open(os.path.join(ham_dir, file), encoding='latin-1') as f:
        texts.append(f.read())
        labels.append(0)