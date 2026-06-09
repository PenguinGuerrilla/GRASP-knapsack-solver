# GRASP for the 0-1 Knapsack Problem

Heuristic solver (GRASP) for the 0-1 knapsack problem, evaluated on the set of
hard instances by Jooken, Leyman & De Causmaecker (2022).

## Objective

This project is a fork of the original data repository. Its goal is to implement
and evaluate a **GRASP** (*Greedy Randomized Adaptive Search Procedure*)
metaheuristic for the 0-1 knapsack problem, comparing the solutions found
against the optima computed by the `combo` algorithm.

## Data (base repository)

The instances in `problemInstances/` and the reference files (`optima.csv`,
`comboExecutable`, `generator.cpp`, etc.) come from the original repository
described in `README.txt`:

> Jooken, J., Leyman, P., & De Causmaecker, P. (2022). *A new class of hard
> problem instances for the 0-1 knapsack problem.* European Journal of
> Operational Research, 301 (3), 841–854.

Each subfolder of `problemInstances/` contains:

- `test.in` — the instance (n, list of items `id profit weight`, capacity `c`).
- `outp.out` — `combo`'s optimal solution (first line = optimal value, or `-1`
  if unsolved).
- `time.out` — `combo`'s runtime.

Full format details in [`README.txt`](README.txt).

## Solver — `solver.py`

GRASP composed of:

1. **Greedy initial population** (`geraPopInicial`) — items sorted by density
   (`profit/weight`) descending, inserted while they fit the capacity.
2. **Greedy-randomized perturbation** (`gulosoAleatorio`) — swaps items for
   higher-value candidates from random windows, with duplicate and validity
   checks (weight ≤ capacity).
3. **Iterative local search** — keeps the best solution across `nIterMax`
   iterations.

At the end, it compares the value found against `combo`'s optimum (`outp.out`)
and reports the *gap*.

### Usage

```bash
python solver.py <path/test.in> [nIterMax]
```

Example:

```bash
python solver.py problemInstances/n_1000_c_10000000000_g_10_f_0.1_eps_0.0001_s_100/test.in 100000
```

Output:

```
valor encontrado: 9999765270
otimo (combo):   9999946233
gap:             0.0018%
```

## Batch run — `run_all.py`

Runs the solver on **all** instances and saves `resultados.csv`.

```bash
python run_all.py [nIterMax]   # default: 1000
```

- Shows a progress bar with elapsed time and ETA.
- `resultados.csv` columns:
  `instancia, valor_encontrado, otimo, gap_pct, tempo_s`
  (`gap_pct` empty when `combo` did not solve the instance, `otimo = -1`).

## Structure

```
solver.py        # GRASP + run for a single instance
run_all.py       # batch run + CSV
problemInstances/  # instances (base repository)
optima.csv       # reference optima (base repository)
README.txt       # original data documentation
```

---

# GRASP para o Problema da Mochila 0-1

Solver heurístico (GRASP) para o problema da mochila 0-1, avaliado sobre o
conjunto de instâncias difíceis de Jooken, Leyman & De Causmaecker (2022).

## Objetivo

Este projeto é um fork do repositório de dados original e tem como objetivo
implementar e avaliar uma metaheurística **GRASP** (*Greedy Randomized Adaptive
Search Procedure*) para o problema da mochila 0-1, comparando as soluções
encontradas com os ótimos calculados pelo algoritmo `combo`.

## Dados (repositório base)

As instâncias em `problemInstances/` e os arquivos de referência
(`optima.csv`, `comboExecutable`, `generator.cpp`, etc.) vêm do repositório
original descrito em `README.txt`:

> Jooken, J., Leyman, P., & De Causmaecker, P. (2022). *A new class of hard
> problem instances for the 0-1 knapsack problem.* European Journal of
> Operational Research, 301 (3), 841–854.

Cada subpasta de `problemInstances/` contém:

- `test.in` — a instância (n, lista de itens `id valor peso`, capacidade `c`).
- `outp.out` — solução ótima do `combo` (primeira linha = valor ótimo, ou `-1`
  se não resolvida).
- `time.out` — tempo do `combo`.

Detalhes completos do formato em [`README.txt`](README.txt).

## Solver — `solver.py`

GRASP composto por:

1. **População inicial gulosa** (`geraPopInicial`) — itens ordenados por
   densidade (`valor/peso`) decrescente, inseridos enquanto cabem na capacidade.
2. **Perturbação guloso-aleatória** (`gulosoAleatorio`) — troca itens por
   candidatos de maior valor em janelas aleatórias, com checagem de duplicata e
   validade (peso ≤ capacidade).
3. **Busca local iterativa** — mantém a melhor solução ao longo de `nIterMax`
   iterações.

Ao final, compara o valor encontrado com o ótimo do `combo` (`outp.out`) e
reporta o *gap*.

### Uso

```bash
python solver.py <caminho/test.in> [nIterMax]
```

Exemplo:

```bash
python solver.py problemInstances/n_1000_c_10000000000_g_10_f_0.1_eps_0.0001_s_100/test.in 100000
```

Saída:

```
valor encontrado: 9999765270
otimo (combo):   9999946233
gap:             0.0018%
```

## Execução em lote — `run_all.py`

Roda o solver em **todas** as instâncias e salva `resultados.csv`.

```bash
python run_all.py [nIterMax]   # padrão: 1000
```

- Mostra uma barra de progresso com tempo decorrido e ETA.
- `resultados.csv` com colunas:
  `instancia, valor_encontrado, otimo, gap_pct, tempo_s`
  (`gap_pct` vazio quando o `combo` não resolveu a instância, `otimo = -1`).

## Estrutura

```
solver.py        # GRASP + execução para uma instância
run_all.py       # execução em lote + CSV
problemInstances/  # instâncias (repositório base)
optima.csv       # ótimos de referência (repositório base)
README.txt       # documentação original dos dados
```
