import os
import requests

class FirefoxProvider(object):
    CACHE_PATH = "/tmp/cache"
    VERSIONS = [
        "mozilla-beta",
        "mozilla-release"
    ]
    def __init__(self):
        self.items = {}
        if not os.path.exists(self.CACHE_PATH):
            os.mkdir(self.CACHE_PATH)
        if not os.path.exists(self.CACHE_PATH + "/firefox/"):
            os.mkdir(self.CACHE_PATH + "/firefox/")
        for i in self.VERSIONS:
            current = {}
            self.items[i] = current
            lines = [x.strip() for x in self.get_release(i)]
            start = lines.index("%%")
            lines = lines[start+1:]
            end = lines.index("%%")
            lines = lines[:end]
            for l in lines:
                current[l.split(",")[0]] = True


    def get_release(self, release):
        cacheFile = self.CACHE_PATH + "/firefox/" + release
        url = "https://hg.mozilla.org/releases/" + release + "/raw-file/tip/security/manager/ssl/nsSTSPreloadList.inc"

        if os.path.exists(cacheFile):
            with open(cacheFile, "r") as cached:
                return cached.readlines()
        else:
            lines = requests.get(url).text
            with open(cacheFile, "w") as cached:
                cached.write(lines)
            return lines


