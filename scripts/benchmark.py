import csv
import math
import os
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(Path(__file__).resolve().parent))

from serial import gerar_matriz, multiplicar_matrizes_serial
from paralelo_sem_agrupamento import multiplicar_paralelo_sem_agrupamento
from paralelo_por_linha import multiplicar_paralelo_por_linha
from paralelo_por_blocos import multiplicar_paralelo_por_blocos

PROCESSOS = 4

# Ajuste aqui os tamanhos que deseja testar
TAMANHOS = [
    (120, 240, 120),
    (180, 360, 180),
    (240, 480, 240),
    (300, 600, 300),
]

SAIDA_GERAL = BASE_DIR / "comparacao_serial_paralelo" / "comparacao_geral_maior.csv"
SAIDA_RESUMIDA = BASE_DIR / "comparacao_serial_paralelo" / "comparacao_resumida_maior.csv"

def medir_tempo(func, *args):
    inicio = time.perf_counter()
    resultado = func(*args)
    fim = time.perf_counter()
    return resultado, fim - inicio

def quase_igual_matriz(A, B):
    return A == B

def main():
    os.makedirs(SAIDA_GERAL.parent, exist_ok=True)
    linhas_geral = []
    linhas_resumo = []

    for idx, (n, m, p) in enumerate(TAMANHOS, start=1):
        print(f"Teste {idx}: {n}x{m} * {m}x{p}")
        seed_a = 100 + idx
        seed_b = 200 + idx

        A = gerar_matriz(n, m, seed=seed_a)
        B = gerar_matriz(m, p, seed=seed_b)

        resultado_serial, tempo_serial = medir_tempo(multiplicar_matrizes_serial, A, B)

        metodos = [
            ("Serial", tempo_serial, True, 1),
        ]

        for nome, func in [
            ("Sem agrupamento", multiplicar_paralelo_sem_agrupamento),
            ("Por linha", multiplicar_paralelo_por_linha),
            ("Por blocos", multiplicar_paralelo_por_blocos),
        ]:
            try:
                resultado_paralelo, tempo = medir_tempo(func, A, B, PROCESSOS)
                validado = quase_igual_matriz(resultado_serial, resultado_paralelo)
            except Exception as exc:
                tempo = math.nan
                validado = False
                print(f"Erro em {nome}: {exc}")
            metodos.append((nome, tempo, validado, PROCESSOS))

        for metodo, tempo, validado, processos in metodos:
            speedup = 1.0 if metodo == "Serial" else (tempo_serial / tempo if tempo and not math.isnan(tempo) else math.nan)
            eficiencia = 1.0 if metodo == "Serial" else (speedup / processos if speedup and not math.isnan(speedup) else math.nan)
            linhas_geral.append({
                "n": n,
                "m": m,
                "p": p,
                "tamanho": f"{n} x {m} x {p}",
                "metodo": metodo,
                "tempo_segundos": round(tempo, 6) if not math.isnan(tempo) else "",
                "speedup": round(speedup, 6) if not math.isnan(speedup) else "",
                "eficiencia": round(eficiencia, 6) if not math.isnan(eficiencia) else "",
                "processos": processos,
                "validado_com_serial": validado,
            })

        resumo = {"n": n, "m": m, "p": p, "tamanho": f"{n} x {m} x {p}"}
        for metodo, tempo, validado, processos in metodos:
            chave = metodo.lower().replace(" ", "_")
            resumo[f"tempo_{chave}"] = round(tempo, 6) if not math.isnan(tempo) else ""
            if metodo != "Serial":
                speedup = tempo_serial / tempo if tempo and not math.isnan(tempo) else math.nan
                resumo[f"speedup_{chave}"] = round(speedup, 6) if not math.isnan(speedup) else ""
        linhas_resumo.append(resumo)

    with open(SAIDA_GERAL, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(linhas_geral[0].keys()))
        writer.writeheader()
        writer.writerows(linhas_geral)

    with open(SAIDA_RESUMIDA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(linhas_resumo[0].keys()))
        writer.writeheader()
        writer.writerows(linhas_resumo)

    print(f"Arquivo gerado: {SAIDA_GERAL}")
    print(f"Arquivo gerado: {SAIDA_RESUMIDA}")

if __name__ == "__main__":
    main()
