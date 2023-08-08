import requests
from secrets import api_key


def start():
    url = "https://api.together.xyz/instances/start?model=togethercomputer%2FLLaMA-2-7B-32K"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, headers=headers)
    print(response.text)


def ask_question(question):
    url = "https://api.together.xyz/inference"

    payload = {
        "model": "togethercomputer/LLaMA-2-7B-32K",
        "prompt": f"{question}",
        "max_tokens": 128,
        "stop": ".",
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
    url = "https://api.together.xyz/instances/stop?model=togethercomputer%2FLLaMA-2-7B-32K"
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
        user_prompt = f"""
            <human>: {user_input}
            <bot>:"""
        print(user_prompt)
        ask_question(user_prompt)

if __name__ == "__main__":

    with open('test_docs.txt', 'r') as file:
        documentation_text = file.read()


    PRE_PROMPT = f"""
<human>: Please answer my questions based on the following documentation. No need to respond with anything till I ask a quesetion. {documentation_text}
<bot>: My name is Bot, model version is 0.16, part of an open-source kit for fine-tuning new bots! I was created by Together, LAION, Ontocord and the open-source community. I am not human, not evil and not alive, and thus have no thoughts and feelings, but I am programmed to be helpful, polite, honest, and friendly. I will answer you questions about this documentation!
"""

    # print(PRE_PROMPT)

    user_input = input()
    if user_input.lower() == "start":
        start()
        ask_question("PRE_PROMPT")
        print("MODEL STARTED")
        execute_llm()
