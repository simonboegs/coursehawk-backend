from nltk.corpus import wordnet

syns = wordnet.synsets("good")
print(syns)

for s in syns:
    for l in s.lemmas():
        print(l.name())
