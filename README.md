# AI-POC
An AI-POC designed to assist team POC's, making workflows more efficient and reducing load on team POCs.

# System Flow/Design
1. Question is asked by User
2. Run Vector Similarity Search on question and all of Appian Docs to find the chunk of text with the most relevant content.
3. Format a Large Language Model prompt with the context, chat history, and most recent question.
4. Pass the prompt to the Meta Llama2-7B large language model.
5. Respond with the Models response and Appian Documentation source.

## Why

### Context Approach
We decided against fine tuning the model on Appian documentation for security purposes. This allows this approach to be applied to searching Appian Internal Documentation in the future. By providing all information as model context, the model takes a reading comprehension approach and answers the user’s question using the context provided. The context information is not physically stored in the models parameters ensuring data security.

### Model Selection
We wanted to use open source language models for the purpose of security and transparency. With an open source model, Appian can host the model and keep all data internal.

The original intention was to use [LLaMA-2-7B-32K](https://huggingface.co/togethercomputer/LLaMA-2-7B-32K), a language model with a context size of 32 thousand tokens (roughly 24,000 words). For perspective, Open-AI’s Chat GPT has a context of 8,000 tokens (~6000 words).
This large context is achieved by modifying the existing Llama2 model using a technique known as [position interpolation](https://huggingface.co/papers/2306.15595). However, this model needs to be finetuned for chat purposes which could not be done with the resources allotted for the hackathon.

We resorted to using a chat fine tuned version of the regular [Llama2 model](https://huggingface.co/meta-llama/Llama-2-7b-chat) with a context size of 4,000 tokens. This can easily be replaced with larger context models in the future.

### Vector Similarity
Due to the model context limitations, we need to narrow down Appian Documentation to just the section that has content most similar to the question the user asked. We used a technique known as vector similarity search to accomplish this.

We use the [Count Vectorizer](https://www.geeksforgeeks.org/using-countvectorizer-to-extracting-features-from-text/) algorithm quickly extract semantic meaning in real time from the user question and Appian documentation and store them as embedding vectors. We can then use [cosine similarity](https://www.pinecone.io/learn/vector-similarity/) between the user question vector and the Appian documentation vectors to find the section of Appian Docs which is most relevant to the user question. This is then fed into the Language Model as context.

# Converter Script
To run the converter script, you will need to install the following depedencies:
 - `pip install bs4`

 Run the converter script from the `./src` directory by running `python3 converter.py`.
 You can change the output directory by changing the `outputDir` variable of the script.
