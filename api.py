import textrazor
textrazor.api_key='cafaaa69e11162fcc743c8ba91c91cfd3274cd874c56faa99c8a0431' #the API key, which will hit the URL and provide the functionality for NER.
def ner(text):
    client = textrazor.TextRazor(extractors=["entities", "topics"])
    response = client.analyze(text)
    return response