import requests
from secrets import api_key
import together

model = "llama-2-7b-chat"
CONTEXT_STORED = 2
stored_messages = []
def start():
    url = f"https://api.together.xyz/instances/start?model=togethercomputer%2F{model}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, headers=headers)


def ask_question(question):
    url = "https://api.together.xyz/inference"
    question = format_prompt(question)

    payload = {
        "model": f"togethercomputer/{model}",
        "prompt": f"{question}",
        "max_tokens": 256,
        "stop": "<|END|>",
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200 and "choices" in response.json()["output"]:
            print(response.json()["output"]["choices"][0]["text"])
            if len(stored_messages) < CONTEXT_STORED:
                stored_messages.append(question)
            else:
                stored_messages.pop(0)
                stored_messages.append(question)
    except requests.exceptions.RequestException:
        stop()
        

def stop():
    url = f"https://api.together.xyz/instances/stop?model=togethercomputer%2F{model}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    requests.post(url, headers=headers)
    print("EXECUTION STOPPED")

def execute_llm():
    while True:
        user_input = input()
        if user_input.lower() == "stop":
            stop()
            return
        ask_question(user_input)
def format_prompt(question):
    with open('test_docs.txt', 'r') as file:
       documentation_text = file.read()
    prompt = f"Context: {documentation_text}"
    for message in stored_messages:
        prompt += f"Here is a previous message from this thread to guide you, this is not the actual question: {message}"
    prompt += f"Question: {question}<|END|>"
    return prompt

if __name__ == "__main__":
   documentation_text = ""
   PRE_PROMPT = f"""
    Please answer my questions based on the following documentation. No need to respond with anything till I ask a question. {documentation_text}
    """
   with open('test_docs.txt', 'r') as file:
       documentation_text = file.read()
   start()
   print("STARTED")
   ask_question("how do I set a source filter to basic mode in appian?")
   ask_question("how do I set a source filter using expression mode in appian?")
   stop()
