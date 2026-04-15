from __future__ import annotations

import multiprocessing as mp
import time
from typing import List, Sequence, Tuple

Matrix = List[List[int]]

_B_GLOBAL: Matrix | None = None


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
    """Versão paralela com aglomeração em blocos de linhas."""
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


if __name__ == "__main__":
    from serial import gerar_matriz

    N = 1000
    M = 2000
    P = 100
    PROCESSOS = 4
    TAMANHO_BLOCO = 20

    A = gerar_matriz(N, M, seed=42)
    B = gerar_matriz(M, P, seed=99)

    inicio = time.perf_counter()
    C = multiplicar_por_blocos(A, B, PROCESSOS, TAMANHO_BLOCO)
    fim = time.perf_counter()

    print(f"Dimensões: A={N}x{M}, B={M}x{P}")
    print(f"Tempo paralelo por blocos: {fim - inicio:.6f} s")
    print(f"Elemento [0][0]: {C[0][0]}")
