from flask import Flask, render_template
from pyngrok import ngrok
from modules.request_bin import RequestBin


__author__ = "b3liott"


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', ngrok=public_url, bins=[RequestBin('Item 1', 1), RequestBin('Item 2', 2), RequestBin('Item 3', 3)])


if __name__ == '__main__':
    # Start ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f" * ngrok tunnel \"{public_url}\"")
    
    # Start Flask server
    app.run(port=5000)
