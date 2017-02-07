import os
import json
import base64
from azure.storage.blob import BlockBlobService

from utils import readJSONFile

account_info = readJSONFile("private/azure_account.json")
service = BlockBlobService(account_name = account_info["account_name"], account_key = account_info["account_key"])

dump_dir = "dump"
prefix = "dev-"

try: os.makedirs(os.path.join(dump_dir, "sessions"))
except: pass
try: os.makedirs(os.path.join(dump_dir, "exports"))
except: pass

for blob in service.list_blobs(prefix + 'sessions'):
    print "sessions/" + blob.name
    service.get_blob_to_path(prefix + "sessions", blob.name, os.path.join(dump_dir, "sessions", blob.name))

for blob in service.list_blobs(prefix + 'exports'):
    print "exports/" + blob.name
    path = os.path.join(dump_dir, "exports", blob.name)
    service.get_blob_to_path(prefix + "exports", blob.name, path)
    with open(path, "rb") as f:
        content = json.loads(f.read().decode("utf-8"))
        dataurl = content["imageDataURL"]
        dataurl_prefix, imageDataBase64 = dataurl.split(",")
        imageData = base64.b64decode(imageDataBase64)
        if dataurl_prefix.startswith("data:image/png"):
            with open(path + ".png", "wb") as fo:
                fo.write(imageData)
        if dataurl_prefix.startswith("data:image/svg+xml"):
            with open(path + ".svg", "wb") as fo:
                fo.write(imageData)
        if dataurl_prefix.startswith("data:image/gif"):
            with open(path + ".gif", "wb") as fo:
                fo.write(imageData)

        with open(path + ".state.json", "wb") as fo:
            fo.write(json.dumps(content["state"]).encode("utf-8"))
