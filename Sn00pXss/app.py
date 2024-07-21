from flask import Flask, request, render_template
from pyngrok import ngrok
from Sn00pXss.modules.request_bin.request_bin import RequestBin


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', ngrok=public_url, bins=[RequestBin('Item 1', 1), RequestBin('Item 2', 2), RequestBin('Item 3', 3)])


@app.route('/request_bin', methods=['GET'])
def receive_request():
    # Print headers and all request data
    print("Headers:")
    for header, value in request.headers:
        print(f"{header}: {value}")
    
    print("\nRequest Data:")
    print(request.data)
    
    return "Request received!", 200

if __name__ == '__main__':
    # Start ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f" * ngrok tunnel \"{public_url}\"")
    
    # Start Flask server
    app.run(port=5000)
