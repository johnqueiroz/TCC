import requests
import nltk
import pandas as pd
import tkinter as tk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#ID da FEATURE e Test Case que serão usados no script
#feature = "FEATURE-3957"
#test_case = "MCA-3815769"

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

       # Tokeniza e remove as stopwords dos documentos
       tokens1 = [token for token in word_tokenize(doc1) if token not in stopwords.words("english")]
       doc1 = " ".join(tokens1)

       tokens2 = [token for token in word_tokenize(doc2) if token not in stopwords.words("english")]
       doc2 = " ".join(tokens2)

       # Transforma os documentos em vetores de características com o TfidfVectorizer
       vectorizer = TfidfVectorizer()
       vectors = vectorizer.fit_transform([doc1, doc2])

       # Calcula a similaridade cosseno entre os dois documentos
       similarity = cosine_similarity(vectors[0], vectors[1])

       if similarity >= 0.07:
           self.resposta.config(text="TC e feature podem estar relacionados: " + feature + ", " + test_case)
       else:
           self.resposta.config(text="TC e feature não estão relacionados: " + feature + ", " + test_case)

app = App()
app.root.mainloop()