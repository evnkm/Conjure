import json
import pandas as pd

# dataset = json.dumps("./demo_dataset.json")

with open("./demo_dataset_600.json", "r") as f: 
    dataset = json.loads(f.read())

files = []
descriptions = []
ids = []
cnt = 1
for filename, desc in dataset.items(): 
    ids.append(cnt)
    files.append(filename)
    descriptions.append(desc)
    cnt += 1

dataset_dict = {'id': ids, 'filename': files, 'description': descriptions}
df = pd.DataFrame.from_dict(dataset_dict)
df.to_csv("./demo-dataset_600.csv")