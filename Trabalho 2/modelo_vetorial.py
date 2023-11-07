"""
Modelo Vetorial

Nome: Augusto Fernandes Macri
Matricula: 12111BSI221
"""

# Importe as bibliotecas necessárias
import nltk
import sys
import os
import math
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize

# Faça o download dos recursos necessários
nltk.download('stopwords')
nltk.download('rslp')
nltk.download('punkt')

# Verifica se o número correto de argumentos da linha de comando foi fornecido
if len(sys.argv) != 3:
    print("Uso correto: python modelo_vetorial.py base.txt consulta.txt")
    sys.exit(1)

# Le o caminho do arquivo em base.txt e o armazena em uma variável
base_file_path = sys.argv[1]
# Le o caminho do arquivo em consulta.txt e o armazena em uma variável
arquivoConsulta = sys.argv[2]

if not os.path.isfile(base_file_path):
    print(f"1° Arquivo não foi encontrado em {base_file_path}")
    sys.exit(1)

if not os.path.isfile(arquivoConsulta):
    print(f"2° Arquivo não foi encontrado em {arquivoConsulta}")
    sys.exit(1)

lista_caminhos = []

# Abre o arquivo e cria uma lista de caminhos
with open(base_file_path, 'r') as arquivo_base:
    for linha in arquivo_base:
        lista_caminhos.append(linha.strip())

# Verifica se pelo menos um documento foi encontrado
if not lista_caminhos:
    print("Nenhum documento foi encontrado")
    sys.exit(1)

# Iteração com todos os caminhos do documento e cria uma lista de palavras
palavras = []
for caminho in lista_caminhos:
    caminho_completo = os.path.join('base1', caminho)
    with open(caminho_completo, 'r') as arquivo:
        for linha in arquivo:
            palavras.extend(nltk.word_tokenize(linha))
            palavras_e_minusculo = [palavra.lower() for palavra in palavras]

# Filtro de palavras que não são interessantes (stopwords) em português
stopwords_em_português = set(stopwords.words('portuguese'))
palavras_sem_stopwords = [palavra for palavra in palavras_e_minusculo if palavra not in stopwords_em_português]

# Stemming = reduzir palavras a seu radical
stemmer = RSLPStemmer()
palavras_stem = [stemmer.stem(palavra) for palavra in palavras_sem_stopwords]

palavras_stem = sorted(palavras_stem)
palavras_stem.reverse()

indice_invertido = {}

# Atualizar o índice invertido com termos, números de documentos e frequência (igual do booleano)
for indice, caminho in enumerate(lista_caminhos, start=1):
    caminho_completo = os.path.join('base1', caminho)
    with open(caminho_completo, 'r') as arquivo:
        for linha in arquivo:
            palavras = nltk.word_tokenize(linha)
            for palavra in palavras:
                if palavra not in stopwords_em_português:
                    palavra_stem = stemmer.stem(palavra)
                    if palavra_stem in indice_invertido:
                        termo = indice_invertido[palavra_stem]
                        if termo and termo[-1][0] == indice:
                            termo[-1] = (indice, termo[-1][1] + 1)
                        else:
                            termo.append((indice, 1))
                    else:
                        indice_invertido[palavra_stem] = [(indice, 1)]

# Leitura e tokenização da consulta
def ler_consulta(arquivoConsulta):
    with open(arquivoConsulta, 'r') as arquivo_consulta:
        consulta = arquivo_consulta.read()
    return consulta

consulta = ler_consulta(arquivoConsulta)
print(consulta)

def tokenizar_consulta(consulta):
    tokens = nltk.word_tokenize(consulta)
    return tokens

tokens = tokenizar_consulta(ler_consulta(arquivoConsulta))
print(tokens)

# Cálculo do TF
TF = {}
for termo, documentos in indice_invertido.items():
    for doc, freq in documentos:
        tf_termo_no_doc = 1 + math.log10(freq)
        if doc not in TF:
            TF[doc] = {termo: tf_termo_no_doc}
        else:
            TF[doc][termo] = tf_termo_no_doc
#print(TF)

# Cálculo do IDF
num_documentos_total = len(lista_caminhos)
IDF = {}
for termo, documentos in indice_invertido.items():
    idf_termo = math.log10(num_documentos_total / len(documentos))
    IDF[termo] = idf_termo
#print(IDF)

# Cálculo do TF-IDF
TF_IDF = {}
for doc, termos in TF.items():
    TF_IDF[doc] = {}
    for termo, tf in termos.items():
        TF_IDF[doc][termo] = tf * IDF[termo]
print(TF_IDF)

# Gravar dados dos pesos no arquivo pesos.txt
dados_pesos = {}
for doc, termos in TF_IDF.items():
    dados_docs = []
    for termo, peso in termos.items():
        if peso > 0 and termo not in ['?', '.', '!']: #Fiz a remoção dos pontos na mão mesmo antes de colocar no documento *(se tiver tempo voltar e tentar de outro jeito)*
            dados_docs.append((termo, peso))
    if dados_docs:
        dados_pesos[lista_caminhos[doc - 1]] = dados_docs

with open('pesos.txt', 'w') as arquivo_pesos:
    for doc, termos in dados_pesos.items():
        arquivo_pesos.write(f'{doc}: {"   ".join([f"{termo}, {peso:.4f} " for termo, peso in termos if termo])}\n') #formatacao: doc1.txt:  W, 0.1845	X, 0.3010
        print("peso.txt")
        print(f'{doc}: {"   ".join([f"{termo}, {peso:.4f} " for termo, peso in termos if termo])}\n')


#enumerar os docs
nome_para_indice = {nome_arquivo: indice + 1 for indice, nome_arquivo in enumerate(lista_caminhos)}
print(nome_para_indice)

# Calculo de Similaridade
similaridade_resultados = []

for doc, termos in TF_IDF.items():  # Itera sobre todos os doc na base
    consulta_vetor = {}
    for termo in tokens:
        termo_stem = stemmer.stem(termo.lower())
        if termo_stem in termos:  # Verifica se tem o termo no doc
            consulta_vetor[termo_stem] = termos[termo_stem]

    similaridade = 0
    for termo, peso in termos.items():
        if termo in consulta_vetor:
            similaridade += peso * consulta_vetor[termo]

    #diminui para 0.00001 porque nenhum arquivo aparecia do resposta.txt !!!! lembrar de mudar 
    if similaridade >= 0.001: #Faz a filtragem dos resultados da similaridade que sao >= a 0.001
        similaridade_resultados.append((lista_caminhos[doc - 1], similaridade))

# Ordena os resultados por similaridade
similaridade_resultados.sort(key=lambda x: x[1], reverse=True)


# trecho de avaliar a consulta com os simbolos do codigo de mod booleano 
def avaliar_consulta(tokens, indice_invertido):
    resultado = set()  # inicializa como um conjunto vazio
    operador = None
    for token in tokens:
        if token == '&':
            operador = 'and'
        elif token == '|':
            operador = 'or'
        elif token == '!':
            operador = 'not'
        else:
            termo_stem = stemmer.stem(token.lower())  # aplica stemming
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
                    resultado.difference_update(documentos_termo)
            operador = None
    return resultado

resultado = avaliar_consulta(tokens, indice_invertido)
print(resultado)

# Ordena os resultados por similaridade
similaridade_resultados.sort(key=lambda x: x[1], reverse=True)

# Grava os resultados no arquivo resposta.txt
with open('resposta.txt', 'w') as arquivo_resposta:
    arquivo_resposta.write(f"{len(similaridade_resultados)}\n")
    for doc, similaridade in similaridade_resultados:
        arquivo_resposta.write(f"{doc} {similaridade:.4f}\n")
        print("resposta.txt")
        print(f"{doc} {similaridade:.4f}")

"""
03/11
Estava funcionando perfeitamente para a consulta 1
mas não funciona para a consulta 2 porque ela tem o & igual no cod do booleano
lembrar de pegar aquele trecho 
04/11
tambem ficava preso so no primeiro doc pq tava TF_IDF[1][termo_stem] no calc da similaridade
ai fazia com que dasse 0 na segunda consulta tbm
6/11
se eu mudar a consulta.txt para engracada ou amor, sempre vai devolver 0.2276
mas se a consulta for casa, ele devolve 0 sempre 
"""