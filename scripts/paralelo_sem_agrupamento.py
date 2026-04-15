from __future__ import annotations

import multiprocessing as mp
import time
from typing import List, Sequence, Tuple

Matrix = List[List[int]]
Task = Tuple[int, int, Sequence[int]]

_B_GLOBAL: Matrix | None = None


def _init_pool(B: Matrix):
    global _B_GLOBAL
    _B_GLOBAL = B


def _calcular_celula(task: Task) -> Tuple[int, int, int]:
    i, j, linha_a = task
    if _B_GLOBAL is None:
        raise RuntimeError("Matriz B não inicializada no processo worker.")

    soma = 0
    for k in range(len(linha_a)):
        soma += linha_a[k] * _B_GLOBAL[k][j]
    return i, j, soma


def multiplicar_sem_agrupamento(A: Matrix, B: Matrix, num_processos: int | None = None) -> Matrix:
    """Versão paralela com granularidade fina: uma tarefa por célula do resultado."""
    if not A or not B:
        raise ValueError("As matrizes não podem ser vazias.")

    linhas_a = len(A)
    colunas_a = len(A[0])
    linhas_b = len(B)
    colunas_b = len(B[0])

    if colunas_a != linhas_b:
        raise ValueError("Dimensões incompatíveis para multiplicação de matrizes.")

    tarefas: list[Task] = []
    for i in range(linhas_a):
        for j in range(colunas_b):
            tarefas.append((i, j, A[i]))

    resultado = [[0 for _ in range(colunas_b)] for _ in range(linhas_a)]

    with mp.Pool(processes=num_processos, initializer=_init_pool, initargs=(B,)) as pool:
        for i, j, valor in pool.imap_unordered(_calcular_celula, tarefas, chunksize=50):
            resultado[i][j] = valor

    return resultado


if __name__ == "__main__":
    from serial import gerar_matriz

    N = 300
    M = 600
    P = 30
    PROCESSOS = 4

    A = gerar_matriz(N, M, seed=42)
    B = gerar_matriz(M, P, seed=99)

    inicio = time.perf_counter()
    C = multiplicar_sem_agrupamento(A, B, PROCESSOS)
    fim = time.perf_counter()

    print(f"Dimensões: A={N}x{M}, B={M}x{P}")
    print(f"Tempo paralelo sem agrupamento: {fim - inicio:.6f} s")
    print(f"Elemento [0][0]: {C[0][0]}")
