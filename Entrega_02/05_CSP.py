"""
Projeto 5: CSP (Problema de Satisfação de Restrições)
Algoritmo: Heurística de Min-Conflicts (Reparo Local)
Problemas Abordados:
 1. Problema Alternativo: N-Damas (Escalável para N muito grande)
 2. Problema do Professor: Coloração do Mapa da Austrália
"""
import random

# ==========================================
# 1. ALGORITMO GENÉRICO: MIN-CONFLICTS
# ==========================================
def min_conflicts(variaveis, dominios, func_conflitos, max_passos=1000):
    """
    Algoritmo Min-Conflicts para resolução de CSP.
    Começa com uma atribuição aleatória completa e repara iterativamente
    as variáveis que violam restrições.
    """
    # 1. Atribuição inicial aleatória completa
    atribuicao = {var: random.choice(dominios[var]) for var in variaveis}
    
    for _ in range(max_passos):
        # 2. Verifica se a atribuição atual é a solução
        if func_conflitos(atribuicao) == 0:
            return atribuicao
            
        # 3. Escolhe aleatoriamente UMA variável que esteja em conflito
        vars_em_conflito = []
        for var in variaveis:
            if func_conflitos(atribuicao, var) > 0:
                vars_em_conflito.append(var)
                
        if not vars_em_conflito:
            return atribuicao # Segurança extra, não deve ocorrer se conflitos > 0
            
        var_conflituosa = random.choice(vars_em_conflito)
        
        # 4. Encontra o valor no domínio dessa variável que minimiza o número de conflitos
        min_conflitos_valor = float('inf')
        melhores_valores = []
        
        valor_original = atribuicao[var_conflituosa]
        
        for valor in dominios[var_conflituosa]:
            atribuicao[var_conflituosa] = valor
            qtd_conflitos = func_conflitos(atribuicao, var_conflituosa)
            
            if qtd_conflitos < min_conflitos_valor:
                min_conflitos_valor = qtd_conflitos
                melhores_valores = [valor]
            elif qtd_conflitos == min_conflitos_valor:
                melhores_valores.append(valor)
                
        # 5. Atribui o melhor valor (desempata aleatoriamente)
        atribuicao[var_conflituosa] = random.choice(melhores_valores)
        
    return None # Falhou após max_passos

# ==========================================
# 2. DEFINIÇÃO DO PROBLEMA: MAPA DA AUSTRÁLIA
# ==========================================
VARS_AUSTRALIA = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
DOMINIOS_AUSTRALIA = {var: ['Vermelho', 'Verde', 'Azul'] for var in VARS_AUSTRALIA}
VIZINHOS_AUSTRALIA = {
    'WA' : ['NT', 'SA'], 
    'NT' : ['WA', 'SA', 'Q'], 
    'SA' : ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q'  : ['NT', 'SA', 'NSW'], 
    'NSW': ['Q', 'SA', 'V'], 
    'V'  : ['SA', 'NSW'], 
    'T'  : []
}

def conflitos_australia(atribuicao, var_foco=None):
    """
    Calcula violações (cores iguais em vizinhos).
    Se var_foco for informada, calcula apenas as violações envolvendo ela.
    Se não, calcula os conflitos globais do mapa.
    """
    conflitos = 0
    vars_a_checar = [var_foco] if var_foco else VARS_AUSTRALIA
    
    for var in vars_a_checar:
        cor_atual = atribuicao[var]
        for vizinho in VIZINHOS_AUSTRALIA[var]:
            if atribuicao[vizinho] == cor_atual:
                conflitos += 1
                
    # Se calculou global, divide por 2 pois cada aresta (conflito) é contada duas vezes (A-B e B-A)
    return conflitos if var_foco else conflitos // 2

# ==========================================
# 3. DEFINIÇÃO DO PROBLEMA: N-DAMAS (MIN-CONFLICTS)
# ==========================================
def criar_problema_ndamas(n):
    """Gera variáveis e domínios para N-Damas."""
    variaveis = list(range(n)) # Variáveis são as colunas (0 a N-1)
    dominios = {var: list(range(n)) for var in variaveis} # Valores são as linhas (0 a N-1)
    return variaveis, dominios

def conflitos_ndamas(atribuicao, var_foco=None):
    """
    Calcula os ataques entre damas.
    atribuicao: {coluna: linha}
    """
    conflitos = 0
    vars_a_checar = [var_foco] if var_foco is not None else atribuicao.keys()
    
    for col1 in vars_a_checar:
        linha1 = atribuicao[col1]
        for col2, linha2 in atribuicao.items():
            if col1 == col2: continue
            
            # Checa conflito de mesma linha (horizontal)
            if linha1 == linha2:
                conflitos += 1
            # Checa conflito de diagonais
            elif abs(linha1 - linha2) == abs(col1 - col2):
                conflitos += 1
                
    return conflitos if var_foco is not None else conflitos // 2

# ==========================================
# 4. EXECUÇÃO DOS TESTES
# ==========================================
if __name__ == "__main__":
    print("==========================================")
    print(" TESTE 1: MAPA DA AUSTRÁLIA (Min-Conflicts)")
    print("==========================================")
    
    solucao_mapa = min_conflicts(VARS_AUSTRALIA, DOMINIOS_AUSTRALIA, conflitos_australia)
    
    if solucao_mapa:
        print("Solução encontrada para Coloração de Mapa:")
        for estado, cor in solucao_mapa.items():
            print(f" {estado}: {cor}")
        print(f"Conflitos Finais: {conflitos_australia(solucao_mapa)}")
    else:
        print("Solução não encontrada.")

    print("\n==========================================")
    print(" TESTE 2: N-DAMAS ESCALADO (N=50) (Min-Conflicts)")
    print("==========================================")
    N = 8
    print(f"Tentando alocar {N} Damas em um tabuleiro {N}x{N}...")
    vars_ndamas, dominios_ndamas = criar_problema_ndamas(N)
    
  
    solucao_damas = min_conflicts(vars_ndamas, dominios_ndamas, conflitos_ndamas, max_passos=5000)
    
    if solucao_damas:
        print(f"Solução encontrada para {N}-Damas!")
        print(f"Conflitos Totais: {conflitos_ndamas(solucao_damas)}")
        print("Amostra das posições (Coluna: Linha):")
        amostra = {k: solucao_damas[k] for k in range(N if N < 10  else 10)}
        print(f" Primeiras {N if N < 10  else 10} colunas -> {amostra} ...")
    else:
        print("Solução não encontrada dentro do limite de passos.")