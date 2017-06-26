import json
import os

from chrome_data import ChromeProvider

import requests
from flask import Flask, Response

app = Flask(__name__)

chrome_data = ChromeProvider()

@app.route('/<url>')
def hello_world(url):
    data = {}
    data["browsers"] = {}
    data["browsers"]["chrome"] = {}
    for os_name, os_builds in chrome_data.all_versions.items():
        os_data = {}
        data["browsers"]["chrome"][os_name] = os_data
        for build_name, build_data in os_builds.items():
            version_data = chrome_data.single_versions[build_data["hash"]]
            os_data[build_name] = version_data[url] if url in version_data else None
    preload_list = json.loads(requests.get("https://hstspreload.org/api/v2/status", params={"domain": url}).text)
    data["preload_list"] = preload_list
    return Response(response=json.dumps(data), mimetype="application/json")

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
