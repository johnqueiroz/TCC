import requests
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet

login = "johnrf"
senha = "Etcfcsgo1.6$mot"

## ID da CR que será usada no script
cr = "IKSWS-177710"
params = "fields=*all"

## URL base para verificação na API
url = "https://idart.mot.com/rest/api/latest/issue/"

## Request feito
request = requests.get(url+cr, auth=(login, senha), params=params)

## Transformando o objeto em json para logo mais observar seus campos
url_json = request.json()

## Campos do json que serão utilizados
title = url_json['fields']['summary']
description = url_json['fields']['description']

## Texto que será utilizado para validação
text = description

#palavras-chave
keywords = ["Google Assistant", "Headset", "Bluetooth", "activated", "Ok Google"]

# Sinônimos das palavras-chave
synonyms = {}
for keyword in keywords:
    synonyms[keyword] = []
    for syn in wordnet.synsets(keyword):
        for lemma in syn.lemmas():
            synonyms[keyword].append(lemma.name())


tokens = nltk.word_tokenize(text)

# Remove as stopwords
filtered_tokens = [token for token in tokens if token not in stopwords.words("english")]

# Contador de palavras-chave
keyword_count = 0

# Verifica se o texto possui alguma das palavras-chave ou sinônimos
for token in filtered_tokens:
    if token in keywords or token in synonyms[keyword]:
        keyword_count += 1

# Resultado da verificação
if keyword_count >= 2:
    print("A CR está relacionada a Google Assistant com bluetooth")
else:
    print("A CR não está relacionada a Google Assistant com bluetooth")
