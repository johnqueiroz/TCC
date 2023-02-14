import json
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# Converte os dados em vetores usando TF-IDF
tfidf_vectorizer = TfidfVectorizer()

all_text = [case["Test_Case"] + case["TC_Setup"] + case["TC_Steps"] + case["TC_Expected_Results"]
            + case["TC_Primary_Domain"] + case["TC_Secondary_Domain"] + case["TC_Component"] + case["TC_Labels"] for case in test_cases]
all_text += [issue["issue_key"] + issue["description"] + issue["COMMENT"] for issue in issues]

vectors = tfidf_vectorizer.fit_transform(all_text)

test_cases_vectors = vectors[:len(test_cases)]
issues_vectors = vectors[len(test_cases):]

# Verifica a similaridade entre os test_cases e issues
results = []
for i in range(len(test_cases)):
    cosine_sim = cosine_similarity(test_cases_vectors[i], issues_vectors)
    if (cosine_sim >= 0.5).any():
        max_index = cosine_sim.argmax()
        results.append({"Test_Case": test_cases[i]["Test_Case"], "Similar_Issue": issues[max_index]["issue_key"]})

# Imprime o resultado
print(results)
