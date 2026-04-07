import math
import random

def calcular_fitness(bits, itens, capacidade_w):
    valor_total = 0
    peso_total = 0
    for i in range(len(bits)):
        if bits[i] == 1:
            valor_total += itens[i]['valor']
            peso_total += itens[i]['peso']
    
    # Se estourar o peso, retorna fitness 0 e o peso para controle
    if peso_total > capacidade_w:
        return 0, peso_total
    return valor_total, peso_total

def executar_tempera(itens, capacidade_w, t0, taxa, t_min):
    n = len(itens)
    # Começamos com uma mochila vazia (que é sempre válida)
    atual = [0] * n 
    v_atual, p_atual = calcular_fitness(atual, itens, capacidade_w)
    
    melhor_est = list(atual)
    v_melhor = v_atual
    
    t = t0
    iteracao_total = 0
    iteracao_convergencia = 0
    L = n * 2 # Definimos o equilíbrio térmico para explorar mais

    while t > t_min:
        for _ in range(L):
            iteracao_total += 1
            vizinho = list(atual)
            idx = random.randint(0, n - 1)
            vizinho[idx] = 1 - vizinho[idx] 
            
            v_viz, p_viz = calcular_fitness(vizinho, itens, capacidade_w)
            
            # Rejeitamos vizinhos que estouram o peso imediatamente
            if p_viz > capacidade_w:
                continue 

            delta = v_viz - v_atual
            
            # Critério de Metrópolis é usado apenas para soluções válidas
            if delta > 0 or (t > 0 and random.random() < math.exp(delta / t)):
                atual, v_atual = vizinho, v_viz
                
                if v_atual > v_melhor:
                    v_melhor = v_atual
                    melhor_est = list(atual)
                    iteracao_convergencia = iteracao_total
        
        t *= taxa 
        
    return v_melhor, iteracao_convergencia