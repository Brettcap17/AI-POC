from flask import Flask, jsonify, request
from similarity import vss


app = Flask(__name__)

@app.route('/hello')
def hello():
    return "Hello"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
