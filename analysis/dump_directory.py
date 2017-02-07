import os
import json

from utils import readJSONFile

class DumpDirectory:
    def __init__(self, root):
        self.root = root

    def sessions(self):
        for root, dirs, files in os.walk(os.path.join(self.root, "sessions")):
            for file in files:
                if not file.endswith(".json"): continue
                path = os.path.join(root, file)
                content = readJSONFile(path)
                yield content

    def exports(self):
        for root, dirs, files in os.walk(os.path.join(self.root, "exports")):
            for file in files:
                if not file.endswith(".json"): continue
                path = os.path.join(root, file)
                content = readJSONFile(path)
                yield content
