import random

def gerar_itens(n, peso_max, valor_max):
    return [{'peso': random.randint(1, peso_max), 'valor': random.randint(1, valor_max)} for _ in range(n)]

def gerar_populacao_inicial(tam_populacao, n, itens, capacidade_max):
    populacao = []
    
    for _ in range(tam_populacao):
        individuo = [random.choice([0, 1]) for _ in range(n)]
        peso_atual = sum(itens[i]['peso'] for i in range(n) if individuo[i] == 1)

        if peso_atual > capacidade_max:
            
            itens_na_mochila = [i for i in range(n) if individuo[i] == 1]
            random.shuffle(itens_na_mochila)
            
            for i in itens_na_mochila:
                individuo[i] = 0 
                peso_atual -= itens[i]['peso']
                
                if peso_atual <= capacidade_max:
                    break 
                    
        populacao.append(individuo)

    return populacao

def calcular_fitness(individuo, itens, capacidade_max):
    peso_total = sum(itens[i]['peso'] for i in range(len(individuo)) if individuo[i]==1)
    valor_total = sum(itens[i]['valor'] for i in range(len(individuo)) if individuo[i]==1)

    if peso_total > capacidade_max:
        return 0
    return valor_total
 
def selecao(populacao, itens, capacidade_max, taxa_mutacao, tam_torneio):

    selecionados = random.sample(populacao, tam_torneio)
    if random.random() < taxa_mutacao:
            sobrevivente = random.choice(selecionados)
            return sobrevivente

    melhor = max(selecionados, key=lambda individuo: calcular_fitness(individuo, itens, capacidade_max))
    return melhor

def cruzamento(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

def mutacao(individuo, taxa_mutacao, capacidade_max, itens):
    for i in range (len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]
            peso_total = sum(itens[i]['peso'] for i in range(len(individuo)) if individuo[i]==1)
            if peso_total > capacidade_max:
                individuo[i] = 1 - individuo[i]
    
    return individuo

def executar_ag(n, capacidade_max, itens, tam_populacao, num_geracoes, taxa_mutacao):
    populacao = gerar_populacao_inicial(tam_populacao, n, itens, capacidade_max)
    
    melhor_fitness_global = -1
    tam_torneio = 3
    geracao_melhor_valor = 0
    historico_recordes = []

    for geracao in range(num_geracoes):
        
        melhor_da_geracao = max(populacao, key=lambda individuo: calcular_fitness(individuo, itens, capacidade_max))
        fitness_atual = calcular_fitness(melhor_da_geracao, itens, capacidade_max)

        if fitness_atual > melhor_fitness_global:
            melhor_fitness_global = fitness_atual
            geracao_melhor_valor = geracao
            

        historico_recordes.append(melhor_fitness_global)

        nova_populacao = []
        #nova_populacao.append(melhor_da_geracao[:])

        while len(nova_populacao) < tam_populacao:
            pai1 = selecao(populacao, itens, capacidade_max, taxa_mutacao, tam_torneio)
            pai2 = selecao(populacao, itens, capacidade_max, taxa_mutacao, tam_torneio)

            filho1, filho2 = cruzamento(pai1, pai2)

            filho1 = mutacao(filho1, taxa_mutacao, capacidade_max, itens)
            filho2 = mutacao(filho2, taxa_mutacao, capacidade_max, itens)
            
            nova_populacao.extend([filho1, filho2])
        populacao = nova_populacao[:tam_populacao]

    melhor_populacao_final = max(populacao, key=lambda ind: calcular_fitness(ind, itens, capacidade_max))
    fitness_final = calcular_fitness(melhor_populacao_final, itens, capacidade_max)

    if fitness_final > melhor_fitness_global:
        melhor_fitness_global = fitness_final
        historico_recordes[-1] = melhor_fitness_global
        geracao_melhor_valor = num_geracoes
    
    return melhor_populacao_final, fitness_final, historico_recordes, geracao_melhor_valor