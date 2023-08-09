from flask import Flask, jsonify, request
from vss_utils.similarity import vss
import model_utils.model


app = Flask(__name__)

# Testing Endpoint
@app.route('/hello')
def hello():
    return "Hello"



@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.json
    text_input = data['text']
    print(text_input)
    # Process the text_input here
    result = {'message': 'Text processed successfully'}
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
