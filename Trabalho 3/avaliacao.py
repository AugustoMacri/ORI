"""
Modelo de avalicação com gráficos 

Nome: Augusto Fernandes Macri
Matrícula: 12111BSI221

matplotlib n funcionava, baixar:
pip install matplotlib

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

#Calcular Precisão e Revocação para cada consulta 
def calcular_prec_revoc(respostas_ideal, resposta_sistema):
    documentos_recuperados = len(resposta_sistema)
    documentos_relevantes_recuperados = len(set(resposta_sistema).intersection(set(respostas_ideal)))

    precisao = documentos_relevantes_recuperados / documentos_recuperados if documentos_recuperados > 0 else 0 #calculo da precisao para cada consulta
    revocacao = documentos_relevantes_recuperados / len(respostas_ideal) if len(respostas_ideal) > 0 else 0 #calculo da revocacao para cada consulta

    return precisao, revocacao


result_precisao = []
result_revoc = []

for i in range(num_consultas):
    precisao, revocacao = calcular_prec_revoc(respostas_ideais[i], respostas_sistema[i])
    result_precisao.append(precisao)
    result_revoc.append(revocacao)
    print(f"Consulta {i + 1}: Precisão: {precisao}, Revocação: {revocacao}")


#Interpolação da prec e revoc
niveis_revocacao = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]# Níveis de revocação de 0 a 1 em incrementos de 0.1
def interpolar_valores(precisao, revocacao):
    valores_interp = []

    precisao_ordenada, revocacao_ordenada = zip(*sorted(zip(precisao, revocacao), key=lambda x: x[1]))

    print(f"Precis ord: {precisao_ordenada}")
    print(f"Revoc ord {revocacao_ordenada}")

    for nivel in niveis_revocacao:
        valores_nivel = [p for r, p in zip(revocacao_ordenada, precisao_ordenada) if r >= nivel] #zip faz com que seja criado uma lista de tuplas onde cada tupla contem um par (revoc, prec)
        if valores_nivel:
            closest_value = min(valores_nivel, key=lambda x: abs(x - nivel))
            valores_interp.append(closest_value)
        else:
            valores_interp.append(0)

        print(f"Nível de revocação: {nivel}, Valores de precisão: {valores_nivel}")

    return valores_interp

"""print("!!!!Valores apos a interpolacao!!!!")
valores_interpolados = interpolar_valores(result_precisao, result_revoc)
print("Valores interpolados:", valores_interpolados)"""


#Interpolação da prec e revoc para cada consulta (na referencia e para sair 3 consultas)
valores_interpolados_por_consulta = []

for i in range(num_consultas):
    valores_interp = interpolar_valores([result_precisao[i]], [result_revoc[i]])
    valores_interpolados_por_consulta.append(valores_interp)

#Plotar os graficos (graficos da consulta, nao o da media)
for i, valores in enumerate(valores_interpolados_por_consulta, start=1):
    plt.figure()  #Tem que criar uma fig nova para cada grafico, antes tava criando uma com todas as consultas 
    plt.plot(niveis_revocacao, valores, marker='o', linestyle='-', label=f'Consulta {i}')
    plt.xlabel('Revocação')
    plt.ylabel('Precisão')
    plt.title(f'Gráfico de Precisão-Revocação para Consulta {i}')
    plt.legend()
    plt.grid(True)
    plt.show()

#Calcular a media 
media_precisao = np.mean(valores_interpolados_por_consulta, axis=0)
#Plotar o grafico da media 
plt.plot(niveis_revocacao, media_precisao, marker='o', linestyle='-', label='Média de Todas as Consultas')
plt.xlabel('Revocação')
plt.ylabel('Precisão')
plt.title('Média de Precisão-Revocação para Todas as Consultas')
plt.legend()
plt.grid(True)
plt.show()

"""
Os calculos estão errados, os gráficos não dão igual aos do enunciado 

"""