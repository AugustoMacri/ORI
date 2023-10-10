#Importação de bibliotecas
import nltk #biblioteca paratrabalhar com linguagem natural
import sys  #biblioteca para manipulação de arquivos
import os   #biblioteca que permite manipular arquivos
from nltk.corpus import stopwords #biblioteca de stopwords
from nltk.stem import RSLPStemmer #biblioteca de Stemming

#download de recursos necessários
nltk.download('stopwords') #esta função é responsável por baixar os stopwords
nltk.download('rslp')
nltk.download('punkt') 

#Verificar se o número correto de argumentos da linha de comando foi fornecido
if len(sys.argv) != 3:
    print("Uso correto: python modelo_booleano.py arquivoBase arquivoConsulta")
    sys.exit(1)

#Le o caminho do arquivo em base.txt e o armazena em uma variável
base_file_path = sys.argv[1] 
#Le o caminho do arquivo em consulta.txt e o armazena em uma variável
arquivoConsulta = sys.argv[2]

if not os.path.isfile(base_file_path):
    print("Arquivo não foi encontrado em {base_file_path}") #se o caminho não existe encerra o programa
    sys.exit(1)

if not os.path.isfile(arquivoConsulta):
    print("Arquivo não foi encontrado em {arquivoConsulta}") #se o caminho não existe encerra o programa
    sys.exit(1)

lista_caminhos = []

#Abre o arquivo e cria uma lista de caminhos
with open(base_file_path, 'r') as arquivo_base:
    for linha in arquivo_base:
        lista_caminhos.append(linha.strip()) #strip remove os espaços do inicio

#Iteração com todos os caminhos do documento e cria uma lista de palavras
palavras = []
for caminho in lista_caminhos:
    caminho_completo = os.path.join('base_samba', caminho)
    with open(caminho_completo, 'r') as arquivo: #abre o atual caminho para leitura !Não encontra o arquivo
        for linha in arquivo:
            #palavras.extend(nltk.word_tokenize(linha)) #cria uma lista de palavras
            palavras_e_minusculo = [palavra.lower() for palavra in palavras]#Já que palavras Maiúsculas e minusculas devem ser tratadas igualmente, então é necessário transformar as palavras em minusculas

#Filtro de palavras que não são interessantes (stopwords) em portugues
stopwords_em_portugues = set(stopwords.words('portuguese'))
palavras_sem_stopwords = [palavra for palavra in palavras_e_minusculo if palavra not in stopwords_em_portugues]

#Stemming = reduzir palavras a seu radical
stemmer = RSLPStemmer()
palavras_stem = [stemmer.stem(palavra) for palavra in palavras_sem_stopwords]

#Índice Invertido
palavras_stem = sorted(palavras_stem) 
palavras_stem.reverse() #inverte a ordem 

indice_invertido = {}  #Dicionário para armazenar os termos e os caminhos

# Atualizar o índice invertido com termos, números de documentos e frequência
for indice, caminho in enumerate(lista_caminhos, start=1): #npumero do docuemnto é dado com base na linha que se encontra dentro do arquivo base.txt, começando em 1
    caminho_completo = os.path.join('base_samba', caminho) #unico jeito que consegui fazer com que seja possível acessar o folder
    with open(caminho_completo, 'r') as arquivo:
        for linha in arquivo:
            palavras = nltk.word_tokenize(linha)
            for palavra in palavras:
                if palavra not in stopwords_em_portugues: #verifica se a palavra não é um stopword
                    palavra_stem = stemmer.stem(palavra) #aplica a parada para pegar só o radical
                    if palavra_stem in indice_invertido:
                        termo = indice_invertido[palavra_stem] #se o termo ja existe no índice, adiciona o número do documento e a frequência
                        if termo and termo[-1][0] == indice: #se o termo já existe no índice, adiciona a frequência
                            termo[-1] = (indice, termo[-1][1] + 1)
                        else:
                            termo.append((indice, 1))
                    else:
                        indice_invertido[palavra_stem] = [(indice, 1)] 

# Gravar o índice invertido em um arquivo de texto
arquivo_saida = 'indice.txt'
def salvar_indice_invertido(indice_invertido, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo_saida:
        for termo, documentos_frequencias in indice_invertido.items(): 
            documentos_formatados = ', '.join([f'{doc_num},{freq}' for doc_num, freq in documentos_frequencias]) #cria uma lista de tuplas
            arquivo_saida.write(f'{termo}: {documentos_formatados}\n')

salvar_indice_invertido(indice_invertido, arquivo_saida)

#Consultas
#Abrir o arquivo de consulta e pegar os termos 
#caminho_consulta = 'base_samba\consulta.txt'
def ler_consulta(arquivoConsulta):
    with open(arquivoConsulta, 'r') as arquivo_consulta:
        consulta = arquivo_consulta.read()
    return consulta

consulta = ler_consulta(arquivoConsulta)
print(consulta)

#tokeinizar a consulta
def tokenizar_consulta(consulta):
    tokens = nltk.tokenize.word_tokenize(consulta) #tokenizar em palavras individuais e símbolos
    return tokens

tokens = tokenizar_consulta(ler_consulta(arquivoConsulta))
print(tokens)

#Avaliar consulta
def avaliar_consulta(tokens, indice_invertido): 
    resultado = set() #inicializa como um conj vazio
    operador = None
    for token in tokens: 
        if token == '&':
            operador = 'and'
        elif token == '|':
            operador = 'or'
        elif token == '!':
            operador = 'not'
        else:
            termo_stem = stemmer.stem(token)  # aplica stemming
            if operador is None:
                if termo_stem in indice_invertido: 
                    resultado = set([doc for doc, freq in indice_invertido[termo_stem]])
                else:
                    resultado = set()  # Termo não existe no índice, conjunto vazio
            else:
                if termo_stem in indice_invertido:
                    documentos_termo = set([doc for doc, freq in indice_invertido[termo_stem]])
                else:
                    documentos_termo = set()
                if operador == 'and':
                    resultado = resultado.intersection(documentos_termo)
                elif operador == 'or':
                    resultado = resultado.union(documentos_termo)
                elif operador == 'not':
                    print(operador)
                    resultado.difference_update(documentos_termo)
            operador = None  # Limpa o operador após usá-lo
    return resultado

resultado = avaliar_consulta(tokens, indice_invertido)
print(resultado)


#gravar o resultado em um arquivo
def salvar_resultado(resultado, arquivo_resposta, lista_caminhos):
    with open(arquivo_resposta, 'w', encoding='utf-8') as arquivo_resposta:
        arquivo_resposta.write(f'{len(resultado)}\n')
        for nome in resultado:
            nome_arquivo = lista_caminhos[nome -1]
            arquivo_resposta.write(f'{nome_arquivo}\n') #nome dos docs que satisfazem a consulta

arquivo_resposta = 'resposta.txt'
salvar_resultado(resultado, arquivo_resposta, lista_caminhos)
