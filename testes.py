import time
import random
import json
import matplotlib.pyplot as plt
from ag import executar_ag

def gerar_grafico(resultados_finais, n, melhores_resultados, w):
    plt.figure(figsize=(10, 6))
    
    testes = list(range(1, len(resultados_finais) + 1))
    
    plt.plot(testes, resultados_finais, marker='o', linestyle='-', color='r', label='Resultado Final')
    plt.plot(testes, melhores_resultados, marker='x', linestyle='', color='b', label='Melhor Solução Encontrada (Global)')

    plt.title(f'Desempenho: {n} itens | Capacidade W = {w}')
    plt.xlabel('Número do Teste')
    plt.ylabel('Valor Encontrado')
    
    plt.xticks(testes) 
    
    plt.grid(True)
    plt.legend()
    
    print("\nExibindo gráfico dos resultados finais... (Feche a janela para encerrar o programa)")
    plt.show()

def testar_ag():
    capacidade_max = 250
    tam_populacao = 100
    num_geracoes = 100
    taxa_mutacao = 0.02
    qnt_testes = 20

    try:
        with open("instancias_mochila.json", "r") as f:
            todas_mochilas = json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo 'instancias_mochila.json' não encontrado. Rode o gerador primeiro.")
        return
    
    print(f"Existem {len(todas_mochilas)} instâncias salvas.")
    escolha = int(input("Escolha qual mochila utilizar (0 a 4): "))
    
    itens = todas_mochilas[escolha]
    n_itens = len(itens)

    print(f"\nIniciando bateria de {qnt_testes} testes na Instância {escolha}...\n")

    resultados = []
    melhores_resultados = []
    tempo_total = 0
    geracoes_recorde = []

    for i in range(qnt_testes):

        tempo_inicio = time.time()
        melhor_solucao, melhor_valor, historico_evolucao, geracao_rec = executar_ag(
            n_itens, capacidade_max, itens, tam_populacao, num_geracoes, taxa_mutacao
        )
        resultados.append(melhor_valor)
        melhores_resultados.append(historico_evolucao[-1])
        geracoes_recorde.append(geracao_rec)
        tempo_fim = time.time()
        tempo_exec = tempo_fim - tempo_inicio
        tempo_total += tempo_exec

    print("\n--- Resumo Final dos Testes ---")
    print(f"Média dos valores alcançados: {sum(resultados) / qnt_testes:.2f}")
    print(f"Média de convergência - geração em que foi encontrado o melhor valor: {sum(geracoes_recorde)/qnt_testes:.2f}")
    print(f"Melhor valor absoluto entre todos os testes: {max(resultados)}")
    print(f"Pior valor entre os testes: {min(resultados)}")
    print(f"Tempo total de execução: {tempo_total:.4f} segundos")

    gerar_grafico(resultados, n_itens, melhores_resultados, capacidade_max)   


if __name__ == "__main__":
    random.seed(100)
    testar_ag()