import pickle

import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('main.html')


@app.route("/ask", methods=['POST'])
def ask():
    parameters = {}
    test = ''
    with open('taskui-data.pickle', 'rb') as handle:
        parameters = pickle.load(handle)
    message = str(request.form['messageText'])
    text = str('{"input":"' + message + '"}')
    parameters["input"] = text
    print(parameters)
    while True:
        if message == "quit":
            exit()
        elif message == "save":
            print("bot_brain.brn")
        else:
            response = requests.get("http://39.108.135.114:8001/simpleMobile/getConversation.sc?", params=parameters)
            data = response.json()
            with open('taskui-data.pickle', 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return jsonify({'status': 'OK', 'answer': data['responce']['show']})


if __name__ == "__main__":
    app.run(debug=True)
