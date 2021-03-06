# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("queryResult").get("action") != "thirukkural":
        return {}
    baseurl = "https://getthirukkural.appspot.com/api/2.0/kural/rnd?appid=gyp31gb8d8thi&format=json"
   #yql_query = makeYqlQuery(req)
    # if yql_query is None:
    #     return {}
    yql_url = baseurl
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    kuralSet = data.get('KuralSet')
    if(kuralSet)is None:
        return{}
    kuralArray = kuralSet.get('Kural')
    if(kuralArray)is None:
        return{}
    kural= kuralArray[0]
    number = kural.get('Number')
    line1 = kural.get('Line1')
    line2 = kural.get('Line2')
    translation= kural.get('Translation')
    speech = line1+line2+translation

    # if (line1 is None) or (line2 is None) or (translation is None):
    #     return {}


    # print(json.dumps(item, indent=4))

    print("Response:")
    print(speech)

    return {

          "fulfillmentText": speech


    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
    #to debug in local environmnet
    # port = 8080
    #
    # app.run(debug=True, port=port, host='0.0.0.0')
