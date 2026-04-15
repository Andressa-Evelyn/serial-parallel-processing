from __future__ import annotations

import csv
import random
import time
from pathlib import Path
from typing import List, Optional

Matrix = List[List[int]]

BASE_DIR = Path(__file__).resolve().parents[1]
ARQUIVO_BASE = BASE_DIR / "comparacao_serial_paralelo" / "comparacao_serial_e_paralelo.csv"
ARQUIVO_SAIDA = BASE_DIR / "comparacao_serial_paralelo" / "comparacao_serial.csv"


def gerar_matriz(linhas: int, colunas: int, seed: Optional[int] = None) -> Matrix:
    rng = random.Random(seed)
    return [[rng.randint(1, 10) for _ in range(colunas)] for _ in range(linhas)]


def multiplicar_matrizes_serial(A: Matrix, B: Matrix) -> Matrix:
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


def main():
    linhas_saida = []

    with open(ARQUIVO_BASE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, start=1):
            n = int(row["n"])
            m = int(row["m"])
            p = n

            print(f"[SERIAL] Teste {idx}: A={n}x{m}, B={m}x{p}")

            A = gerar_matriz(n, m, seed=100 + idx)
            B = gerar_matriz(m, p, seed=200 + idx)

            inicio = time.perf_counter()
            multiplicar_matrizes_serial(A, B)
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