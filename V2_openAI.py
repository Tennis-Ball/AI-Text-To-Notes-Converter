import openai
from transformers import GPT2Tokenizer


with open("OPENAI_API_KEY.txt", "r") as k:
    openai.api_key = k.readline()
k.close()

with open("example_passage3.txt", "r", encoding="utf-8") as f:
    text = f.read()
f.close()

prompt = f'Please indentify each heading with a * and underneath summarize its corresponding information in factual statements in less than 4 sentences: "{text}"'
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
number_of_tokens = len(tokenizer(prompt)['input_ids'])

completion = openai.Completion.create(engine="text-davinci-003", max_tokens=4096-number_of_tokens, prompt=prompt)
print(completion.choices[0].text)
