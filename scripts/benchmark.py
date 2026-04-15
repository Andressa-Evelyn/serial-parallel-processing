from __future__ import annotations

import csv
import math
import multiprocessing as mp
import time
from pathlib import Path
from typing import Callable, Optional

from paralelo_por_blocos import multiplicar_por_blocos
from paralelo_por_linha import multiplicar_por_linha
from paralelo_sem_agrupamento import multiplicar_sem_agrupamento
from serial import gerar_matriz, multiplicar_matrizes_serial

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "comparacao_serial_paralelo"
OUTPUT_DIR.mkdir(exist_ok=True)

# Preset seguro para gerar resultados em tempo razoável.
# Se quiser, troque pelos tamanhos do seu trabalho.
EXPERIMENTOS = [
    (10, 20, 10),
    (60, 120, 60),
    (120, 240, 120),
]

NUM_PROCESSOS = max(2, min(4, mp.cpu_count()))
TAMANHO_BLOCO = 20
REPETICOES = 1
SEED_A = 42
SEED_B = 99

# Evita explodir o número de tarefas no modo "sem agrupamento".
MAX_TAREFAS_SEM_AGRUPAMENTO = 40_000


def medir_tempo(func: Callable, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = func(*args, **kwargs)
    fim = time.perf_counter()
    return resultado, fim - inicio


def matrizes_iguais(A, B) -> bool:
    if len(A) != len(B):
        return False
    return all(linha_a == linha_b for linha_a, linha_b in zip(A, B))


def media(valores: list[float]) -> float:
    return sum(valores) / len(valores) if valores else math.nan


def formatar_numero(valor: Optional[float]) -> str:
    if valor is None or (isinstance(valor, float) and math.isnan(valor)):
        return "N/A"
    return f"{valor:.6f}"


def executar_metodo_repetido(func: Callable, *args, repeticoes: int = 1, **kwargs):
    tempos = []
    ultimo_resultado = None
    for _ in range(repeticoes):
        ultimo_resultado, tempo = medir_tempo(func, *args, **kwargs)
        tempos.append(tempo)
    return ultimo_resultado, media(tempos)


def main():
    linhas_csv = []
    linhas_txt = []

    for n, m, p in EXPERIMENTOS:
        A = gerar_matriz(n, m, seed=SEED_A)
        B = gerar_matriz(m, p, seed=SEED_B)

        resultado_serial, tempo_serial = executar_metodo_repetido(
            multiplicar_matrizes_serial,
            A,
            B,
            repeticoes=REPETICOES,
        )

        linhas_resultado = [
            {
                "metodo": "Serial",
                "n": n,
                "m": m,
                "p": p,
                "tempo_segundos": tempo_serial,
                "speedup": 1.0,
                "eficiencia": 1.0,
                "processos": 1,
                "valido": True,
                "observacao": "Baseline sequencial",
            }
        ]

        total_tarefas_finas = n * p
        if total_tarefas_finas <= MAX_TAREFAS_SEM_AGRUPAMENTO:
            resultado_sem, tempo_sem = executar_metodo_repetido(
                multiplicar_sem_agrupamento,
                A,
                B,
                NUM_PROCESSOS,
                repeticoes=REPETICOES,
            )
            valido_sem = matrizes_iguais(resultado_serial, resultado_sem)
            speedup_sem = tempo_serial / tempo_sem if tempo_sem > 0 else math.nan
            eficiencia_sem = speedup_sem / NUM_PROCESSOS if NUM_PROCESSOS > 0 else math.nan
            linhas_resultado.append(
                {
                    "metodo": "Paralelo sem agrupamento",
                    "n": n,
                    "m": m,
                    "p": p,
                    "tempo_segundos": tempo_sem,
                    "speedup": speedup_sem,
                    "eficiencia": eficiencia_sem,
                    "processos": NUM_PROCESSOS,
                    "valido": valido_sem,
                    "observacao": f"Uma tarefa por célula ({total_tarefas_finas} tarefas)",
                }
            )
        else:
            linhas_resultado.append(
                {
                    "metodo": "Paralelo sem agrupamento",
                    "n": n,
                    "m": m,
                    "p": p,
                    "tempo_segundos": math.nan,
                    "speedup": math.nan,
                    "eficiencia": math.nan,
                    "processos": NUM_PROCESSOS,
                    "valido": False,
                    "observacao": f"Ignorado: {total_tarefas_finas} tarefas > limite de {MAX_TAREFAS_SEM_AGRUPAMENTO}",
                }
            )

        resultado_linha, tempo_linha = executar_metodo_repetido(
            multiplicar_por_linha,
            A,
            B,
            NUM_PROCESSOS,
            repeticoes=REPETICOES,
        )
        valido_linha = matrizes_iguais(resultado_serial, resultado_linha)
        speedup_linha = tempo_serial / tempo_linha if tempo_linha > 0 else math.nan
        eficiencia_linha = speedup_linha / NUM_PROCESSOS if NUM_PROCESSOS > 0 else math.nan
        linhas_resultado.append(
            {
                "metodo": "Paralelo por linha",
                "n": n,
                "m": m,
                "p": p,
                "tempo_segundos": tempo_linha,
                "speedup": speedup_linha,
                "eficiencia": eficiencia_linha,
                "processos": NUM_PROCESSOS,
                "valido": valido_linha,
                "observacao": f"Uma tarefa por linha ({n} tarefas)",
            }
        )

        resultado_blocos, tempo_blocos = executar_metodo_repetido(
            multiplicar_por_blocos,
            A,
            B,
            NUM_PROCESSOS,
            TAMANHO_BLOCO,
            repeticoes=REPETICOES,
        )
        valido_blocos = matrizes_iguais(resultado_serial, resultado_blocos)
        speedup_blocos = tempo_serial / tempo_blocos if tempo_blocos > 0 else math.nan
        eficiencia_blocos = speedup_blocos / NUM_PROCESSOS if NUM_PROCESSOS > 0 else math.nan
        linhas_resultado.append(
            {
                "metodo": "Paralelo por blocos",
                "n": n,
                "m": m,
                "p": p,
                "tempo_segundos": tempo_blocos,
                "speedup": speedup_blocos,
                "eficiencia": eficiencia_blocos,
                "processos": NUM_PROCESSOS,
                "valido": valido_blocos,
                "observacao": f"Blocos de {TAMANHO_BLOCO} linhas",
            }
        )

        linhas_csv.extend(linhas_resultado)

        linhas_txt.append(f"Experimento A={n}x{m}, B={m}x{p}")
        linhas_txt.append("-" * 72)
        for linha in linhas_resultado:
            linhas_txt.append(
                f"{linha['metodo']:<28} | tempo={formatar_numero(linha['tempo_segundos'])} s | "
                f"speedup={formatar_numero(linha['speedup'])} | "
                f"eficiência={formatar_numero(linha['eficiencia'])} | "
                f"válido={linha['valido']} | {linha['observacao']}"
            )
        linhas_txt.append("")

    csv_path = OUTPUT_DIR / "comparacao_geral.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as arquivo_csv:
        writer = csv.DictWriter(
            arquivo_csv,
            fieldnames=[
                "metodo",
                "n",
                "m",
                "p",
                "tempo_segundos",
                "speedup",
                "eficiencia",
                "processos",
                "valido",
                "observacao",
            ],
        )
        writer.writeheader()
        writer.writerows(linhas_csv)

    txt_path = OUTPUT_DIR / "comparacao_geral.txt"
    txt_path.write_text("\n".join(linhas_txt), encoding="utf-8")

    resumo_path = OUTPUT_DIR / "resumo_tabela.md"
    tabela_md = [
        "| Método | N | M | P | Tempo (s) | Speedup | Eficiência | Processos | Válido |",
        "|---|---:|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for linha in linhas_csv:
        tabela_md.append(
            f"| {linha['metodo']} | {linha['n']} | {linha['m']} | {linha['p']} | "
            f"{formatar_numero(linha['tempo_segundos'])} | {formatar_numero(linha['speedup'])} | "
            f"{formatar_numero(linha['eficiencia'])} | {linha['processos']} | {linha['valido']} |"
        )
    resumo_path.write_text("\n".join(tabela_md), encoding="utf-8")

    print(f"Arquivos gerados em: {OUTPUT_DIR}")
    print(f"- CSV: {csv_path.name}")
    print(f"- TXT: {txt_path.name}")
    print(f"- Tabela Markdown: {resumo_path.name}")
    print(f"- Processos usados: {NUM_PROCESSOS}")


if __name__ == "__main__":
    mp.freeze_support()
    main()
