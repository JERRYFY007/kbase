import pickle

import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('main.html')


@app.route("/ask", methods=['POST'])
def ask():
    text = {}
    with open('taskui-data.pickle', 'rb') as handle:
        text = pickle.load(handle)
    message = str(request.form['messageText'])
    text['input'] = str(message)
    parameters = "input=" + str(text)
    print("Parameters", parameters)
    while True:
        if message == "quit":
            print("Quit!")
            exit()
        elif message == "save":
            print("save")
        else:
            response = requests.get("http://39.108.135.114:8001/simpleMobile/getConversation.sc?", params=parameters)
            data = response.json()
            print("Recive:", data)
            with open('taskui-data.pickle', 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return jsonify({'status': 'OK', 'answer': data['responce']['show']})


if __name__ == "__main__":
    app.run(debug=True)
