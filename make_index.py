import json 

inds = list(range(5000))

with open('index.json', 'w') as f:
    json.dump(inds, f)