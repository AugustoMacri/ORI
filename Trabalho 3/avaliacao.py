"""
Modelo de avalicação com gráficos 

Nome: Augusto Fernandes Macri
Matrícula: 12111BSI221
"""
import sys

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

"""# Teste para a consulta se foi ou nao bem sucedida
print(f"Número de consultas: {num_consultas}")
print("Respostas ideais:")
print(respostas_ideais)
print("Respostas do sistema:")
print(respostas_sistema)"""

#Calcular Precisão e Revocação para cada consulta 
def calcular_prec_revoc(respostas_ideal, resposta_sistema):
    documentos_recuperados = len(resposta_sistema)
    documentos_relevantes_recuperados = len(set(resposta_sistema).intersection(set(respostas_ideal)))

    precisao = documentos_relevantes_recuperados / documentos_recuperados if documentos_recuperados > 0 else 0 #calculo da precisao para cada consulta
    revocacao = documentos_relevantes_recuperados / len(respostas_ideal) if len(respostas_ideal) > 0 else 0 #calculo da revocacao para cada consulta

    return precisao, revocacao

"""#Teste para uma única consulta
consulta = 0  
precisao, revocacao = calcular_prec_revoc(respostas_ideais[consulta], respostas_sistema[consulta])
print(f"Consulta {consulta + 1}:")
print(f"Precisão: {precisao}")
print(f"Revocação: {revocacao}")"""

#Calcular precisão e revocação para todas as consultas
result_precisao = []
reult_revoc = []

for i in range(num_consultas):
    precisao, revocacao = calcular_prec_revoc(respostas_ideais[i], respostas_sistema[i])
    result_precisao.append(precisao)
    reult_revoc.append(revocacao)

"""#Teste todas as consultas
for i, (p, r) in enumerate(zip(result_precisao, reult_revoc)):
    print(f"Consulta {i + 1}: Precisao: {p}, Revocacao: {r}")"""

#Interpolação da prec e revoc
def interpolar_valores(precisao, revocacao):
    niveis_revocacao = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # Níveis de revocação de 0 a 1 em incrementos de 0.1
    valores_interp = []

    for nivel in niveis_revocacao:
        max_precisao = max([p for r, p in zip(revocacao, precisao) if r >= nivel], default=0)
        valores_interp.append(max_precisao)

    return valores_interp

#Exemplo para uma consulta específica (altere para iterar sobre todas as consultas):
consulta = 0  #Índice da consulta
valores_interpolados_por_consulta = []


