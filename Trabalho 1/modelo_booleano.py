#Importação de bibliotecas
import nltk #biblioteca paratrabalhar com linguagem natural
import sys  #biblioteca para manipulação de arquivos
import os   #biblioteca que permite manipular arquivos
from nltk.corpus import stopwords #biblioteca de stopwords
from nltk.stem import RSLPStemmer #biblioteca de Stemming

#download de recursos necessários
nltk.download('stopwords') #esta função é responsável por baixar os stopwords
nltk.download('rslp')

#Verificar se o número correto de argumentos da linha de comando foi fornecido
if len(sys.argv) != 2:
    print("Uso coreto: python modelo_booleano.py base_samba\base.txt")
    sys.exit(1)

#Le o caminho do arquivo em base.txt e o armazena em uma variável
base_file_path = sys.argv[1] 

if not os.path.isfile(base_file_path):
    print("Arquivo não foi encontrado em {base_file_path}") #se o caminho não existe encerra o programa
    sys.exit(1)

lista_caminhos = []

#Abre o arquivo e cria uma lista de caminhos
with open(base_file_path, 'r') as arquivo_base:
    for linha in arquivo_base:
        lista_caminhos.append(linha.strip()) #strip remove os espaços do inicio

"""#Imprime os caminhos
print("caminhos dos documentos da base:")
for caminho in lista_caminhos:
    print(caminho)
"""

#Iteração com todos os caminhos do documento e cria uma lista de palavras
palavras = []
for caminho in lista_caminhos:
    caminho_completo = os.path.join('base_samba', caminho)
    with open(caminho_completo, 'r') as arquivo: #abre o atual caminho para leitura !Não encontra o arquivo
        for linha in arquivo:
            palavras.extend(linha.split()) #split permite dividir uma string em palavras
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

#Atualizar o indice invertido com os termos e seus respectivos documentos
#----------------------------------------------------------------------------------------------------
for indice, caminho in enumerate(lista_caminhos, start=1): #O número do documento é dado com base na linha que se encontra dentro do arquivo, começando em 1
    caminho_completo = os.path.join('base_samba', caminho) #Único jeito de conseguir fazer com que seja possível acessar o folder 'base_dados' sem tirar os arquivos do folder
    with open(caminho_completo, 'r') as arquivo:
        for linha in arquivo:
            palavras = linha.split()
            for palavra in palavras:
                if palavra not in stopwords_em_portugues: #verifica se a palavra não é uma stopword
                    palavra_stem = stemmer.stem(palavra) #aplica a parada para pegar só o radical 
                    if palavra_stem in indice_invertido:
                        if indice not in indice_invertido[palavra_stem]: # Se o termo já existe no índice, adiciona o número do documento
                            indice_invertido[palavra_stem].append(indice)
                    else:
                        indice_invertido[palavra_stem] = [indice] # Se o termo não existe no índice vai criar uma nova entrada com o número do documento

#----------------------------------------------------------------------------------------------------

#indice invertido com termo, caminho e frequência
for termo, ocorrencias in indice_invertido.items():
    caminhos = []
    print(f'{termo}: ')
    for caminho in ocorrencias:
        if caminho not in caminhos:
            caminhos.append(caminho)
    frequencia = len(caminhos)
    print(frequencia)
    print(caminhos)
    print()
    
#Gravar o indice invertido em um arquivo texto
arquivo_saida = 'indice.txt'
def salvar_indice_invertido(indice_invertido, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo_saida:
        for termo, numeros_documentos in indice_invertido.items():
            numeros_documentos_formatados = ', '.join(map(str, numeros_documentos))
            arquivo_saida.write(f'{termo}:{numeros_documentos_formatados}\n')

salvar_indice_invertido(indice_invertido, arquivo_saida)


#Consultas
#Abrir o arquivo de consulta, pegar os termos e transformar em uma lista
caminho_consulta = 'base_samba\consulta.txt'
def ler_consulta(caminho_consulta):
    termos = []
    with open(caminho_consulta, 'r') as arquivo_consulta:
        consulta = arquivo_consulta.read()
        palavras = consulta.split()
        termos.extend([palavra.replace('!', '') for palavra in palavras if palavra not in ['&', '!', '|']])
        termos = [stemmer.stem(palavra) for palavra in termos] # Pegar só o radical porque é o que está no índice invertido
    return termos


print(ler_consulta(caminho_consulta))

#Mapear os termos para o índice
def mapear_termos(termos):
    termos_mapeados = {}
    for termo in termos:
        termos_mapeados[termo] = indice_invertido[termo]
    return termos_mapeados
            
termos_mapeados = mapear_termos(ler_consulta(caminho_consulta))
print(termos_mapeados)

#Avalia a consulta, levando em conta os termos booleanos
