from flask import Flask, jsonify, request
from vss_utils.similarity import vss
import model_utils.model as model


app = Flask(__name__)

# Testing Endpoint
@app.route('/hello')
def hello():
    return "Hello"


@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.json
    text_input = data['text']
    
    # Get Context
    chat_history = model.get_chat_history()
    chat_history += f"{text_input}\n"
    context = vss(chat_history, "output_full")

    # Get Model Response
    model.start()
    output = model.ask_question(text_input, context[1])
    result = {'message': output, 'source': context[0]}
    return jsonify(result)


# Need to create a button which calls this!
@app.route('/clear_history', methods=['POST'])
def clear_history():
    model.clear_chat_history()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
