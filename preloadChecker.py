import json
import os

from chrome_data import ChromeProvider
from firefox_data import FirefoxProvider

import requests
from flask import Flask, Response, send_file

app = Flask(__name__)

chrome_data = ChromeProvider()
FF = FirefoxProvider()
@app.route('/api/<url>')
def hello_world(url):
    data = {}
    data["browsers"] = {}
    data["browsers"]["chrome"] = {}
    for os_name, os_builds in chrome_data.all_versions.items():
        os_data = {}
        data["browsers"]["chrome"][os_name] = os_data
        for build_name, build_data in os_builds.items():
            version_data = chrome_data.single_versions[build_data["hash"]]
            os_data[build_name] = {}
            os_data[build_name]["state"] = version_data[url] if url in version_data else None
            major, minor, build, patch = build_data["build"].split(".")
            os_data[build_name]["version"] = {"major": major, "minor": minor, "build": build, "patch": patch}

    data["browsers"]["firefox"] = {}
    data["browsers"]["firefox"]["desktop"] = {}
    for item in FF.VERSIONS:
        d = {}
        data["browsers"]["firefox"]["desktop"][item] = d
        d["state"] = url in FF.items[item]

    preload_list = json.loads(requests.get("https://hstspreload.org/api/v2/status", params={"domain": url}).text)
    data["preload_list"] = preload_list
    return Response(response=json.dumps(data), mimetype="application/json")


@app.route("/")
def index():
    return send_file("static/index.html")

@app.route("/<path>")
def resultsPage(path):
    return send_file("static/index.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)