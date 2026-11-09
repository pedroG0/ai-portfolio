"""
Executor Principal - Portfólio de Inteligência Artificial (FGA0221)
Pedro Gomes Oliveira (Matrícula: 211031440)
Faculdade de Ciências e Tecnologias em Engenharia (FGA / FCTE) - Universidade de Brasília (UnB)
Docente: Prof. Dr. Fabiano Araujo Soares
"""

import sys
import subprocess
from pathlib import Path

# Módulos Práticos de Métodos Clássicos de IA
SCRIPTS_CLASSICOS = {
    "1": ("Busca Não Informada (IDDFS)", "Algoritimos_Classicos/01_busca_nao_informada.py"),
    "2": ("Busca Informada (Weighted A*)", "Algoritimos_Classicos/02_busca_informada.py"),
    "3": ("Busca Complexa / Local (Busca Tabu)", "Algoritimos_Classicos/03_busca_complexa.py"),
    "4": ("Algoritmo Genético (OX1 & Elitismo)", "Algoritimos_Classicos/04_algoritimo_genetico.py"),
    "5": ("CSP - Min-Conflicts (Reparo Local)", "Algoritimos_Classicos/05_CSP.py"),
    "6": ("Banco de Conhecimento (Forward & Backward Chaining)", "Algoritimos_Classicos/06_banco_de_conhecimento.py"),
}

def executar_modulo(chave: str) -> None:
    if chave not in SCRIPTS_CLASSICOS:
        print(f"[ERRO] Opção '{chave}' inválida.", flush=True)
        return

    nome, caminho_relativo = SCRIPTS_CLASSICOS[chave]
    arquivo = Path(__file__).parent / caminho_relativo
    if not arquivo.exists():
        print(f"[ERRO] Arquivo não encontrado: {arquivo}", flush=True)
        return

    print("\n" + "#" * 68, flush=True)
    print(f" Executando: {nome}", flush=True)
    print(f" Caminho: {caminho_relativo}", flush=True)
    print("#" * 68 + "\n", flush=True)
    
    resultado = subprocess.run([sys.executable, str(arquivo)], text=True)
    if resultado.returncode != 0:
        print(f"\n[AVISO] O módulo encerrou com código de retorno {resultado.returncode}.", flush=True)

def executar_todos() -> None:
    print("\n" + "=" * 68)
    print(" EXECUTANDO TODOS OS ALGORITMOS DE MÉTODOS CLÁSSICOS EM SEQUÊNCIA")
    print("=" * 68)
    for chave in sorted(SCRIPTS_CLASSICOS.keys()):
        executar_modulo(chave)
    print("\n" + "=" * 68)
    print(" [OK] Todas as execuções de algoritmos clássicos foram concluídas.")
    print("=" * 68)

def menu() -> None:
    print("\n" + "=" * 68)
    print(" Portfólio de Inteligência Artificial (FGA0221) - UnB / FGA")
    print(" Autor: Pedro Gomes Oliveira (Matrícula: 211031440)")
    print(" Docente: Prof. Dr. Fabiano Araujo Soares")
    print("=" * 68)
    print("Módulo: Métodos Clássicos de IA (Algoritmos de Busca e Raciocínio):\n")
    for chave, (nome, _) in SCRIPTS_CLASSICOS.items():
        print(f" [{chave}] {nome}")
    print("\n [A] Executar TODOS os 6 algoritmos clássicos")
    print(" [0] Sair\n")
    
    escolha = input("Digite sua opção: ").strip().upper()
    if escolha == "0":
        print("Encerrando.")
        return
    elif escolha == "A":
        executar_todos()
    elif escolha in SCRIPTS_CLASSICOS:
        executar_modulo(escolha)
    else:
        print("[Opção inválida]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        if arg in ["--all", "-A", "ALL"]:
            executar_todos()
        elif arg in SCRIPTS_CLASSICOS:
            executar_modulo(arg)
        else:
            print("Uso: python main.py [1..6|--all]")
    else:
        if not sys.stdin.isatty():
            executar_todos()
        else:
            menu()
