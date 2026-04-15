import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PASTA_COMPARACAO = BASE_DIR / "comparacao_serial_paralelo"
PASTA_IMAGEM = BASE_DIR / "imagem"

CSV_CANDIDATOS = [
    PASTA_COMPARACAO / "comparacao_geral_maior.csv",
    PASTA_COMPARACAO / "comparacao_geral.csv",
]

def carregar_csv() -> pd.DataFrame:
    for caminho in CSV_CANDIDATOS:
        if caminho.exists():
            return pd.read_csv(caminho), caminho
    raise FileNotFoundError("Nenhum CSV de comparação encontrado.")

def main():
    os.makedirs(PASTA_IMAGEM, exist_ok=True)
    df, origem = carregar_csv()
    print(f"Usando arquivo: {origem}")

    # Gráfico 1: tempo por método
    plt.figure(figsize=(10, 5))
    for metodo in df["metodo"].unique():
        base = df[df["metodo"] == metodo]
        plt.plot(base["tamanho"], base["tempo_segundos"], marker="o", label=metodo)
    plt.title("Comparação de Tempo por Método")
    plt.xlabel("Tamanho da matriz")
    plt.ylabel("Tempo de execução (s)")
    plt.legend()
    plt.grid(True, axis="y")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(PASTA_IMAGEM / "grafico_tempo.png", dpi=200)
    plt.close()

    # Gráfico 2: speedup
    df_speedup = df[df["metodo"] != "Serial"].copy()
    pivot_speedup = df_speedup.pivot(index="tamanho", columns="metodo", values="speedup")
    ax = pivot_speedup.plot(kind="bar", figsize=(10, 5))
    ax.set_title("Speedup por Método")
    ax.set_xlabel("Tamanho da matriz")
    ax.set_ylabel("Speedup")
    plt.xticks(rotation=20)
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(PASTA_IMAGEM / "grafico_speedup.png", dpi=200)
    plt.close()

    # Gráfico 3: eficiência
    pivot_ef = df_speedup.pivot(index="tamanho", columns="metodo", values="eficiencia")
    ax = pivot_ef.plot(kind="bar", figsize=(10, 5))
    ax.set_title("Eficiência por Método")
    ax.set_xlabel("Tamanho da matriz")
    ax.set_ylabel("Eficiência")
    plt.xticks(rotation=20)
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(PASTA_IMAGEM / "grafico_eficiencia.png", dpi=200)
    plt.close()

    print("Gráficos salvos em:", PASTA_IMAGEM)

if __name__ == "__main__":
    main()
