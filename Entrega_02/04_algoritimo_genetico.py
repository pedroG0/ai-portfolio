"""
Projeto 4: Algoritmo Genético
Algoritmo: Algoritmo Genético com Order Crossover (OX) e Elitismo
Problemas Abordados:
 1. Problema Alternativo: Caixeiro Viajante (TSP) com Cruzamento Ordenado
 2. Problema do Professor: Problema das 8 Damas
"""
import random

# ==========================================
# 1. DEFINIÇÃO DO PROBLEMA: 8 DAMAS
# ==========================================
def fitness_8damas(individuo):
    """
    Avalia a aptidão (fitness) do tabuleiro das 8 Damas.
    Calcula o número de pares de damas que NÃO se atacam (máximo = 28).
    Um indivíduo é um vetor permutacional (ex: [0, 4, 7, 5, 2, 6, 1, 3])
    onde o índice é a coluna e o valor é a linha.
    """
    conflitos = 0
    n = len(individuo)
    for i in range(n):
        for j in range(i + 1, n):
            # Como usamos permutação, nunca há conflito na mesma linha ou coluna.
            # Basta checar as diagonais.
            if abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    
    # Máximo de pares possíveis em 8 damas é Combinação(8, 2) = 28.
    return 28 - conflitos

def gerar_individuo_8damas():
    """Gera um indivíduo aleatório (cromossomo) garantindo valores únicos (0 a 7)."""
    cromossomo = list(range(8))
    random.shuffle(cromossomo)
    return cromossomo

# ==========================================
# 2. DEFINIÇÃO DO PROBLEMA: CAIXEIRO VIAJANTE (TSP)
# ==========================================
CIDADES_TSP = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
# Matriz de distâncias arbitrárias para 8 cidades
DISTANCIAS = {
    (c1, c2): random.randint(10, 100) if c1 != c2 else 0
    for c1 in CIDADES_TSP for c2 in CIDADES_TSP
}
# Garantindo simetria (A->B == B->A)
for c1 in CIDADES_TSP:
    for c2 in CIDADES_TSP:
        DISTANCIAS[(c2, c1)] = DISTANCIAS[(c1, c2)]

def fitness_tsp(individuo):
    """
    Avalia a rota do TSP.
    Aptidão = 1 / Distância Total (queremos minimizar a distância, logo maximizar 1/dist).
    """
    distancia_total = 0
    n = len(individuo)
    for i in range(n - 1):
        distancia_total += DISTANCIAS[(individuo[i], individuo[i+1])]
    # Volta à origem
    distancia_total += DISTANCIAS[(individuo[-1], individuo[0])]
    
    # Penaliza severamente distância 0 (caso de erro)
    if distancia_total == 0: return 0.0001
    
    # Multiplica por 1000 apenas para os valores não ficarem muito pequenos na tela
    return 1000.0 / distancia_total

def gerar_individuo_tsp():
    """Gera uma rota aleatória válida passando por todas as 8 cidades."""
    rota = CIDADES_TSP.copy()
    random.shuffle(rota)
    return rota

# ==========================================
# 3. OPERADORES GENÉTICOS PARA PERMUTAÇÃO
# ==========================================
def selecao_torneio(populacao, func_fitness, k=3):
    """Seleciona o melhor indivíduo de um subconjunto aleatório da população."""
    competidores = random.sample(populacao, k)
    melhor = max(competidores, key=func_fitness)
    return melhor

def order_crossover(pai1, pai2):
    """
    Order Crossover (OX1): Método de cruzamento para cromossomos baseados em permutação.
    Evita repetição de genes, ideal para 8 Damas (1 rainha por linha) e TSP (1 cidade 1 vez).
    """
    tamanho = len(pai1)
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    
    filho1 = [None] * tamanho
    filho2 = [None] * tamanho
    
    # 1. Copia o segmento central diretamente dos pais
    filho1[inicio:fim+1] = pai1[inicio:fim+1]
    filho2[inicio:fim+1] = pai2[inicio:fim+1]
    
    # 2. Preenche o restante com os genes do outro pai, mantendo a ordem relativa
    def preencher_filho(filho, pai_doador):
        pos_atual = (fim + 1) % tamanho
        for gene in pai_doador:
            if gene not in filho:
                filho[pos_atual] = gene
                pos_atual = (pos_atual + 1) % tamanho
                
    # Começa a procurar a partir do fim do corte no pai doador
    pai2_reordenado = pai2[fim+1:] + pai2[:fim+1]
    pai1_reordenado = pai1[fim+1:] + pai1[:fim+1]
    
    preencher_filho(filho1, pai2_reordenado)
    preencher_filho(filho2, pai1_reordenado)
    
    return filho1, filho2

def mutacao_swap(individuo, taxa_mutacao):
    """
    Mutação por Troca (Swap Mutation).
    Troca duas posições aleatórias do cromossomo se a probabilidade for atingida.
    """
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(individuo)), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo

# ==========================================
# 4. ALGORITMO GENÉTICO GENÉRICO
# ==========================================
def algoritmo_genetico(gerador_indiv, func_fitness, tam_populacao=100, geracoes=500, taxa_mut=0.1, taxa_elite=0.1):
    """
    Estrutura clássica de AG com suporte a elitismo.
    """
    populacao = [gerador_indiv() for _ in range(tam_populacao)]
    melhor_global = None
    melhor_fitness_global = -1
    
    num_elite = int(tam_populacao * taxa_elite)
    # Garante que seja um número par para facilitar o preenchimento da prole
    if (tam_populacao - num_elite) % 2 != 0: 
        num_elite += 1
        
    for geracao in range(geracoes):
        # Ordena a população atual pelo fitness
        populacao.sort(key=func_fitness, reverse=True)
        
        melhor_da_geracao = populacao[0]
        fitness_da_geracao = func_fitness(melhor_da_geracao)
        
        # Atualiza o melhor global
        if fitness_da_geracao > melhor_fitness_global:
            melhor_global = melhor_da_geracao
            melhor_fitness_global = fitness_da_geracao
            
        nova_populacao = []
        
        # Elitismo: preserva os X% melhores para a próxima geração intactos
        nova_populacao.extend(populacao[:num_elite])
        
        # Preenche o restante com reprodução
        while len(nova_populacao) < tam_populacao:
            pai1 = selecao_torneio(populacao, func_fitness)
            pai2 = selecao_torneio(populacao, func_fitness)
            
            filho1, filho2 = order_crossover(pai1, pai2)
            
            filho1 = mutacao_swap(filho1, taxa_mut)
            filho2 = mutacao_swap(filho2, taxa_mut)
            
            nova_populacao.extend([filho1, filho2])
            
        populacao = nova_populacao
        
        # Condição de parada ideal atingida (Para as 8 Damas, 28 é a pontuação máxima)
        if melhor_fitness_global == 28 and gerador_indiv == gerar_individuo_8damas:
            return melhor_global, melhor_fitness_global, geracao
            
    return melhor_global, melhor_fitness_global, geracoes

# ==========================================
# 5. EXECUÇÃO DOS TESTES
# ==========================================
if __name__ == "__main__":
    print("==========================================")
    print(" TESTE 1: PROBLEMA DAS 8 DAMAS (AG)")
    print("==========================================")
    print("Procurando solução... (Fitness Máximo = 28)")
    solucao_8d, fit_8d, gen_8d = algoritmo_genetico(
        gerar_individuo_8damas, fitness_8damas, 
        tam_populacao=50, geracoes=200, taxa_mut=0.2
    )
    
    print(f"Melhor Indivíduo (Colunas 0 a 7, Valores = Linha): {solucao_8d}")
    print(f"Aptidão Encontrada: {fit_8d}/28 (Geração {gen_8d})")
    if fit_8d == 28:
        print("-> SUCESSO: Nenhuma dama se ataca!")
        
    print("\n==========================================")
    print(" TESTE 2: CAIXEIRO VIAJANTE (TSP) 8 Cidades")
    print("==========================================")
    
    rota_otimizada, fit_tsp, gen_tsp = algoritmo_genetico(
        gerar_individuo_tsp, fitness_tsp, 
        tam_populacao=50, geracoes=100, taxa_mut=0.1
    )
    
    distancia_final = 1000.0 / fit_tsp
    print(f"Melhor Rota: {' -> '.join(rota_otimizada)} -> {rota_otimizada[0]}")
    print(f"Distância Total Otimizada: {distancia_final:.2f}")
    print(f"Resolvido ao final de {gen_tsp} gerações.")
