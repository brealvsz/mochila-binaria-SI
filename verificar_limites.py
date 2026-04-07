def calcular_limite_guloso(itens, capacidade_w):
    # Calcula a eficiência (valor/peso) e ordena do maior para o menor
    # Usamos get() para suportar tanto a chave 'peso' quanto 'weight'
    itens_ordenados = sorted(
        itens, 
        key=lambda x: x['valor'] / (x.get('peso') or x.get('weight')), 
        reverse=True
    )
    
    valor_total = 0
    peso_total = 0
    
    for item in itens_ordenados:
        p = item.get('peso') or item.get('weight')
        v = item['valor']
        
        if peso_total + p <= capacidade_w:
            peso_total += p
            valor_total += v
            
    return valor_total