from flask import Flask, render_template, request
from pyngrok import ngrok
from models import RequestBin
from datetime import datetime


__author__ = "b3liott"


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', ngrok=public_url, bins=bins)


@app.route('/bin', methods=['GET'])
def bin():
    # Add new bin
    now = datetime.now()
    args = [f"{key}: {value}" for key, value in request.args.items()]
    bins.append(RequestBin(f'New request at {now.hour}:{now.minute}:{now.second}', args))
    
    return {"status": "ok"}



if __name__ == '__main__':
    # Start ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f" * ngrok tunnel \"{public_url}\"")
    
    global bins
    bins: list[RequestBin] = []

    # Start Flask server
    app.run(port=5000)
