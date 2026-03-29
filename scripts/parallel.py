import multiprocessing
import time
import random
from tqdm import tqdm

def multiplicar_parcial(args):
    """Calcula uma fatia específica da matriz resultante."""
    A, B, inicio, fim = args
    colunas_b = len(B[0])
    linhas_b = len(B)
    # Pré-alocação da matriz de resultado parcial
    resultado_parcial = [[0 for _ in range(colunas_b)] for _ in range(fim - inicio)]
    
    for i in range(inicio, fim):
        for j in range(colunas_b):
            for k in range(linhas_b):
                resultado_parcial[i - inicio][j] += A[i][k] * B[k][j]
    return resultado_parcial

def multiplicar_paralelo(A, B, num_processos):
    """Gerencia a distribuição de tarefas entre os núcleos da CPU."""
    linhas_a = len(A)
    colunas_b = len(B[0])
    resultado = [[0 for _ in range(colunas_b)] for _ in range(linhas_a)]
    
    # Define quantas linhas cada núcleo vai processar
    linhas_por_processo = (linhas_a + num_processos - 1) // num_processos
    tarefas = []
    for i in range(num_processos):
        inicio = i * linhas_por_processo
        fim = min(inicio + linhas_por_processo, linhas_a)
        if inicio < fim:
            tarefas.append((A, B, inicio, fim))

    # Criação do Pool de processos
    with multiprocessing.Pool(processes=num_processos) as pool:
        # imap permite que a barra do tqdm atualize conforme cada processo termina
        resultados_parciais = list(tqdm(
            pool.imap(multiplicar_parcial, tarefas), 
            total=len(tarefas), 
            desc="Processando blocos"
        ))

    # Combina os resultados na matriz final
    for i, parcial in enumerate(resultados_parciais):
        inicio_idx = i * linhas_por_processo
        for j in range(len(parcial)):
            resultado[inicio_idx + j] = parcial[j]
            
    return resultado

def gerar_matriz(linhas, colunas):
    """Cria uma matriz preenchida com números aleatórios."""
    return [[random.randint(1, 10) for _ in range(colunas)] for _ in range(linhas)]

# --- BLOCO OBRIGATÓRIO PARA SCRIPTS .PY ---
if __name__ == "__main__":
    # Configurações
    N = 10000
    M = 20000
    N_PROCESSOS = 4

    print(f"Gerando matrizes {N}x{M} e {M}x{N}...")
    A = gerar_matriz(N, M)
    B = gerar_matriz(M, N)

    print(f"Iniciando multiplicação paralela com {N_PROCESSOS} processos...")
    inicio_tempo = time.time()
    
    C = multiplicar_paralelo(A, B, N_PROCESSOS)
    
    fim_tempo = time.time()
    print(f"\nTempo de execução: {fim_tempo - inicio_tempo:.2f} segundos")