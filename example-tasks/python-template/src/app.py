import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def entry_point():
    input = request.json
    print("Request:", request)
    print("Input:", input)

    return json.dumps(input)

print("meca-init-done")