"""
Projeto 1: Busca Não Informada
Algoritmo: Busca em Profundidade Iterativa (IDDFS)
Problemas Abordados:
 1. Problema Alternativo: Jarros de Água (4 Litros)
 2. Problema do Professor: Mapa da Romênia (De Arad a Bucareste)
"""

# ==========================================
# 1. DEFINIÇÃO DO PROBLEMA: MAPA DA ROMÊNIA
# ==========================================
GRAFO_ROMENIA = {
    'Arad': ['Zerind', 'Sibiu', 'Timisoara'],
    'Zerind': ['Oradea', 'Arad'],
    'Oradea': ['Sibiu', 'Zerind'],
    'Sibiu': ['Arad', 'Oradea', 'Fagaras', 'Rimnicu Vilcea'],
    'Fagaras': ['Sibiu', 'Bucharest'],
    'Rimnicu Vilcea': ['Sibiu', 'Craiova', 'Pitesti'],
    'Timisoara': ['Arad', 'Lugoj'],
    'Lugoj': ['Timisoara', 'Mehadia'],
    'Mehadia': ['Lugoj', 'Drobeta'],
    'Drobeta': ['Mehadia', 'Craiova'],
    'Craiova': ['Drobeta', 'Rimnicu Vilcea', 'Pitesti'],
    'Pitesti': ['Rimnicu Vilcea', 'Craiova', 'Bucharest'],
    'Bucharest': ['Fagaras', 'Pitesti', 'Giurgiu', 'Urziceni'],
    'Giurgiu': ['Bucharest'],
    'Urziceni': ['Bucharest', 'Hirsova', 'Vaslui'],
    'Hirsova': ['Urziceni', 'Eforie'],
    'Eforie': ['Hirsova'],
    'Vaslui': ['Urziceni', 'Iasi'],
    'Iasi': ['Vaslui', 'Neamt'],
    'Neamt': ['Iasi']
}

def sucessores_romenia(estado):
    """Gera os vizinhos de uma cidade no mapa da Romênia."""
    return GRAFO_ROMENIA.get(estado, [])

# ==========================================
# 2. DEFINIÇÃO DO PROBLEMA: JARROS DE ÁGUA
# ==========================================
def sucessores_jarros(estado):
    """
    Gera todos os estados sucessores válidos para os jarros de 5L e 3L.
    Estado: (j5, j3) indicando o volume em cada jarro.
    """
    j5, j3 = estado
    sucessores = []
    
    if j5 < 5: sucessores.append((5, j3)) # Encher o jarro de 5L
    if j3 < 3: sucessores.append((j5, 3)) # Encher o jarro de 3L
    if j5 > 0: sucessores.append((0, j3)) # Esvaziar o jarro de 5L
    if j3 > 0: sucessores.append((j5, 0)) # Esvaziar o jarro de 3L
    
    # Despejar de 5L para 3L
    if j5 > 0 and j3 < 3:
        transferencia = min(j5, 3 - j3)
        sucessores.append((j5 - transferencia, j3 + transferencia))
        
    # Despejar de 3L para 5L
    if j3 > 0 and j5 < 5:
        transferencia = min(j3, 5 - j5)
        sucessores.append((j5 + transferencia, j3 - transferencia))

    return sucessores

# ==========================================
# 3. ALGORITMO GENÉRICO: IDDFS
# ==========================================
def dls(estado, objetivo_func, limite, caminho, visitados, func_sucessores):
    """Busca em Profundidade Limitada Genérica (DLS)."""
    if objetivo_func(estado):
        return caminho

    if limite == 0:
        return "Corte" 
    
    ocorreu_corte = False
    
    for sucessor in func_sucessores(estado):
        # Evita ciclos dentro do mesmo ramo da árvore
        if sucessor not in visitados:
            visitados.add(sucessor)
            resultado = dls(sucessor, objetivo_func, limite - 1, caminho + [sucessor], visitados, func_sucessores)
            visitados.remove(sucessor) # Backtrack da lista de visitados
            
            if resultado == "Corte":
                ocorreu_corte = True
            elif resultado is not None:
                return resultado
                
    return "Corte" if ocorreu_corte else None

def iddfs(estado_inicial, objetivo_func, func_sucessores, limite_maximo=20):
    """Busca em Profundidade Iterativa Genérica (IDDFS)."""
    for profundidade in range(limite_maximo):
        visitados = {estado_inicial}
        resultado = dls(estado_inicial, objetivo_func, profundidade, [estado_inicial], visitados, func_sucessores)
        
        if resultado != "Corte" and resultado is not None:
            return resultado, profundidade
            
    return None, limite_maximo

# ==========================================
# 4. EXECUÇÃO DOS TESTES
# ==========================================
if __name__ == "__main__":
    print("==========================================")
    print(" TESTE 1: PROBLEMA DOS JARROS DE ÁGUA")
    print("==========================================")
    inicio_jarros = (0, 0)
    # Objetivo: jarro de 5L (índice 0) deve conter exatamente 4 litros
    objetivo_jarros = lambda estado: estado[0] == 4 
    
    solucao_jarros, prof_jarros = iddfs(inicio_jarros, objetivo_jarros, sucessores_jarros)
    
    if solucao_jarros:
        print(f"Solução encontrada na profundidade {prof_jarros}:")
        for i, estado in enumerate(solucao_jarros):
            print(f"Passo {i}: 5L={estado[0]}, 3L={estado[1]}")
    else:
        print("Solução não encontrada.")

    print("\n============================================")
    print(" TESTE 2: MAPA DA ROMÊNIA (Arad -> Bucharest)")
    print("==============================================")
    inicio_romenia = 'Arad'
    objetivo_romenia = lambda estado: estado == 'Bucharest'
    
    solucao_romenia, prof_romenia = iddfs(inicio_romenia, objetivo_romenia, sucessores_romenia)
    
    if solucao_romenia:
        print(f"Solução ótima em passos encontrada na profundidade {prof_romenia}:")
        print(" -> ".join(solucao_romenia))
    else:
        print("Solução não encontrada.")