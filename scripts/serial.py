from __future__ import annotations

import random
import time
from typing import List, Optional

Matrix = List[List[int]]


def gerar_matriz(linhas: int, colunas: int, seed: Optional[int] = None) -> Matrix:
    """Gera uma matriz preenchida com inteiros aleatórios."""
    rng = random.Random(seed)
    return [[rng.randint(1, 10) for _ in range(colunas)] for _ in range(linhas)]


def multiplicar_matrizes_serial(A: Matrix, B: Matrix) -> Matrix:
    """Multiplica duas matrizes de forma sequencial."""
    if not A or not B:
        raise ValueError("As matrizes não podem ser vazias.")

    qtd_linhas_a = len(A)
    qtd_colunas_a = len(A[0])
    qtd_linhas_b = len(B)
    qtd_colunas_b = len(B[0])

    if qtd_colunas_a != qtd_linhas_b:
        raise ValueError(
            f"Dimensões incompatíveis: A é {qtd_linhas_a}x{qtd_colunas_a} e "
            f"B é {qtd_linhas_b}x{qtd_colunas_b}."
        )

    resultado = [[0 for _ in range(qtd_colunas_b)] for _ in range(qtd_linhas_a)]

    for i in range(qtd_linhas_a):
        for j in range(qtd_colunas_b):
            soma = 0
            for k in range(qtd_colunas_a):
                soma += A[i][k] * B[k][j]
            resultado[i][j] = soma

    return resultado


def executar_experimento_serial(n: int, m: int, p: int, seed_a: int = 42, seed_b: int = 99):
    """Gera as matrizes, executa o algoritmo serial e retorna resultado + tempo."""
    A = gerar_matriz(n, m, seed=seed_a)
    B = gerar_matriz(m, p, seed=seed_b)

    inicio = time.perf_counter()
    C = multiplicar_matrizes_serial(A, B)
    fim = time.perf_counter()

    return {
        "matriz_a": A,
        "matriz_b": B,
        "resultado": C,
        "tempo": fim - inicio,
    }


if __name__ == "__main__":
    N = 1000
    M = 2000
    P = 100

    dados = executar_experimento_serial(N, M, P)
    print(f"Dimensões: A={N}x{M}, B={M}x{P}")
    print(f"Tempo serial: {dados['tempo']:.6f} s")
