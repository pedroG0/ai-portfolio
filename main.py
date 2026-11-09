"""
Executor Principal - Portfólio de Inteligência Artificial (FGA0221)
Pedro Gomes Oliveira
Faculdade de Ciências e Tecnologias em Engenharia (FGA / FCTE) - Universidade de Brasília (UnB)
Docente: Prof. Dr. Fabiano Araujo Soares
"""

import os
import sys
import runpy
import traceback
from pathlib import Path

# Garante compatibilidade com terminais Windows padrão (cp1252/cp850)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent

# Módulos Práticos de Métodos Clássicos de IA
SCRIPTS_CLASSICOS = {
    "1": ("Busca Não Informada (IDDFS)", BASE_DIR / "Algoritimos_Classicos" / "01_busca_nao_informada.py"),
    "2": ("Busca Informada (Weighted A*)", BASE_DIR / "Algoritimos_Classicos" / "02_busca_informada.py"),
    "3": ("Busca Complexa / Local (Busca Tabu)", BASE_DIR / "Algoritimos_Classicos" / "03_busca_complexa.py"),
    "4": ("Algoritmo Genético (OX1 & Elitismo)", BASE_DIR / "Algoritimos_Classicos" / "04_algoritimo_genetico.py"),
    "5": ("CSP - Min-Conflicts (Reparo Local)", BASE_DIR / "Algoritimos_Classicos" / "05_CSP.py"),
    "6": ("Banco de Conhecimento (Forward & Backward Chaining)", BASE_DIR / "Algoritimos_Classicos" / "06_banco_de_conhecimento.py"),
}

def executar_modulo(chave: str) -> bool:
    """Executa um módulo específico diretamente no processo Python atual."""
    if chave not in SCRIPTS_CLASSICOS:
        print(f"[ERRO] Opção '{chave}' inválida.", flush=True)
        return False

    nome, arquivo = SCRIPTS_CLASSICOS[chave]
    if not arquivo.exists():
        print(f"[ERRO] Arquivo não encontrado: {arquivo}", flush=True)
        return False

    print("\n" + "=" * 70, flush=True)
    print(f" [>] Executando: {nome}", flush=True)
    print(f" [*] Arquivo: {arquivo.name}", flush=True)
    print("=" * 70 + "\n", flush=True)

    diretorio_original = os.getcwd()
    try:
        # Muda o diretório de trabalho temporariamente para a pasta do script
        os.chdir(str(arquivo.parent))
        if str(arquivo.parent) not in sys.path:
            sys.path.insert(0, str(arquivo.parent))

        # Executa o script como __main__ de forma direta e sem depender de subprocessos externos
        runpy.run_path(str(arquivo), run_name="__main__")
        print("\n" + "-" * 70, flush=True)
        print(f" [OK] Concluído com sucesso: {nome}", flush=True)
        print("-" * 70 + "\n", flush=True)
        return True
    except Exception as e:
        print(f"\n[FALHA] Erro durante a execução de {nome}: {e}", flush=True)
        traceback.print_exc()
        return False
    finally:
        os.chdir(diretorio_original)

def executar_todos() -> None:
    """Executa todos os 6 algoritmos clássicos em sequência."""
    print("\n" + "#" * 70, flush=True)
    print(" EXECUTANDO TODAS AS ATIVIDADES DE MÉTODOS CLÁSSICOS", flush=True)
    print("#" * 70, flush=True)

    sucessos = 0
    for chave in sorted(SCRIPTS_CLASSICOS.keys()):
        if executar_modulo(chave):
            sucessos += 1

    print("\n" + "#" * 70, flush=True)
    print(f" Resumo: {sucessos} de {len(SCRIPTS_CLASSICOS)} módulos executados com sucesso.", flush=True)
    print("#" * 70 + "\n", flush=True)

def menu() -> None:
    """Menu interativo em loop contínuo."""
    while True:
        print("\n" + "=" * 70)
        print(" Portfólio de Inteligência Artificial (FGA0221) - UnB / FGA")
        print(" Autor: Pedro Gomes Oliveira")
        print(" Orientador: Prof. Dr. Fabiano Araujo Soares")
        print("=" * 70)
        print("Selecione um algoritmo para executar:\n")
        for chave, (nome, _) in SCRIPTS_CLASSICOS.items():
            print(f"  [{chave}] {nome}")
        print("\n  [A] Executar TODOS os 6 algoritmos em lote")
        print("  [0] Sair do programa")
        print("=" * 70)

        try:
            escolha = input("\nDigite sua opção: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando o programa.")
            break

        opcao = escolha.lower()
        if opcao in ["0", "s", "sair", "exit", "quit", "q"]:
            print("Encerrando.")
            break
        elif opcao in ["a", "all", "-a", "--all"]:
            executar_todos()
        elif escolha in SCRIPTS_CLASSICOS:
            executar_modulo(escolha)
        else:
            print(f"\n[AVISO] Opção '{escolha}' inválida. Escolha entre 1 e 6, 'A' para todos ou '0' para sair.")

def main() -> None:
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip().lower()
        if arg in ["--all", "-a", "all", "todos", "-all"]:
            executar_todos()
        elif arg in SCRIPTS_CLASSICOS:
            executar_modulo(arg)
        elif arg in ["-h", "--help", "help", "/?"]:
            print("Uso do executor:")
            print("  python main.py          -> Abre o menu interativo")
            print("  python main.py [1..6]   -> Executa o módulo indicado diretamente")
            print("  python main.py --all    -> Executa todos os módulos em lote")
        else:
            print(f"[ERRO] Argumento '{sys.argv[1]}' desconhecido.")
            print("Uso: python main.py [1..6|--all]")
    else:
        # Se estiver em ambiente sem TTY (ex: Code Runner, CI, etc.), executa tudo diretamente
        if not sys.stdin.isatty():
            executar_todos()
        else:
            menu()

if __name__ == "__main__":
    main()
