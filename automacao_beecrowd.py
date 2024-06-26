from selenium import webdriver
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

email_cadastrado = os.getenv('EMAIL_CADASTRADO')
senha = os.getenv('SENHA_CADASTRADA')

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
navegador = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(navegador, 20)
tempos = {'tempo_carregamento': 2, 'tempo_final': 5, 'clear': 0.1}

def quadro (frase):
    tamanho = len(frase)
    retorno = " " + "-"*(tamanho + 2) + " \n"
    retorno += "| " + frase + " |" + "\n"
    retorno += " " + "-"*(tamanho + 2) + " " + "\n"
    return retorno

def filtro (linguagem):
    if(linguagem == "C99" or linguagem == "C"):
        return "C"
    if(linguagem == "C++" or linguagem == "C++17"):
        return "C++"
    return linguagem

def falta(problema):
    if("Python" in problema and "Ruby" not in problema):
        return True
    return False

navegador.maximize_window()
navegador.get("https://judge.beecrowd.com/pt/login")
sleep(tempos['tempo_carregamento'])
campo_email = navegador.find_element('xpath', '//*[@id="email"]')
campo_email.send_keys(email_cadastrado)
campo_senha = navegador.find_element('xpath', '//*[@id="password"]')
campo_senha.send_keys(senha)
sai_da_frente = navegador.find_element('xpath', '/html/body/div[3]/div/div/button')
sai_da_frente.click()
botao_login = navegador.find_element('xpath', '//*[@id="users-form"]/form/div[5]/input')
botao_login.click()
sleep(tempos['tempo_carregamento'])
navegador.get("https://www.beecrowd.com.br/judge/pt/runs?answer_id=1")
sleep(tempos['tempo_carregamento'])
navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(tempos['tempo_carregamento'])
botao_ultimo = navegador.find_element('xpath', '/html/body/div[1]/div/div[2]/div[4]/div/div[2]/div[2]/li[4]')
botao_ultimo.click()
url_atual = navegador.current_url
quantidade_paginas = int(url_atual.split("page=")[1])
arquivo = open('problemas2.0.txt','w+')

dados = []
problemas = []

for num_pagina in range(1, quantidade_paginas + 1):
    url = "https://www.beecrowd.com.br/judge/pt/runs?answer_id=1&page="+str(num_pagina)
    navegador.get(url)
    submissoes = navegador.find_elements('tag name', 'tr')
    for i in range(1, len(submissoes)):
        if("" != submissoes[i].text):
            dados_do_problema = submissoes[i].text.split()
            codigo = dados_do_problema[1]
            indice = dados_do_problema.index('Accepted') + 1
            linguagem = filtro(dados_do_problema[indice])
            if(codigo not in problemas):
                dados.append([codigo, linguagem])
                problemas.append(codigo)
            else:
                for problema in dados:
                    if(problema[0] == codigo and linguagem not in problema):
                        problema.append(linguagem)
dados.sort()
dados_pontuacao = []
nao_resolvidos = i = 0
tam_coluna = 20
quantidade_colunas = 1
os.system('cls')
print("-"*(tam_coluna+2)*quantidade_colunas)
arquivo.write(" " + "-"*tam_coluna*quantidade_colunas + " \n")
for problema in dados:
    if(falta(problema) and 'PostgreSQL' not in problema):
        dados_pontuacao.append(problema)
        if((nao_resolvidos + 1) % quantidade_colunas == 0):
            print("|" + ' '.join(problema).center(tam_coluna) + "|")
            arquivo.write("|" + ' '.join(problema).center(tam_coluna)  + "|" + '\n')
        else:
            print("|"+' '.join(problema).center(tam_coluna) + "|", end="")
            arquivo.write("|"+' '.join(problema).center(tam_coluna) + "|")
        nao_resolvidos += 1
if((nao_resolvidos + 1) % 5 != 0):
    print("")
    arquivo.write("\n")
print("-"*(tam_coluna+2)*quantidade_colunas)
arquivo.write(" " + "-"*(tam_coluna+2)*quantidade_colunas + " \n")
quadro_nao_resolvidos = "\n" + quadro("Problemas não resolvidos em alguma linguagem: " + str(nao_resolvidos))
print(quadro_nao_resolvidos)
arquivo.write(quadro_nao_resolvidos)

arquivo.write("\n\n")
pontos_problemas = []

for problema in dados_pontuacao:
    numero = problema[0]
    url = "https://www.beecrowd.com.br/judge/pt/problems/view/" + str(numero)
    navegador.get(url)
    sleep(tempos['clear'])
    pontos = navegador.find_element('xpath', '/html/body/div[2]/div/div[1]/div/ul/li[5]/em')
    valor = float(pontos.text.split(" ")[1])
    pontos_problemas.append([valor, problema[0]])

pontos_problemas.sort()

for ponto_problema in pontos_problemas:
    print(str(ponto_problema[1]) + " - " + str(ponto_problema[0]))
    arquivo.write(str(ponto_problema[1]) + " - " + str(ponto_problema[0]) + "\n")