from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from data_analysis import getMostCommonPatterns, getLeastCommonPatterns, getMostCommonResponses, getLeastCommonResponses
from chatgui import chatbot_response

app = Flask(__name__)

CORS(app)


@app.route("/", methods=['POST', 'GET'])
@cross_origin()
def indexRoute():
    return chatFunc("abcabc")

@app.route("/chat", methods=['POST'])
@cross_origin()
def chatRoute():
    res = chatbot_response(request.json['message'])
    return  {'res': res}


@app.route("/analytics", methods=['POST'])
@cross_origin()
def analyticsRoute():
    print(request.json['dataSource'])
    dataSource = request.json['dataSource']

    if(dataSource == 'mostCommonResponse'):
        return {'res': getMostCommonResponses()}

    elif(dataSource == 'leastCommonResponse'):
        return {'res': getLeastCommonResponses()}

    elif(dataSource == 'mostCommonPatterns'):
        return {'res': getMostCommonPatterns()}

    elif(dataSource == 'leastCommonPatterns'):
        return {'res': getLeastCommonPatterns()}

    else:
        return {'res': []}

def chatFunc(message): 
    return "test response message"