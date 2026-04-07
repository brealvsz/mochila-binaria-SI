import matplotlib.pyplot as plt
import random
import time
from gerador_mochila import carregar_instancias
from tempera import executar_tempera
from verificar_limites import calcular_limite_guloso

def gerar_grafico(resultados, n, w_usado, limite_verde, tipo="desempenho", labels_sensib=None):
    plt.figure(figsize=(10, 6))
    if tipo == "sensibilidade":
        plt.plot(labels_sensib, resultados, marker='s', linestyle='-', color='g', label='Resultado por Configuração')
        plt.title(f'Teste de Sensibilidade: Parâmetros (n={n}, W={w_usado})')
        plt.xlabel('Configuração (Temperatura / Taxa)')
    else:
        eixo_x = list(range(1, len(resultados) + 1))
        plt.plot(eixo_x, resultados, marker='o', linestyle='-', color='r', label='Valor da Rodada')
        plt.title(f'Desempenho: {n} itens | Capacidade W={w_usado}')
        plt.xlabel('Número da Rodada')
        plt.xticks(eixo_x)

    melhor_v = max(resultados)
    plt.axhline(y=melhor_v, color='b', linestyle='--', alpha=0.6, label=f'Melhor ({melhor_v})')
    plt.axhline(y=limite_verde, color='limegreen', linestyle=':', linewidth=2, label=f'Guloso ({limite_verde})')
    plt.ylabel('Valor Total (Fitness)')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='lower right')
    plt.show()

def iniciar_experimento():
    instancias = carregar_instancias()
    RODADAS = 20
    capacidades = {10: 50, 100: 250, 500: 1000}

    # --- 1. TESTE DE SENSIBILIDADE ---
    print(f"\nExecutando Sensibilidade (n=100, W=250)...")
    itens_100 = instancias[100]
    w_sensib = capacidades[100]
    limite_100 = calcular_limite_guloso(itens_100, w_sensib)
    
    # Configurações equilibradas: Note que aumentamos a taxa para as T maiores
    configs_labels = ["T100/0.9", "T500/0.95", "T1000/0.98", "T5000/0.99"]
    configs_params = [(100, 0.9), (500, 0.95), (1000, 0.98), (5000, 0.99)]
    resultados_sensibilidade = []

    for t0, taxa in configs_params:
        v, _ = executar_tempera(itens_100, w_sensib, t0, taxa, 0.01)
        resultados_sensibilidade.append(v)
        print(f"  Config {t0}/{taxa} -> Melhor: {v}")
    
    gerar_grafico(resultados_sensibilidade, 100, w_sensib, limite_100, tipo="sensibilidade", labels_sensib=configs_labels)

    # --- 2. BATERIA DE DESEMPENHO ---
    for n in [10, 100, 500]:
        W_ATUAL = capacidades[n]
        print(f"\n" + "="*40 + f"\nTESTANDO: {n} ITENS | W={W_ATUAL}\n" + "="*40)
        limite_teorico = calcular_limite_guloso(instancias[n], W_ATUAL)
        resultados_valores, tempos, iters = [], [], []
        
        for i in range(RODADAS):
            inicio_t = time.time()
            valor, iter_conv = executar_tempera(instancias[n], W_ATUAL, 5000, 0.99, 0.01)
            fim_t = time.time()
            
            resultados_valores.append(valor)
            tempos.append(fim_t - inicio_t)
            iters.append(iter_conv)
            print(f"  Rodada {i+1} ok...", end='\r')

        print(f"\n\nMédias: Tempo {sum(tempos)/RODADAS:.4f}s | Conv. {sum(iters)/RODADAS:.1f}")
        gerar_grafico(resultados_valores, n, W_ATUAL, limite_teorico)

if __name__ == "__main__":
    random.seed(1000)
    iniciar_experimento()