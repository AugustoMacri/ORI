#Importação de bibliotecas
import nltk #biblioteca paratrabalhar com linguagem natural
import sys  #biblioteca para manipulação de arquivos
import os   #biblioteca que permite manipular arquivos
from nltk.corpus import stopwords #biblioteca de stopwords

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

#Imprime os caminhos
print("caminhos dos documentos da base:")
for caminho in lista_caminhos:
    print(caminho)


#Iteração com todos os caminhos do documento e cria uma lista de palavras
palavras = []
for caminho in lista_caminhos:
    with open(caminho, 'r') as arquivo: #abre o atual caminho para leitura !Não encontra o arquivo
        for linha in arquivo:
            palavras.extend(linha.split()) #split permite dividir uma string em palavras
            palavras_e_minusculo = [palavra.lower() for palavra in palavras]#Já que palavras Maiúsculas e minusculas devem ser tratadas igualmente, então é necessário transformar as palavras em minusculas
#OBS: para conseguir encontrar o caminho dos arquivos foi necessário remover elas do folder

#Filtro de palavras que não são interessantes (stopwords)
stopwords_em_portugues = stopwords.words('portuguese')
palavras_sem_stopwords = [palavra for palavra in palavras_e_minusculo if palavra not in stopwords_em_portugues]

#Índice Invertido
palavras_sem_stopwords = sorted(palavras_sem_stopwords) #ordena a lista de palavras já sem as stopwords em ordem alfabética
palavras_sem_stopwords.reverse()
print("Palavras sem stopwords")

indice_invertido = {}

