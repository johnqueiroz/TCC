import json
import string
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein

# Recebendo arquivos JSON
test_cases_file = open('resources/test_cases.json', 'r', encoding='utf-8')
test_cases_data = json.load(test_cases_file)

issues_file = open('resources/issues.json', 'r', encoding='utf-8')
issues_data = json.load(issues_file)

# Removendo stopwords e pontuações dos dados do arquivo JSON
stopwords = set(stopwords.words("english"))
punctuations = string.punctuation

test_cases_text = []
for test_case in test_cases_data:
    tc_text = test_case['Test_Case']
    tc_text = tc_text.lower()
    tc_text = ''.join([word for word in tc_text if word not in punctuations])
    tc_text = ' '.join([word for word in tc_text.split() if word not in stopwords])
    test_cases_text.append(tc_text)

issues_text = []
for issue in issues_data:
    issue_text = issue['description']
    issue_text = issue_text.lower()
    issue_text = ''.join([word for word in issue_text if word not in punctuations])
    issue_text = ' '.join([word for word in issue_text.split() if word not in stopwords])
    issues_text.append(issue_text)

# Verificando a similaridade entre os dados
for test_case_text in test_cases_text:
    for issue_text in issues_text:
        distance = Levenshtein.distance(test_case_text, issue_text)
        ratio = Levenshtein.ratio(test_case_text, issue_text)
        print("Test Case:", test_case_text)
        print("Issue:", issue_text)
        print("Levenshtein Distance:", distance)
        print("Levenshtein Ratio:", ratio)
        print("\n")
