"""
Modelo de avalicação com gráficos 

Nome: Augusto Fernandes Macri
Matrícula: 12111BSI221

matplotlib n funcionava, baixar:
pip install matplotlib

"""
import sys
import matplotlib.pyplot as plt

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
result_revoc = []

for i in range(num_consultas):
    precisao, revocacao = calcular_prec_revoc(respostas_ideais[i], respostas_sistema[i])
    result_precisao.append(precisao)
    result_revoc.append(revocacao)
    #print(f"Consulta {i + 1}: Precisão: {precisao}, Revocação: {revocacao}")


#Interpolação da prec e revoc
#Tá devolvendo sempre o memo valor 
#zip faz com que seja criado uma lista de tuplas onde cada tupla contem um par (revoc, prec)
niveis_revocacao = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]# Níveis de revocação de 0 a 1 em incrementos de 0.1
def interpolar_valores(precisao, revocacao):
    niveis_revocacao = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # Níveis de revocação de 0 a 1 em incrementos de 0.1
    valores_interp = []

    precisao_ordenada, revocacao_ordenada = zip(*sorted(zip(precisao, revocacao), key=lambda x: x[1]))

    print(f"Precis ord: {precisao_ordenada}")
    print(f"Revoc ord {revocacao_ordenada}")

    for nivel in niveis_revocacao:
        valores_nivel = [p for r, p in zip(revocacao_ordenada, precisao_ordenada) if r >= nivel]
        if valores_nivel:
            closest_value = min(valores_nivel, key=lambda x: abs(x - nivel))
            valores_interp.append(closest_value)
        else:
            valores_interp.append(0)

        print(f"Nível de revocação: {nivel}, Valores de precisão: {valores_nivel}")

    return valores_interp

"""a = interpolar_valores(result_precisao, result_revoc)
print(a)"""

# Interpolação da precisão e revocação para cada consulta
