import json
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier


def read_issues(filename):
   with open("resources/" + filename, "r", encoding="utf-8") as f:
       return json.load(f)


def read_test_cases(filename):
   with open("resources/" + filename, "r", encoding="utf-8") as f:
       return json.load(f)


def preprocess_text(text):
   stop_words = set(stopwords.words('english'))
   if text is not None:
       tokens = word_tokenize(text.lower())
       words = [w for w in tokens if w not in stop_words and w not in string.punctuation]
       return ' '.join(words)


def preprocess_issues(issues):
   for issue in issues:
       issue['description'] = preprocess_text(issue['description'])
       issue['COMMENT'] = preprocess_text(issue['COMMENT'])
   return issues


def preprocess_test_cases(test_cases):
   for test_case in test_cases:
       test_case['TC_Setup'] = preprocess_text(test_case['TC_Setup'])
       test_case['TC_Steps'] = preprocess_text(test_case['TC_Steps'])
       test_case['TC_Expected_Results'] = preprocess_text(test_case['TC_Expected_Results'])
   return test_cases


def train_model(issues, test_cases):
   # Cria um DataFrame com as descrições dos casos de teste e suas respectivas labels
   test_case_descriptions = []
   test_case_labels = []
   for test_case in test_cases:
       test_case_descriptions.append(
           (test_case['TC_Setup'] or '') +
           ' ' +
           (test_case['TC_Steps'] or '') +
           ' ' +
           (test_case['TC_Expected_Results'] or '')
       )
       test_case_labels.append(test_case['Test_Case'])
   test_case_df = pd.DataFrame({'description': test_case_descriptions, 'label': test_case_labels})

   # Cria um DataFrame com as descrições das issues e suas respectivas labels
   issue_descriptions = []
   issue_labels = []
   for issue in issues:
       issue_descriptions.append(issue['description'] + ' ' + issue['COMMENT'])
       issue_labels.append(issue['issue_key'])
   issue_df = pd.DataFrame({'description': issue_descriptions, 'label': issue_labels})

   # Usa o TF-IDF para representar as descrições como vetores numéricos
   vectorizer = TfidfVectorizer()
   X_test_cases = vectorizer.fit_transform(test_case_df['description'])
   X_issues = vectorizer.transform(issue_df['description'])

   # Treina um modelo de Random Forest
   y_test_cases = test_case_df['label']
   rf = RandomForestClassifier()
   rf.fit(X_test_cases, y_test_cases)

   # Faz a predição das labels das issues
   y_pred = rf.predict(X_issues)

   # Cria um dicionário com as predições
   predictions = {}
   for i, issue_key in enumerate(issue_df['label']):
       predictions[issue_key] = y_pred[i]

   return predictions


def show_results(predictions):
   for issue_key, test_case in predictions.items():
       print(f"Issue {issue_key} está relacionada com o caso de teste {test_case}")


# Lê os arquivos JSON
issues = read_issues('issues.json')
test_cases = read_test_cases('test_cases.json')

# Pré-processa o texto
issues = preprocess_issues(issues)
test_cases = preprocess_test_cases(test_cases)

# Treina o modelo de Random Forest
predictions = train_model(issues, test_cases)

# Mostra os resultados
show_results(predictions)
