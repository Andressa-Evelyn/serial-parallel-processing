#  Multiplicação de Matrizes: Execução Serial vs Paralela

##  Descrição

Este projeto tem como objetivo demonstrar, na prática, os conceitos de **computação paralela e concorrente** utilizando Python, comparando a execução **serial** e **paralela** na multiplicação de matrizes de grande porte.

O trabalho foi desenvolvido como parte da disciplina de Computação Paralela e Concorrente, aplicando a **Metodologia de Foster** para divisão e paralelização do problema.

---

##  Objetivos

* Implementar a multiplicação de matrizes de forma **sequencial (serial)**
* Implementar a multiplicação de matrizes utilizando **paralelismo**
* Comparar o desempenho entre as duas abordagens
* Analisar o ganho de eficiência com o uso de múltiplos núcleos
* Aplicar os conceitos da **Metodologia de Foster**

---

##  Tecnologias Utilizadas

* Python 3
* Biblioteca `multiprocessing`
* Biblioteca `time`

---

##  Resultados Obtidos

###  Execução Serial

| Tamanho        | Tempo     |
| -------------- | --------- |
| n=10, m=20     | 0.00032 s |
| n=100, m=200   | 0.1477 s  |
| n=1000, m=2000 | 190.20 s  |

---

###  Execução Paralela

| Tamanho        | Tempo   |
| -------------- | ------- |
| n=10, m=20     | 0.19 s  |
| n=100, m=200   | 0.24 s  |
| n=1000, m=2000 | 60.53 s |

---

##  Análise dos Resultados

* Para matrizes pequenas, a execução paralela apresentou pior desempenho devido ao **overhead de criação de processos**.
* Para matrizes grandes, o paralelismo reduziu significativamente o tempo de execução.

---

##  Autora

**Andressa Evelyn Lima de Luna**

---

##  Disciplina

Computação Paralela e Concorrente
Semestre 2026.1

---
