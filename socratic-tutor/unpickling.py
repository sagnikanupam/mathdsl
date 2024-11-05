import pickle

with open('best-config/lemma/A2.pkl', 'rb') as f:
    A2 = pickle.load(f)
    print(A2)