import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Abrindo os arquivos que serão usados como dataset
features_file = pd.read_csv('features.csv')
test_case_file = pd.read_csv("TestsCases.csv")


# Extraindo o valor das colunas dos arquivos
cabecalho_features = features_file.columns.values.tolist()
cabecalho_test_case = test_case_file.columns.values.tolist()


# Extraindo o valor das linhas dos arquivos
lista_features = features_file.values.tolist()
lista_test_case = test_case_file.values.tolist()


# Juntando os dois valores
lista_features.insert(0, cabecalho_features)
lista_test_case.insert(0, cabecalho_test_case)


# Documentos a serem comparados
doc1 = [str(x) for x in lista_features]
doc2 = [str(x) for x in lista_test_case]


# tokeniza e remove stopwords de cada elemento das listas
list1_tokens = [word_tokenize(sent) for sent in doc1]
list2_tokens = [word_tokenize(sent) for sent in doc2]
list1_tokens = [[word for word in sent if word.lower() not in stopwords.words('english') and word not in string.punctuation] for sent in list1_tokens]
list2_tokens = [[word for word in sent if word.lower() not in stopwords.words('english') and word not in string.punctuation] for sent in list2_tokens]


# Juntando de volta as lista de tokens para serem strings
list1_tokens = [" ".join(sent) for sent in list1_tokens]
list2_tokens = [" ".join(sent) for sent in list2_tokens]


# Converte o texto em vetores usando o TF-IDF
tfidf = TfidfVectorizer()
vectors = tfidf.fit_transform(list1_tokens + list2_tokens)


# Obtém as similaridades entre cada elemento da lista1 e cada elemento da lista2
for i, element1 in enumerate(list1_tokens):
    for j, element2 in enumerate(list2_tokens):
        similarity = cosine_similarity(vectors[i], vectors[len(list1_tokens) + j])
        print(f'Similaridade entre {element1} e {element2}: {similarity[0][0]}')


        #Manter os resultados em um CSV
        # if similarity >= 0.07:
        #     results = [[element1, element2, similarity[0][0]] for i, element1 in enumerate(list1_tokens) for j, element2 in
        #                enumerate(list2_tokens)]
        #     df = pd.DataFrame(results, columns=['list1', 'list2', 'similarity'])
        #
        #     # salva o dataframe em um arquivo CSV
        #     df.to_csv('similarity_results.csv', index=False)