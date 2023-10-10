import transformers
from transformers import T5ForConditionalGeneration, T5Tokenizer

model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')

text = input("Enter the text you want to summarize: ")
max_length = 20

input_text = "summarize: " + text
input_ids = tokenizer.encode(input_text, return_tensors='pt')

summary = model.generate(input_ids, max_length=max_length)

summary_text = tokenizer.decode(summary[0], skip_special_tokens=True)
print("Summary:", summary_text)
