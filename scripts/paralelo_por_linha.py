from __future__ import annotations

import multiprocessing as mp
import time
from typing import List, Sequence, Tuple

Matrix = List[List[int]]

_B_GLOBAL: Matrix | None = None


def _init_pool(B: Matrix):
    global _B_GLOBAL
    _B_GLOBAL = B


def _calcular_linha(task: Tuple[int, Sequence[int]]) -> Tuple[int, List[int]]:
    indice_linha, linha_a = task
    if _B_GLOBAL is None:
        raise RuntimeError("Matriz B não inicializada no processo worker.")

    colunas_b = len(_B_GLOBAL[0])
    linha_resultado = [0] * colunas_b

    for j in range(colunas_b):
        soma = 0
        for k in range(len(linha_a)):
            soma += linha_a[k] * _B_GLOBAL[k][j]
        linha_resultado[j] = soma

    return indice_linha, linha_resultado


def multiplicar_por_linha(A: Matrix, B: Matrix, num_processos: int | None = None) -> Matrix:
    """Versão paralela em que cada tarefa processa uma linha inteira da matriz resultado."""
    if not A or not B:
        raise ValueError("As matrizes não podem ser vazias.")

    linhas_a = len(A)
    colunas_a = len(A[0])
    linhas_b = len(B)

    if colunas_a != linhas_b:
        raise ValueError("Dimensões incompatíveis para multiplicação de matrizes.")

    resultado = [[0 for _ in range(len(B[0]))] for _ in range(linhas_a)]
    tarefas = [(i, A[i]) for i in range(linhas_a)]

    with mp.Pool(processes=num_processos, initializer=_init_pool, initargs=(B,)) as pool:
        for indice_linha, linha_resultado in pool.imap_unordered(_calcular_linha, tarefas, chunksize=1):
            resultado[indice_linha] = linha_resultado

    return resultado


if __name__ == "__main__":
    from serial import gerar_matriz

    N = 100
    M = 200
    P = 100
    PROCESSOS = 4

    A = gerar_matriz(N, M, seed=42)
    B = gerar_matriz(M, P, seed=99)

    inicio = time.perf_counter()
    C = multiplicar_por_linha(A, B, PROCESSOS)
    fim = time.perf_counter()

    print(f"Dimensões: A={N}x{M}, B={M}x{P}")
    print(f"Tempo paralelo por linha: {fim - inicio:.6f} s")
    print(f"Elemento [0][0]: {C[0][0]}")
