import json
import string
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein

nltk.download('stopwords')

# Carregando os arquivos JSON
with open("resources/test_cases.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)

with open("resources/issues.json", "r", encoding="utf-8") as file:
    issues = json.load(file)

# Remove stopwords e pontuações
stop_words = set(stopwords.words("english"))
punctuations = string.punctuation

def remove_stopwords_punctuations(text):
    if text:
        text = text.lower()
        text = ''.join(word for word in text if word not in punctuations)
        text = ' '.join(word for word in text.split() if word not in stop_words)
        return text
    return ""


# Aplica a função de remoção em cada campo dos test_cases e issues
for case in test_cases:
    for field in case.keys():
        case[field] = remove_stopwords_punctuations(case[field])

for issue in issues:
    for field in issue.keys():
        issue[field] = remove_stopwords_punctuations(issue[field])

# Verifica a similaridade entre os test_cases e issues
results = []
for i in range(len(test_cases)):
    test_case_text = test_cases[i]["Test_Case"] + test_cases[i]["TC_Setup"] + test_cases[i]["TC_Steps"] + test_cases[i]["TC_Expected_Results"] + test_cases[i]["TC_Primary_Domain"] + test_cases[i]["TC_Secondary_Domain"] + test_cases[i]["TC_Component"] + test_cases[i]["TC_Labels"]
    min_distance = float("inf")
    min_distance_issue = None
    for j in range(len(issues)):
        issue_text = issues[j]["issue_key"] + issues[j]["description"] + issues[j]["COMMENT"]
        distance = Levenshtein.distance(test_case_text, issue_text)
        if distance < min_distance:
            min_distance = distance
            min_distance_issue = issues[j]["issue_key"]
    results.append({"Test_Case": test_cases[i]["Test_Case"], "Similar_Issue": min_distance_issue})

# Imprime o resultado
print(results)