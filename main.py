"""
Executor Principal - Portfólio de Métodos Clássicos de IA
Pedro Gomes Oliveira (Matrícula: 211031440)
FGA0221 - Inteligência Artificial | Universidade de Brasília (UnB)
"""

import sys
import subprocess
from pathlib import Path

SCRIPTS = {
    "1": ("Busca Não Informada (IDDFS)", "Entrega_02/01_busca_nao_informada.py"),
    "2": ("Busca Informada (Weighted A*)", "Entrega_02/02_busca_informada.py"),
    "3": ("Busca Complexa / Local (Busca Tabu)", "Entrega_02/03_busca_complexa.py"),
    "4": ("Algoritmo Genético (OX1 & Elitismo)", "Entrega_02/04_algoritimo_genetico.py"),
    "5": ("CSP - Min-Conflicts (Reparo Local)", "Entrega_02/05_CSP.py"),
    "6": ("Banco de Conhecimento (Forward & Backward Chaining)", "Entrega_02/06_banco_de_conhecimento.py"),
}

def executar_modulo(chave: str) -> None:
    nome, caminho = SCRIPTS[chave]
    arquivo = Path(__file__).parent / caminho
    if not arquivo.exists():
        print(f"[ERRO] Arquivo não encontrado: {arquivo}", flush=True)
        return

    print("\n" + "#" * 60, flush=True)
    print(f" Executando: {nome} [{caminho}]", flush=True)
    print("#" * 60 + "\n", flush=True)
    
    resultado = subprocess.run([sys.executable, str(arquivo)], text=True)
    if resultado.returncode != 0:
        print(f"\n[AVISO] O módulo encerrou com código de retorno {resultado.returncode}.", flush=True)

def executar_todos() -> None:
    print("\n" + "=" * 60)
    print(" EXECUTANDO TODAS AS ATIVIDADES EM SEQUÊNCIA")
    print("=" * 60)
    for chave in sorted(SCRIPTS.keys()):
        executar_modulo(chave)
    print("\n" + "=" * 60)
    print(" [OK] Todas as execuções foram finalizadas com sucesso.")
    print("=" * 60)

def menu() -> None:
    print("\n" + "=" * 60)
    print(" Portfólio de Inteligência Artificial Clássica - UnB / FGA")
    print(" Autor: Pedro Gomes Oliveira (Matrícula: 211031440)")
    print("=" * 60)
    print("Selecione um módulo para executar:\n")
    for chave, (nome, caminho) in SCRIPTS.items():
        print(f" [{chave}] {nome}")
    print(" [A] Executar TODOS os módulos")
    print(" [0] Sair\n")
    
    escolha = input("Digite sua opção: ").strip().upper()
    if escolha == "0":
        print("Encerrando.")
        return
    elif escolha == "A":
        executar_todos()
    elif escolha in SCRIPTS:
        executar_modulo(escolha)
    else:
        print("[Opção inválida]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        if arg in ["--all", "-A", "ALL"]:
            executar_todos()
        elif arg in SCRIPTS:
            executar_modulo(arg)
        else:
            print(f"Uso: python main.py [1..6|--all]")
    else:
        # Se chamado sem argumentos e for não interativo ou com stdin fechado, roda todos
        if not sys.stdin.isatty():
            executar_todos()
        else:
            menu()
