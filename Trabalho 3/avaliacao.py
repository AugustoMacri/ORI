"""
Modelo de avalicação com gráficos 

Nome: Augusto Fernandes Macri
Matrícula: 12111BSI221

Os cálculos e gráficos foram realizados na mão antes de serem implementados no código para maior acurácia, a resolução pode ser vista em: https://github.com/AugustoMacri/ORI/tree/main/Trabalho%203
"""
import sys
import matplotlib.pyplot as plt
import numpy as np

def ler_arq(arquivo):
    try:
        with open(arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            #Extrair o num de consultas
            num_consultas = int(linhas[0])

            #Extrair respostas ideais e do sistema
            respostas_ideais = [list(map(int, linha.split())) for linha in linhas[1:num_consultas + 1]]
            respostas_sistema = [list(map(int, linha.split())) for linha in linhas[num_consultas + 1:]]

            return num_consultas, respostas_ideais, respostas_sistema
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        sys.exit(1)

if __name__ == "__main__": #verifica se o programa está sendo executado diretamente
    if len(sys.argv) != 2: #verifica se dois arquivos foram passados
        print("Uso: >python avaliacao.py nome_do_arquivo")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    num_consultas, respostas_ideais, respostas_sistema = ler_arq(nome_arquivo)

#print(respostas_ideais)
#print(respostas_sistema)

#Calcular prec e revoc para cada consulta
def calcular_prec_revoc(respostas_ideal, resposta_sistema):
    precisoes = []
    revocacoes = []

    for termo in resposta_sistema:
        if termo in respostas_ideal:
            documentos_recuperados = len(resposta_sistema[:resposta_sistema.index(termo)+1])
            documentos_relevantes_recuperados = len(set(resposta_sistema[:resposta_sistema.index(termo)+1]).intersection(set(respostas_ideal)))

            precisao = documentos_relevantes_recuperados / documentos_recuperados if documentos_recuperados > 0 else 0
            revocacao = documentos_relevantes_recuperados / len(respostas_ideal) if len(respostas_ideal) > 0 else 0

            precisoes.append(precisao)
            revocacoes.append(revocacao)

    return precisoes, revocacoes



# Interpolação da prec e revoc
niveis_revocacao = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
def interpolar_valores(precisoes, revocacoes):
    #lista com prec e revoc
    dados = list(zip(revocacoes, precisoes))
    dados.sort(reverse=True)  #revoc decrescente

    valores_interp = []

    for nivel in niveis_revocacao:
        prec_interpoladas = [prec for rev, prec in dados if rev >= nivel]  #Filtrar a maior prec
        if prec_interpoladas:
            valor_interp = max(prec_interpoladas)  #maior prec para o nivel
            valores_interp.append(valor_interp)
        else:
            valores_interp.append(0)  #se nao tiver precisao colocar em 0

    return valores_interp


valores_interpolados_por_consulta = []
for i in range(num_consultas):
    precisoes, revocacoes = calcular_prec_revoc(respostas_ideais[i], respostas_sistema[i])
    
    #interp para cada consulta
    valores_interp = interpolar_valores(precisoes, revocacoes)
    valores_interpolados_por_consulta.append(valores_interp)

    #print(valores_interp)

#calcular a media dos valores 
media_precisao = np.mean(valores_interpolados_por_consulta, axis=0)

#Colocar medias no arquivo media.txt
with open('media.txt', 'w') as arquivo:
    for precisao in media_precisao:
        arquivo.write(f'{precisao:.2f} ')

#Plotação dos graficos
#disposiçao dos graficos 
num_linhas = 2
num_colunas = 2

#todos numa unica janela
fig, axs = plt.subplots(num_linhas, num_colunas, figsize=(12, 10))

#Ajuste de posicao
for i, valores in enumerate(valores_interpolados_por_consulta[:num_linhas*num_colunas], start=1):
    linha = (i - 1) // num_colunas
    coluna = (i - 1) % num_colunas
    axs[linha, coluna].plot(niveis_revocacao, valores, marker='o', linestyle='-', label=f'Consulta {i}')
    axs[linha, coluna].set_xlabel('Revocação')
    axs[linha, coluna].set_ylabel('Precisão')
    axs[linha, coluna].set_title(f'Gráfico de Precisão-Revocação para Consulta {i}')
    axs[linha, coluna].legend()
    axs[linha, coluna].grid(True)

#Gráfico da média
axs[num_linhas-1, num_colunas-1].plot(niveis_revocacao, media_precisao, marker='o', linestyle='-', label='Média de Todas as Consultas')
axs[num_linhas-1, num_colunas-1].set_xlabel('Revocação')
axs[num_linhas-1, num_colunas-1].set_ylabel('Precisão')
axs[num_linhas-1, num_colunas-1].set_title('Média de Precisão-Revocação para Todas as Consultas')
axs[num_linhas-1, num_colunas-1].legend()
axs[num_linhas-1, num_colunas-1].grid(True)

plt.tight_layout()
plt.show()
