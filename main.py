import json

FILE_NAME = 'test.json'

with open(FILE_NAME, 'r') as file:
    data = json.load(file)

for i in data:
    print("\n\n", i)