import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Opening the files that will be used as dataset
features_file = pd.read_csv('features_sem_comments.csv')
test_case_file = pd.read_csv("TestsCases.csv")


# Extracting value from the columns of the files
cabecalho_features = features_file.columns.values.tolist()
cabecalho_test_case = test_case_file.columns.values.tolist()


# Extracting value from the lines of the files
lista_features = features_file.values.tolist()
lista_test_case = test_case_file.values.tolist()


# Joining both values
lista_features.insert(0, cabecalho_features)
lista_test_case.insert(0, cabecalho_test_case)


# Converting variables to string
doc1 = [str(x) for x in lista_features]
doc2 = [str(x) for x in lista_test_case]


# tokenizes and removes stopwords from each element in lists
list1_tokens = [word_tokenize(sent) for sent in doc1]
list2_tokens = [word_tokenize(sent) for sent in doc2]
list1_tokens = [[word for word in sent if word.lower() not in stopwords.words('english') and word not in string.punctuation] for sent in list1_tokens]
list2_tokens = [[word for word in sent if word.lower() not in stopwords.words('english') and word not in string.punctuation] for sent in list2_tokens]


# Putting back the list of tokens to be strings
list1_tokens = [" ".join(sent) for sent in list1_tokens]
list2_tokens = [" ".join(sent) for sent in list2_tokens]


# Convert text to vectors using TF-IDF
tfidf = TfidfVectorizer()
vectors = tfidf.fit_transform(list1_tokens + list2_tokens)

# Create an empty dataframe to store the similarities
similarities = pd.DataFrame()

# Gets the similarities between each element of list1 and each element of list2
for i, element1 in enumerate(list1_tokens):
    for j, element2 in enumerate(list2_tokens):
        similarity = cosine_similarity(vectors[i], vectors[len(list1_tokens) + j])
        similarity = similarity[0][0]

        if similarity >= 0.4:
            # Adiciona as frases comparadas e a similaridade calculada ao dataframe
            similarities = similarities.append({'Features': element1[1:13], 'Test Case': element2[1:13], 'similarity': similarity}, ignore_index=True)

# salva o dataframe no arquivo xlsx
similarities.to_excel("similaridade.xlsx", index=False)
print("Similaridade salva com sucesso no arquivo similaridade.xlsx")


# testando