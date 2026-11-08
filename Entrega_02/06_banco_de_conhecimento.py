"""
Projeto 6: Banco de Conhecimentos
Algoritmos: Encadeamento para Frente (Forward Chaining) e Encadeamento para Trás (Backward Chaining)
Problemas Abordados:
 1. Problema Alternativo: Sistema Especialista para Diagnóstico de Falhas de TI
 2. Problema do Professor: Dedução Lógica no Mundo do Wumpus (Agentes Lógicos)
"""

class BaseDeConhecimento:
    def __init__(self):
        self.fatos = set()
        self.regras = [] # Formato: ( [lista_de_premissas], conclusao )

    def adicionar_fato(self, fato):
        self.fatos.add(fato)

    def adicionar_regra(self, premissas, conclusao):
        self.regras.append((premissas, conclusao))

    def encadeamento_para_frente(self, objetivo=None):
        """
        Dedução guiada por dados (Data-driven).
        Parte dos fatos conhecidos e aplica as regras até esgotar as inferências
        ou até encontrar o objetivo.
        """
        fatos_inferidos = []
        adicionou_novo_fato = True
        
        while adicionou_novo_fato:
            adicionou_novo_fato = False
            for premissas, conclusao in self.regras:
                # Se todas as premissas da regra são verdades absolutas (estão nos fatos)
                if all(p in self.fatos for p in premissas):
                    # E a conclusão ainda não foi inferida
                    if conclusao not in self.fatos:
                        self.fatos.add(conclusao)
                        fatos_inferidos.append(conclusao)
                        adicionou_novo_fato = True
                        
                        if objetivo and conclusao == objetivo:
                            return True, fatos_inferidos
                            
        if objetivo:
            return False, fatos_inferidos
        return True, fatos_inferidos

    def encadeamento_para_tras(self, objetivo, visitados=None):
        """
        Dedução guiada por metas (Goal-driven).
        Começa do objetivo e tenta provar suas premissas recursivamente.
        """
        if visitados is None:
            visitados = set()

        # Caso base: O objetivo já é um fato conhecido
        if objetivo in self.fatos:
            return True
        
        # Evita loops infinitos em regras cíclicas
        if objetivo in visitados:
            return False 
            
        visitados.add(objetivo)
        
        # Procura alguma regra que resulte neste objetivo
        for premissas, conclusao in self.regras:
            if conclusao == objetivo:
                todas_provadas = True
                # Tenta provar todas as premissas necessárias para esta regra
                for p in premissas:
                    if not self.encadeamento_para_tras(p, visitados):
                        todas_provadas = False
                        break
                
                if todas_provadas:
                    return True
                    
        return False

# ==========================================
# 1. EXECUÇÃO: DIAGNÓSTICO DE TI (NOVO PROBLEMA)
# ==========================================
def teste_sistema_especialista():
    print("==========================================")
    print(" TESTE 1: SISTEMA ESPECIALISTA DE TI")
    print("==========================================")
    bc = BaseDeConhecimento()
    
    # Adicionando Regras
    bc.adicionar_regra(["ping_falhou", "luz_roteador_apagada"], "falha_energia_roteador")
    bc.adicionar_regra(["ping_falhou", "luz_roteador_acesa"], "falha_provedor_internet")
    bc.adicionar_regra(["falha_provedor_internet", "dia_de_chuva"], "cabo_externo_rompido")
    bc.adicionar_regra(["cabo_externo_rompido"], "acionar_suporte_tecnico")
    
    # Inserindo Fatos Observados (Sintomas)
    bc.adicionar_fato("ping_falhou")
    bc.adicionar_fato("luz_roteador_acesa")
    bc.adicionar_fato("dia_de_chuva")
    
    # Testando Encadeamento para Trás (Pergunta: Devemos acionar o suporte?)
    objetivo = "acionar_suporte_tecnico"
    resultado = bc.encadeamento_para_tras(objetivo)
    print(f"Pergunta: A ação '{objetivo}' é necessária?")
    print(f"Resposta via Encadeamento para Trás: {'SIM' if resultado else 'NÃO'}")

# ==========================================
# 2. EXECUÇÃO: MUNDO DO WUMPUS (PROBLEMA DO PROFESSOR)
# ==========================================
def teste_mundo_wumpus():
    print("\n==========================================")
    print(" TESTE 2: DEDUÇÃO NO MUNDO DO WUMPUS")
    print("==========================================")
    bc = BaseDeConhecimento()
    
    # Regras lógicas transformadas em Cláusulas de Horn baseadas na Aula 10:
    # 1. Se não há brisa em [1,2], então não há poço em [2,2]
    bc.adicionar_regra(["nao_B12"], "nao_P22")
    
    # 2. Se há brisa em [2,1] e já sabemos que não há poço em [2,2], o poço DEVE estar em [3,1]
    bc.adicionar_regra(["B21", "nao_P22"], "P31")
    
    # 3. Se há fedor em [1,2] e não há fedor em [2,1], o Wumpus DEVE estar em [1,3]
    bc.adicionar_regra(["S12", "nao_S21"], "W13")
    
    # Fatos Observados pelo Agente enquanto navegava (Percepções)
    bc.adicionar_fato("nao_B12") # Agente não sentiu brisa em [1,2]
    bc.adicionar_fato("B21")     # Agente sentiu brisa em [2,1]
    bc.adicionar_fato("S12")     # Agente sentiu fedor em [1,2]
    bc.adicionar_fato("nao_S21") # Agente não sentiu fedor em [2,1]
    
    # Executando Encadeamento para Frente para ver tudo que o Agente descobre
    _, novas_descobertas = bc.encadeamento_para_frente()
    
    print("Fatos iniciais conhecidos pelo Agente:")
    print(list(bc.fatos - set(novas_descobertas)))
    print("\nDeduções feitas pelo Agente (Forward Chaining):")
    for d in novas_descobertas:
        if d == "P31":
            print(" -> O Agente deduziu que há um POÇO em [3,1]!")
        elif d == "W13":
            print(" -> O Agente deduziu que o WUMPUS está em [1,3]!")
        elif d == "nao_P22":
            print(" -> O Agente deduziu que a casa [2,2] é SEGURA (sem poço).")

if __name__ == "__main__":
    teste_sistema_especialista()
    teste_mundo_wumpus()