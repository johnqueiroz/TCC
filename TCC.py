import requests
from pprint import pprint
from bs4 import BeautifulSoup
import json
#result_number_max = 0 ##Número total de CRs WAD Approval -- não precisa da variável aqui provavelmente
#number_of_crs_max_of_page_all = 0 ##Número de CR já registradas -- não precisa da variável aqui provavelmente
##i = 100 ## Precisa para alterar a paginação -- não precisa da variável aqui provavelmente
#c = 0 -- não precisa da variável aqui provavelmente

login = 'johnrf'
senha = 'Etcsdc365$'


'''------------------------------- Capturar todos os IDs das CRs ---------------------------------'''
def create_file_id_crs():
    try:
            ##  Faz uma requisção a URL com o filtro das CRs WAD Approval e armazena na variável 'response' como text
            response = requests.get('https://idart.mot.com/issues/?jql=issuetype%20%3D%20Defect%20AND%20project%20%3D%20%22SW%20S%20RELEASE%22%20AND%20status%20%3D%20%22WAD%20APPROVAL%22', auth=(login, senha)).text
            ##  Utiliza o bs4 com o html.parser para deixar a variável como um html e guarda em 'soup'
            soup = BeautifulSoup(response, 'html.parser')
            ##  A variável 'links' armazena os dados relacionados a 'tr' na classe 'issuerow' que tem no html do soup
            links = soup.find_all('tr', attrs={'class': 'issuerow'})
            ##  A variável 'number_of_crs_max' armazena os dados relacionados a 'div' na classe 'aui-item' que tem no html do soup
            number_of_crs_max = soup.find_all('div', attrs={'class': 'aui-item'})

            ## Abre/Cria o arquivo 'CR.txt' que vai deixar armazenado os IDs das CRs e o número total de CRs, sendo o último para comparar com o número da página atual e mandar ir na próxima pág
            with open('CR.txt', 'w', encoding="utf-8") as file:
            ## Os for vão passar nas tags e atributos que são designados, para recuperar os IDs e número total de CRs, respectivamente
                for link in links:
                    url_link = link.find('td', attrs={'class': 'issuekey'}).text ## Precisa ser text pro file aceitar
                    ids_crs = url_link.strip()
                    file.write(ids_crs)
                    file.write('\n')


        ## Controla o erro de Atributo que ocorreu, mesmo sem eu saber o pq. Pq no fim das contas funcionou.
    except AttributeError as mens:
        print('Deu esse erro no arquivo -', mens)

''' ------------------------------------- CR individual ---------------------------------- '''
def request_to_all_crs():
    with open('CR.txt', 'r', encoding="utf-8") as file:
        for contador in file:
            CR = contador[0:12]
            response = requests.get('https://idart.mot.com/rest/api/2/issue/'+CR, auth=(login, senha)).json()
            comments = response['fields']['comment']['comments']
            for count in comments:
                print(count['body'])
            print("\n")

'''
try:
    while number_of_crs_max_of_page_all < result_number_max:
        response = requests.get('https://idart.mot.com/issues/?jql=issuetype%20%3D%20Defect%20AND%20project%20%3D%20%22SW%20S%20RELEASE%22%20AND%20status%20%3D%20%22WAD%20APPROVAL%22&startIndex='+str(i), auth=(login, senha)).text
        soup = BeautifulSoup(response, 'html.parser')
        ##  A variável 'links' armazena os dados relacionados a 'tr' na classe 'issuerow' que tem no html do soup
        links = soup.find_all('tr', attrs={'class': 'issuerow'})
        ##  A variável 'number_of_crs_max' armazena os dados relacionados a 'div' na classe 'aui-item' que tem no html do soup
        number_of_crs_max = soup.find_all('div', attrs={'class': 'aui-item'})

        ## Abre/Cria o arquivo 'CR.txt' que vai deixar armazenado os IDs das CRs e o número total de CRs, sendo o último para comparar com o número da página atual e mandar ir na próxima pág
        with open('CR.txt', 'a', encoding="utf-8") as file:
        ## Os for vão passar nas tags e atributos que são designados, para recuperar os IDs e número total de CRs, respectivamente
            for link in links:
                url_link = link.find('td', attrs={'class': 'issuekey'}).text ## Precisa ser text pro file aceitar
                file.write(url_link)
            for number_in_page in number_of_crs_max:
                result_number_max = number_in_page.find('span', attrs={'results-count-total results-count-link'})
                number_of_crs_max_of_page_all = number_in_page.find('span', attrs={'class': 'results-count-end'})
        i = i + 100
    ## Controla o erro de Atributo que ocorreu, mesmo sem eu saber o pq. Pq no fim das contas funcionou.
except AttributeError as mens:
    print('Deu esse erro no arquivo -', mens)


'''


'''
a = '?filter=-3&jql=status%20in%20(new%2C%20working%2C%20Closed)%20AND%20issuetype%20%3D%20Defect%20AND%20project%20%3D%20%22SW%20S%20RELEASE%22%20AND%20summary%20~%20%2290Hz%22'
b = a.split('%20')
print(b)
'''


#create_file_id_crs()
request_to_all_crs()

