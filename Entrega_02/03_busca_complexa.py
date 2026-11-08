"""
Projeto 3: Busca Complexa / Local
Algoritmo: Busca Tabu (Tabu Search)
Problemas Abordados:
 1. Problema Alternativo: Caixeiro Viajante (TSP - Traveling Salesperson Problem)
 2. Problema do Professor: Maximização de Função f(x) = -x^2 + 4x + 1
"""
import random
import copy

# ==========================================
# 1. DEFINIÇÃO DO PROBLEMA: MAXIMIZAÇÃO DE FUNÇÃO
# ==========================================
# f(x) = -x^2 + 4x + 1
def avaliar_funcao(x):
    """Calcula o valor da função f(x)."""
    return -(x**2) + 4*x + 1

def vizinhos_funcao(x):
    """Gera os vizinhos imediatos (x-1 e x+1) restritos ao domínio [0, 5]."""
    vizinhos = []
    if x > 0:
        vizinhos.append(x - 1)
    if x < 5:
        vizinhos.append(x + 1)
    return vizinhos

# =================================================
# 2. DEFINIÇÃO DO PROBLEMA: CAIXEIRO VIAJANTE (TSP)
# =============================================
CIDADES = ['A', 'B', 'C', 'D', 'E']
DISTANCIAS_TSP = {
    ('A', 'B'): 10, ('A', 'C'): 15, ('A', 'D'): 20, ('A', 'E'): 25,
    ('B', 'A'): 10, ('B', 'C'): 35, ('B', 'D'): 25, ('B', 'E'): 30,
    ('C', 'A'): 15, ('C', 'B'): 35, ('C', 'D'): 30, ('C', 'E'): 5,
    ('D', 'A'): 20, ('D', 'B'): 25, ('D', 'C'): 30, ('D', 'E'): 15,
    ('E', 'A'): 25, ('E', 'B'): 30, ('E', 'C'): 5,  ('E', 'D'): 15
}

def avaliar_tsp(rota):
    """
    Calcula a distância total da rota.
    Retorna o valor negativo para transformar o problema de minimização em maximização (para usar o mesmo algoritmo genérico).
    """
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += DISTANCIAS_TSP[(rota[i], rota[i+1])]
    distancia_total += DISTANCIAS_TSP[(rota[-1], rota[0])] # Volta à cidade de origem
    return -distancia_total # Retorna negativo para maximizar (menor distância = maior valor)

def vizinhos_tsp(rota):
    """
    Gera vizinhos trocando a posição de duas cidades na rota (Swap).
    A cidade inicial e final da permutação continuam as mesmas da estrutura lógica.
    """
    vizinhos = []
    n = len(rota)
    for i in range(n):
        for j in range(i + 1, n):
            vizinho = copy.deepcopy(rota)
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            vizinhos.append(vizinho)
    return vizinhos

# ==========================================
# 3. ALGORITMO GENÉRICO: BUSCA TABU
# ==========================================
def tabu_search(estado_inicial, func_avaliacao, func_vizinhos, iteracoes_max=50, tamanho_tabu=5):
    """
    Busca Tabu Genérica.
    Mantém uma 'lista tabu' de estados recentemente visitados para evitar ciclos e escapar de ótimos locais.
    """
    melhor_estado_global = estado_inicial
    melhor_valor_global = func_avaliacao(estado_inicial)
    
    estado_atual = estado_inicial
    lista_tabu = []
    
    for _ in range(iteracoes_max):
        vizinhos = func_vizinhos(estado_atual)
        
        # Filtra os vizinhos que estão na lista tabu
        vizinhos_validos = [v for v in vizinhos if v not in lista_tabu]
        
        if not vizinhos_validos:
            break # Preso, sem movimentos permitidos
            
        # Encontra o melhor vizinho (mesmo que seja pior que o estado atual - característica da busca local)
        melhor_vizinho = vizinhos_validos[0]
        melhor_valor_vizinho = func_avaliacao(melhor_vizinho)
        
        for vizinho in vizinhos_validos[1:]:
            valor = func_avaliacao(vizinho)
            if valor > melhor_valor_vizinho:
                melhor_vizinho = vizinho
                melhor_valor_vizinho = valor
                
        estado_atual = melhor_vizinho
        
        # Atualiza a lista tabu
        lista_tabu.append(estado_atual)
        if len(lista_tabu) > tamanho_tabu:
            lista_tabu.pop(0) # Remove o mais antigo (FIFO)
            
        # Atualiza o melhor global encontrado até agora
        if melhor_valor_vizinho > melhor_valor_global:
            melhor_estado_global = estado_atual
            melhor_valor_global = melhor_valor_vizinho
            
    return melhor_estado_global, melhor_valor_global

# ==========================================
# 4. EXECUÇÃO DOS TESTES
# ==========================================
if __name__ == "__main__":
    print("==========================================")
    print(" TESTE 1: MAXIMIZAÇÃO DA FUNÇÃO f(x)")
    print("==========================================")
    inicio_funcao = 0 # Valor inicial x = 0
    melhor_x, max_f = tabu_search(inicio_funcao, avaliar_funcao, vizinhos_funcao, iteracoes_max=10, tamanho_tabu=2)
    
    print(f"Melhor valor de x encontrado: {melhor_x}")
    print(f"Valor máximo de f(x): {max_f}")

    print("\n==========================================")
    print(" TESTE 2: CAIXEIRO VIAJANTE (TSP)")
    print("==========================================")
    inicio_rota = ['A', 'B', 'C', 'D', 'E'] # Rota inicial arbitrária
    
    print(f"Rota Inicial: {' -> '.join(inicio_rota)} (Distância: {-avaliar_tsp(inicio_rota)})")
    melhor_rota, dist_maximizada = tabu_search(inicio_rota, avaliar_tsp, vizinhos_tsp, iteracoes_max=50, tamanho_tabu=10)
    
    print(f"Melhor Rota Encontrada: {' -> '.join(melhor_rota)}")
    print(f"Distância Mínima: {-dist_maximizada}") # Inverte o sinal de volta para a distância real
