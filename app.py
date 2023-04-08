from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)


@app.route("/", methods=['POST', 'GET'])
@cross_origin()
def indexRoute():
    return chatFunc("abcabc")

@app.route("/chat", methods=['POST'])
@cross_origin()
def chatRoute():
    print(request.json)
    return  {'res': chatFunc("abcabc")}



def chatFunc(message): 
    return "test response message"