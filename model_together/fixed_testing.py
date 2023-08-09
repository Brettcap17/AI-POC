import requests
from secrets import api_key
import together


model = "llama-2-7b-chat"
CONTEXT_STORED = 5
stored_messages = []


def start():
    url = f"https://api.together.xyz/instances/start?model=togethercomputer%2F{model}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, headers=headers)


def stop():
    url = f"https://api.together.xyz/instances/stop?model=togethercomputer%2F{model}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    requests.post(url, headers=headers)
    print("EXECUTION STOPPED")


def ask_question(question):
    url = "https://api.together.xyz/inference"

    prompt = format_prompt(question)

    payload = {
        "model": f"togethercomputer/{model}",
        "prompt": f"{prompt}",
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

            answer = response.json()["output"]["choices"][0]["text"]

            # Try to adjust context size dynamically
            if len(stored_messages) > CONTEXT_STORED:
                stored_messages.pop(0)
            stored_messages.append((question, answer))


            return answer
        else :
            print(response.json()["output"])

    except requests.exceptions.RequestException as e:
        print("EXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTIONEXCEPTION")
        stop()



def format_prompt(question):
    with open('test_docs.txt', 'r') as file:
       documentation_text = file.read()
    prompt = f"Answer questions based on this context:\n{documentation_text}"

    prompt += "\n\nThe following is the chat history:\n"
    for (question_past, answer) in stored_messages:

        prompt += f"Question: {question_past}\n"
        prompt += f"Answer: {answer}\n"

    prompt += f"Question: {question}<|END|>"

    return prompt.strip()


if __name__ == "__main__":

    start()

    while True:
        output = ask_question(input())
        print(output)


    stop()
