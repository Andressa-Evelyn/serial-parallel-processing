import time
import random
from tqdm import tqdm

def gerar_matriz(linhas, colunas):
    """Gera uma matriz preenchida com inteiros aleatórios."""
    return [[random.randint(1, 10) for _ in range(colunas)] for _ in range(linhas)]

def multiplicar_matrizes_serial(A, B):
    """Realiza a multiplicação de matrizes de forma sequencial (um núcleo)."""
    qtd_linhas_a = len(A)
    qtd_colunas_a = len(A[0])
    qtd_colunas_b = len(B[0])
    
    # Matriz resultado inicializada com zeros
    C = [[0 for _ in range(qtd_colunas_b)] for _ in range(qtd_linhas_a)]
    
    # Adicionamos o tqdm no primeiro loop para ver o progresso por linha
    for i in tqdm(range(qtd_linhas_a), desc="Multiplicando Serial"):
        for j in range(qtd_colunas_b):
            for k in range(qtd_colunas_a):
                C[i][j] += A[i][k] * B[k][j]
    return C

def main():
    # Configurações das dimensões
    n = 1000
    m = 2000
    
    print(f"Gerando matrizes {n}x{m} e {m}x{n}...")
    A = gerar_matriz(n, m)
    B = gerar_matriz(m, n)
    
    print("Iniciando multiplicação serial (isso pode demorar)...")
    inicio = time.time()
    
    C = multiplicar_matrizes_serial(A, B)
    
    fim = time.time()
    
    print(f"\nTempo serial total: {fim - inicio:.2f} segundos")

if __name__ == "__main__":
    main()