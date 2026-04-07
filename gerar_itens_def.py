import json
from ag import gerar_itens

def salvar_instancias():
    tamanhos_n = [10, 100, 200, 500, 1000]
    peso_max_item = 40
    valor_max_item = 300
    
    todas_mochilas = []
    
    for n in tamanhos_n:
        itens = gerar_itens(n, peso_max_item, valor_max_item)
        todas_mochilas.append(itens)
    
    with open("instancias_mochila.json", "w") as f:
        json.dump(todas_mochilas, f)
    
    print(f"Arquivo 'instancias_mochila.json' gerado com instâncias de tamanhos: {tamanhos_n}")

if __name__ == "__main__":
    salvar_instancias()