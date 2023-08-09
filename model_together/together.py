import requests
from secrets import api_key

model = "llama-2-7b-chat"
def start():
    url = f"https://api.together.xyz/instances/start?model=togethercomputer%2F{model}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, headers=headers)


def ask_question(question):
    url = "https://api.together.xyz/inference"

    payload = {
        "model": f"togethercomputer/{model}",
        "prompt": f"{question}",
        "max_tokens": 512,
        "stop": "<human>",
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
        if response.status_code == 200:
            print(response.json()["output"]["choices"][0]["text"])
    except requests.exceptions.RequestException:
        stop()


def stop():
    url = f"https://api.together.xyz/instances/stop?model=togethercomputer%2F{model}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, headers=headers)
    print(response.text)
    print("EXECUTION STOPPED")

def execute_llm():
    while True:
        user_input = input()
        if user_input.lower() == "stop":
            stop()
            return
        ask_question(user_input)

if __name__ == "__main__":
    documentation_text = ""
    with open('test_docs.txt', 'r') as file:
        documentation_text = file.read()


    PRE_PROMPT = f"""
    Please answer my questions based on the following documentation. No need to respond with anything till I ask a question. {documentation_text}
    """

    # print(PRE_PROMPT)

    user_input = input()
    if user_input.lower() == "start":
        start()
        ask_question(PRE_PROMPT)
        print("MODEL STARTED")
        execute_llm()
