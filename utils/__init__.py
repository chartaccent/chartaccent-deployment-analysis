import json

def readJSONFile(path):
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))