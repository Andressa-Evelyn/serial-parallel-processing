| Método | N | M | P | Tempo (s) | Speedup | Eficiência | Processos | Válido |
|---|---:|---:|---:|---:|---:|---:|---:|:---:|
| Serial | 10 | 20 | 10 | 0.000204 | 1.000000 | 1.000000 | 1 | True |
| Paralelo sem agrupamento | 10 | 20 | 10 | 0.243951 | 0.000838 | 0.000209 | 4 | True |
| Paralelo por linha | 10 | 20 | 10 | 0.210412 | 0.000971 | 0.000243 | 4 | True |
| Paralelo por blocos | 10 | 20 | 10 | 0.214763 | 0.000952 | 0.000238 | 4 | True |
| Serial | 60 | 120 | 60 | 0.050253 | 1.000000 | 1.000000 | 1 | True |
| Paralelo sem agrupamento | 60 | 120 | 60 | 0.276610 | 0.181673 | 0.045418 | 4 | True |
| Paralelo por linha | 60 | 120 | 60 | 0.301789 | 0.166515 | 0.041629 | 4 | True |
| Paralelo por blocos | 60 | 120 | 60 | 0.229900 | 0.218584 | 0.054646 | 4 | True |
| Serial | 120 | 240 | 120 | 0.268687 | 1.000000 | 1.000000 | 1 | True |
| Paralelo sem agrupamento | 120 | 240 | 120 | 0.486681 | 0.552080 | 0.138020 | 4 | True |
| Paralelo por linha | 120 | 240 | 120 | 0.485644 | 0.553260 | 0.138315 | 4 | True |
| Paralelo por blocos | 120 | 240 | 120 | 0.334894 | 0.802305 | 0.200576 | 4 | True |