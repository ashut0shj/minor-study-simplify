from textrazor import TextRazor
c
client = TextRazor("0c74699f63a2ed1f5e10ed2b17fbb78dfeedc6d1f11ed6a1e8e5a7d0", extractors=["entities"])
response = client.analyze(text)
for entity in response.entities():
    print(entity)