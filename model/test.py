import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("togethercomputer/LLaMA-2-7B-32K")
model = AutoModelForCausalLM.from_pretrained("togethercomputer/LLaMA-2-7B-32K")


while True:
    input_context = input()
    input_ids = tokenizer.encode(input_context, return_tensors="pt")
    output = model.generate(input_ids, max_length=128, temperature=0.7)
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(output_text)
