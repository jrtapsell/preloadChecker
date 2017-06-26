import json
import os
from base64 import b64decode

import requests

class ChromeProvider(object):
    VERSIONS_URL = "https://omahaproxy.appspot.com/all.json"
    SINGLE_VERSION_URL \
        = "https://chromium.googlesource.com/chromium/src/+/%s/net/http/transport_security_state_static.json?format=TEXT"

    CACHE_PATH = "preloadChecker/cache"
    DATA_PATH = CACHE_PATH + "/data"
    VERSIONS_FILE = CACHE_PATH + "/versions.json"

    all_versions = {}
    single_versions = {}


    def load_versions(self):
        if os.path.isfile(self.VERSIONS_FILE):
            with open(self.VERSIONS_FILE) as cache_file:
                return json.load(cache_file)
        else:
            data = requests.get(self.VERSIONS_URL).text
            json_data = json.loads(data)
            cleaned_data = {}
            for item in json_data:
                data_object = {}
                cleaned_data[item["os"]] = data_object
                for version in item["versions"]:
                    if "chromium_commit" not in version:
                        continue
                    hash = version["chromium_commit"]
                    version_data = {}
                    data_object[version["channel"]] = version_data
                    version_data["hash"] = hash
                if len(data_object) == 0:
                    del cleaned_data[item["os"]]

            with open(self.VERSIONS_FILE, "w") as cache_file:
                json.dump(cleaned_data, cache_file)
                return cleaned_data


    def load_single_version(self, hash):
        hash_path = self.DATA_PATH + "/" + hash + ".json"
        if os.path.isfile(hash_path):
            with open(hash_path) as cache_file:
                return json.load(cache_file)
        else:
            url = self.SINGLE_VERSION_URL % hash
            request = requests.get(url)
            data = b64decode(request.text).decode("UTF8")
            cleaned_data = ""
            for line in data.split("\n"):
                stripped = line.strip()
                if stripped[:2] == ("//") :
                    continue
                if stripped == "":
                    continue
                cleaned_data += line + "\n"
            data = cleaned_data
            json_data = json.loads(data)

            cleaned_data = {}
            for item in json_data["entries"]:
                cleaned_data[item["name"]] = item
            with open(hash_path, "w") as cache_file:
                json.dump(cleaned_data, cache_file)
                return cleaned_data


    def prearm_cache(self):
        self.all_versions = self.load_versions()
        for os in self.all_versions.values():
            for branch in os.values():
                self.single_versions[branch["hash"]] = self.load_single_version(branch["hash"])

    def __init__(self):
        if not os.path.exists(self.CACHE_PATH):
            os.mkdir(self.CACHE_PATH)
        if not os.path.exists(self.DATA_PATH):
            os.mkdir(self.DATA_PATH)
        self.prearm_cache()