import string
import tkinter as tk
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics import accuracy_score

# Coletar os textos e a classe "relacionado" em duas listas
texts1 = ["Check Screen Recording when device storage is full", "O gato comeu o rato" , "Check Gestures Navigation Tutorial", "I am hungry", "Enable Mobile Hotspot icon from Quick Settings - WiFi ON (No Concurrency)", "Lazy is kingdom", "Verify status bar when sim are inserted."]
texts2 = ["Screen Recording", "Direct Boot Mode - Basic Verification", "Tutorial for Q Nav", "The water is dark", "Setting UI requirements", "I am hungry also", "Settings requirements integration and customization"]
related = [1, 0, 1, 0, 1, 0, 1]

# Juntar os textos em uma única lista e remover pontuação e stopwords
punctuation = string.punctuation
stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower()
    text = ''.join([c for c in text if c not in punctuation])
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens)

texts = [preprocess(t1) + " " + preprocess(t2) for t1, t2 in zip(texts1, texts2)]

# Transformar os textos em vetores de palavras com Tf-Idf
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, related, test_size=0.2)

# Treinar o modelo de classificação
model = LogisticRegression()
model.fit(X_train, y_train)

# Testar o modelo com os dados de teste
predictions = model.predict(X_test)

# Verificar a precisão do modelo
accuracy = accuracy_score(y_test, predictions)
print("Precisão do modelo:", accuracy)

class App:
   def __init__(self):
       self.root = tk.Tk()
       self.root.title("Teste x Feature")
       self.root.geometry("400x400")

       tk.Label(self.root, text="Core ID:").pack()
       self.coreid = tk.Entry(self.root)
       self.coreid.pack()

       tk.Label(self.root, text="Senha :").pack()
       self.password = tk.Entry(self.root, show="*")
       self.password.pack()

       tk.Label(self.root, text="Test case:").pack()
       self.test_case = tk.Entry(self.root)
       self.test_case.pack()

       tk.Label(self.root, text="Feature:").pack()
       self.feature = tk.Entry(self.root)
       self.feature.pack()

       tk.Label(self.root, text="").pack()

       tk.Button(self.root, text="Mostrar Resposta", command=self.mostrar_resposta).pack()

       tk.Label(self.root, text="").pack()

       self.resposta = tk.Label(self.root, text="")
       self.resposta.pack()

# Usar o modelo para classificar um novo par de textos
# new_text1 = "Check Wifi Data Usage"
# new_text2 = "Settings requirements integration and customization"

   def mostrar_resposta(self):
    coreid = self.coreid.get()
    password = self.password.get()
    test_case = self.test_case.get()
    feature = self.feature.get()

    params = "fields=*all"

    # URLs base para verificação na API
    url_feature = "https://idart.mot.com/rest/api/latest/issue/"
    url_test_case = "https://dalek.mot.com/rest/api/latest/issue/"

    # Request feito
    request_feature = requests.get(url_feature + feature, auth=(coreid, password), params=params)
    request_test_case = requests.get(url_test_case + test_case, auth=(coreid, password), params=params)

    # Transformando o objeto em json para logo mais observar seus campos
    url_feature_json = request_feature.json()
    url_test_case_json = request_test_case.json()

    # Campos do json que serão utilizados
    summary_feature = url_feature_json['fields']['summary']
    summary_test_case = url_test_case_json['fields']['summary']

    # Documentos a serem comparados
    doc1 = summary_feature
    doc2 = summary_test_case


    new_text = preprocess(doc1) + " " + preprocess(doc2)
    new_vector = vectorizer.transform([new_text])


    prediction = model.predict(new_vector)[0]

    if prediction == 1:
        self.resposta.config(text="TC e feature podem estar relacionados: " + feature + ", " + test_case)
    else:
        self.resposta.config(text="TC e feature não estão relacionados: " + feature + ", " + test_case)

app = App()
app.root.mainloop()