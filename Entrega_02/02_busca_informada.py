"""
Projeto 2: Busca Informada
Algoritmo: Busca A* Ponderado (Weighted A*)
Problemas Abordados:
 1. Problema Alternativo: Quebra-Cabeça de 15 Peças (15-Puzzle)
 2. Problema do Professor: Mapa da Romênia (com Distância em Linha Reta)
"""
import heapq

# ==========================================
# 1. DEFINIÇÃO DO PROBLEMA: MAPA DA ROMÊNIA
# ==========================================
GRAFO_ROMENIA_CUSTOS = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Oradea': 71, 'Arad': 75},
    'Oradea': {'Sibiu': 151, 'Zerind': 71},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

# Heurística: Distância em linha reta (SLD) até Bucareste
H_SLD_BUCHAREST = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161,
    'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244,
    'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

def sucessores_romenia_custo(estado):
    """Retorna lista de tuplas (vizinho, custo_da_aresta)"""
    return [(vizinho, custo) for vizinho, custo in GRAFO_ROMENIA_CUSTOS.get(estado, {}).items()]

def heuristica_romenia(estado):
    """Retorna o valor da heurística (linha reta até Bucharest)"""
    return H_SLD_BUCHAREST.get(estado, float('inf'))

# ==========================================
# 2. DEFINIÇÃO DO PROBLEMA: 15-PUZZLE
# ==========================================
def heuristica_manhattan_15puzzle(estado):
    """Calcula a Distância de Manhattan para o 15-puzzle."""
    # Objetivo: (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    meta = {val: (divmod(val-1, 4)) for val in range(1, 16)}
    meta[0] = (3, 3) # O vazio (0) fica na posição inferior direita (linha 3, coluna 3)
    
    distancia = 0
    for i, val in enumerate(estado):
        if val != 0:
            gx, gy = meta[val]
            x, y = divmod(i, 4)
            distancia += abs(x - gx) + abs(y - gy)
    return distancia

def sucessores_15puzzle(estado):
    """Gera sucessores válidos para o 15-Puzzle. Retorna (novo_estado, custo=1)"""
    sucessores = []
    idx_vazio = estado.index(0)
    x, y = divmod(idx_vazio, 4)
    
    # Movimentos: Cima, Baixo, Esquerda, Direita
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in movimentos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 4 and 0 <= ny < 4:
            novo_idx = nx * 4 + ny
            novo_estado = list(estado)
            # Troca o vazio com a peça adjacente
            novo_estado[idx_vazio], novo_estado[novo_idx] = novo_estado[novo_idx], novo_estado[idx_vazio]
            # O custo de mover uma peça é sempre 1
            sucessores.append((tuple(novo_estado), 1))
            
    return sucessores

# ==========================================
# 3. ALGORITMO GENÉRICO: WEIGHTED A*
# ==========================================
def weighted_a_star(estado_inicial, objetivo_func, func_sucessores, func_heuristica, peso=1.5):
    """
    Busca A* Ponderada genérica.
    f(n) = g(n) + W * h(n)
    Um peso W > 1 torna a busca mais rápida que o A* clássico, mas relaxa a garantia de otimalidade.
    """
    # Fila de prioridade armazena tuplas: (f_n, id_criacao, estado, caminho, g_n)
    # id_criacao serve apenas para desempatar nós com o mesmo f_n sem dar erro de comparação de estado
    contador = 0 
    
    h_inicial = func_heuristica(estado_inicial)
    f_inicial = 0 + (peso * h_inicial)
    
    fronteira = [(f_inicial, contador, estado_inicial, [estado_inicial], 0)]
    visitados = {estado_inicial: 0} # Armazena estado: menor_g_n_encontrado
    
    nos_expandidos = 0
    
    while fronteira:
        f_n, _, estado_atual, caminho, g_atual = heapq.heappop(fronteira)
        nos_expandidos += 1
        
        if objetivo_func(estado_atual):
            return caminho, g_atual, nos_expandidos
            
        for vizinho, custo_aresta in func_sucessores(estado_atual):
            novo_g = g_atual + custo_aresta
            
            # Se o vizinho nunca foi visitado ou se encontramos um caminho mais barato até ele
            if vizinho not in visitados or novo_g < visitados[vizinho]:
                visitados[vizinho] = novo_g
                h_vizinho = func_heuristica(vizinho)
                novo_f = novo_g + (peso * h_vizinho) # Equação do Weighted A*
                
                contador += 1
                heapq.heappush(fronteira, (novo_f, contador, vizinho, caminho + [vizinho], novo_g))
                
    return None, 0, nos_expandidos

# ==========================================
# 4. EXECUÇÃO DOS TESTES
# ==========================================
if __name__ == "__main__":
    print("==========================================")
    print(" TESTE 1: MAPA DA ROMÊNIA (Weighted A*)")
    print("==========================================")
    inicio_romenia = 'Arad'
    objetivo_romenia = lambda estado: estado == 'Bucharest'
    
    # Testando com W = 1.0 (A* Clássico Ótimo) e W = 2.0 (Ganhando velocidade)
    for w in [1.0, 2.0]:
        caminho, custo_total, nos = weighted_a_star(inicio_romenia, objetivo_romenia, sucessores_romenia_custo, heuristica_romenia, peso=w)
        if caminho:
            print(f"\n--- Peso (W) = {w} ---")
            print(f"Caminho: {' -> '.join(caminho)}")
            print(f"Custo Real da Viagem (g): {custo_total}km")
            print(f"Nós Expandidos: {nos}")


    print("\n==========================================")
    print(" TESTE 2: 15-PUZZLE (Weighted A*)")
    print("==========================================")
    # 0 é o espaço vazio. Configuração inicial bagunçada, mas solucionável
    estado_inicio_15 = (1, 2, 3, 4, 
                        5, 6, 7, 8, 
                        9, 10, 0, 11, 
                        13, 14, 15, 12)
                        
    estado_objetivo_15 = (1, 2, 3, 4, 
                          5, 6, 7, 8, 
                          9, 10, 11, 12, 
                          13, 14, 15, 0)
                          
    objetivo_15 = lambda estado: estado == estado_objetivo_15
    
    # Usando um peso maior (W=2.0) para resolver o 15-puzzle de forma viável na memória
    caminho_15, passos_15, nos_15 = weighted_a_star(estado_inicio_15, objetivo_15, sucessores_15puzzle, heuristica_manhattan_15puzzle, peso=2.0)
    
    if caminho_15:
        print(f"Solução encontrada em {passos_15} movimentos.")
        print(f"Nós Expandidos: {nos_15}")
        print("Sequência das 3 últimas posições:")
        for estado in caminho_15[-3:]:
            print(f" {estado[0:4]}\n {estado[4:8]}\n {estado[8:12]}\n {estado[12:16]}\n")
    else:
        print("Solução não encontrada.")
