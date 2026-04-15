from __future__ import annotations

import csv
import multiprocessing as mp
import random
import time
from pathlib import Path
from typing import List, Sequence, Tuple, Optional

Matrix = List[List[int]]

BASE_DIR = Path(__file__).resolve().parents[1]
ARQUIVO_BASE = BASE_DIR / "comparacao_serial_paralelo" / "comparacao_serial_e_paralelo.csv"
ARQUIVO_SAIDA = BASE_DIR / "comparacao_serial_paralelo" / "comparacao_paralelo.csv"

_B_GLOBAL: Optional[Matrix] = None


def gerar_matriz(linhas: int, colunas: int, seed: Optional[int] = None) -> Matrix:
    rng = random.Random(seed)
    return [[rng.randint(1, 10) for _ in range(colunas)] for _ in range(linhas)]


def _init_pool(B: Matrix):
    global _B_GLOBAL
    _B_GLOBAL = B


def _calcular_bloco(task: Tuple[int, List[Sequence[int]]]) -> Tuple[int, List[List[int]]]:
    inicio_linha, bloco_a = task
    if _B_GLOBAL is None:
        raise RuntimeError("Matriz B não inicializada no processo worker.")

    colunas_b = len(_B_GLOBAL[0])
    bloco_resultado: List[List[int]] = []

    for linha_a in bloco_a:
        linha_resultado = [0] * colunas_b
        for j in range(colunas_b):
            soma = 0
            for k in range(len(linha_a)):
                soma += linha_a[k] * _B_GLOBAL[k][j]
            linha_resultado[j] = soma
        bloco_resultado.append(linha_resultado)

    return inicio_linha, bloco_resultado


def multiplicar_por_blocos(
    A: Matrix,
    B: Matrix,
    num_processos: int | None = None,
    tamanho_bloco: int = 10,
) -> Matrix:
    if not A or not B:
        raise ValueError("As matrizes não podem ser vazias.")

    linhas_a = len(A)
    colunas_a = len(A[0])
    linhas_b = len(B)

    if colunas_a != linhas_b:
        raise ValueError("Dimensões incompatíveis para multiplicação de matrizes.")

    resultado = [[0 for _ in range(len(B[0]))] for _ in range(linhas_a)]

    tarefas: list[Tuple[int, List[Sequence[int]]]] = []
    for inicio in range(0, linhas_a, tamanho_bloco):
        fim = min(inicio + tamanho_bloco, linhas_a)
        tarefas.append((inicio, A[inicio:fim]))

    with mp.Pool(processes=num_processos, initializer=_init_pool, initargs=(B,)) as pool:
        for inicio_linha, bloco_resultado in pool.imap_unordered(_calcular_bloco, tarefas, chunksize=1):
            for deslocamento, linha_resultado in enumerate(bloco_resultado):
                resultado[inicio_linha + deslocamento] = linha_resultado

    return resultado


def main():
    linhas_saida = []
    processos = 4
    tamanho_bloco = 10

    with open(ARQUIVO_BASE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, start=1):
            n = int(row["n"])
            m = int(row["m"])
            p = n

            print(f"[PARALELO] Teste {idx}: A={n}x{m}, B={m}x{p}")

            A = gerar_matriz(n, m, seed=100 + idx)
            B = gerar_matriz(m, p, seed=200 + idx)

            inicio = time.perf_counter()
            multiplicar_por_blocos(A, B, num_processos=processos, tamanho_bloco=tamanho_bloco)
            fim = time.perf_counter()

            tempo = fim - inicio

            linhas_saida.append({
                "n": n,
                "m": m,
                "tempo_execucao": round(tempo, 6),
            })

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "m", "tempo_execucao"])
        writer.writeheader()
        writer.writerows(linhas_saida)

    print(f"Arquivo gerado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()