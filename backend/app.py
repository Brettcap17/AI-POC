from flask import Flask, jsonify, request
from vss_utils.similarity import vss
from model_utils.model import LlamaThread
from vss_utils.similarity import vss
import model_utils.model as model


app = Flask(__name__)
model = LlamaThread("llama-2-7b-chat")

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
    if context is None:
        result = {'message': "I am sorry, I cannot understand your question. Please try rephrasing.", 'source': ""}
        return jsonify(result)

    # Get Model Response
    model.start()
    output = model.ask_question(text_input, context[1])
    result = {'message': output, 'source': context[0]}
    return jsonify(result)


@app.route('/clear_history', methods=['POST'])
def clear_history():
    model.clear_chat_history()

    return {'message': "Cleared"}

if __name__ == '__main__':
    model.start()
    app.run(port=5000, debug=True)
