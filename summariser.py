from transformers import PegasusForConditionalGeneration , PegasusTokenizer
model_name = "google/pegasus-xsum"
pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)
tokens = pegasus_tokenizer(example_text, truncation = True , padding = "longest" , return_tensors = "pt")
tokens
