# Grasp para mochila:

import random
import sys
import os


class Elemento:
    def __init__(self, index, peso, valor):
        self.index = index
        self.peso = peso
        self.valor = valor
        self.densidade = self.valor / self.peso


class Mochila:
    def __init__(self, capacidade, elementos):
        self.capacidade = capacidade
        self.elementos = elementos


# fn leArquivo(caminho):
#     n = primeira linha
#     elementos = n linhas seguintes (id, valor, peso)
#     capacidade = ultima linha
def leArquivo(caminho):
    with open(caminho) as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    n = int(linhas[0])
    elementos = []
    for i in range(1, n + 1):
        idx, valor, peso = map(int, linhas[i].split())
        elementos.append(Elemento(idx, peso, valor))

    capacidade = int(linhas[n + 1])
    return capacidade, elementos


# fn geraPopInicial(elementos):
#     pop_inicial = []
#     peso_total = 0
#     para cada elemento e da mochila (ordenada por densidade)
#         se e.peso + peso_total > capacidade
#             break
#         pop_inicial.append(e)
#         peso_total += e.peso
#     fim para
#     return pop_inicial
def geraPopInicial(elementos, capacidade):
    popInicial = []
    pesoTotal = 0

    # densidade maior primeiro (guloso por valor/peso)
    sortedElementos = sorted(elementos, key=lambda e: e.densidade, reverse=True)

    for elemento in sortedElementos:
        if elemento.peso + pesoTotal > capacidade:
            continue
        popInicial.append(elemento)
        pesoTotal += elemento.peso

    return popInicial


# fn calculaValorMochila(m, capacidade)
#     pesoTotal = 0
#     valorTotal = 0
#     para cada elemento e de m:
#         se e.peso + pesoTotal > capacidade
#             return -1
#         pesoTotal += e.peso
#         valorTotal += e.valor
#     return valorTotal
def calculaValorMochila(solucao, capacidade):
    pesoTotal = 0
    valorTotal = 0

    for elemento in solucao:
        pesoTotal += elemento.peso
        valorTotal += elemento.valor

    if pesoTotal > capacidade:
        return -1
    return valorTotal


# fn gulosoAleatorio(elementos, mochila):
#     nElemetosAlterados = 4
#     tamSubconjuntoAnalisado = 2
#     for i in range(nElemetosAlterados):
#         do:
#             seleciona elemento aleatorio da mochila
#             seleciona tamSubconjuntoAnalisado acima e abaixo do elemento -> subconjunto
#             seleciona o elemento de maior valor do subconjunto
#             substitui o elemento da mochila pelo novo elemento do subconjunto
#         while mochila nao for valida
#     return mochila
def gulosoAleatorio(solucao, elementos, capacidade):
    nElementosAlterados = 4
    tamSubconjuntoAnalisado = 2

    novaSolucao = list(solucao)

    for _ in range(nElementosAlterados):
        if not novaSolucao:
            break

        tentativas = 0
        while tentativas < 100:
            backup = list(novaSolucao)

            pos = random.randrange(len(novaSolucao))

            i = random.randrange(
                tamSubconjuntoAnalisado,
                len(elementos) - tamSubconjuntoAnalisado,
            )
            janela = elementos[i - tamSubconjuntoAnalisado : i + tamSubconjuntoAnalisado + 1]

            # ignora item ja presente na mochila (sem o da pos atual, que sera trocado)
            presentes = {e.index for k, e in enumerate(novaSolucao) if k != pos}
            candidatos = [e for e in janela if e.index not in presentes]
            if not candidatos:
                novaSolucao[:] = backup
                tentativas += 1
                continue

            melhor = max(candidatos, key=lambda e: e.valor)
            novaSolucao[pos] = melhor

            if calculaValorMochila(novaSolucao, capacidade) > -1:
                break

            novaSolucao[:] = backup
            tentativas += 1

    return novaSolucao


# fn main():
#     abre arquivo
#     capacidade = capaciade do arquivo
#     elementos = elementos do arquivo
#     ordenar itens por densidade
#     popInicial = geraPopInicial
#     valorMax = -1
#     nIter = 0
#     nIterMax = 1000000
#     do:
#         popNova = gulosoAleatorio(elementos, popInicial)
#         valorNovo = calculaValorMochila(popNova)
#         if(valorNovo > valorMax):
#             valorMax = valorNovo
#             popInicial = popNova
#     while(nIter < nIterMax)
def main():
    if len(sys.argv) < 2:
        print("uso: python solver.py <caminho test.in> [nIterMax]")
        sys.exit(1)

    caminho = sys.argv[1]
    nIterMax = int(sys.argv[2]) if len(sys.argv) > 2 else 100000

    capacidade, elementos = leArquivo(caminho)

    popInicial = geraPopInicial(elementos, capacidade)
    melhorSolucao = popInicial
    valorMax = calculaValorMochila(popInicial, capacidade)

    for _ in range(nIterMax):
        popNova = gulosoAleatorio(melhorSolucao, elementos, capacidade)
        valorNovo = calculaValorMochila(popNova, capacidade)
        if valorNovo > valorMax:
            valorMax = valorNovo
            melhorSolucao = popNova

    print(f"valor encontrado: {valorMax}")

    # compara com otimo do combo (outp.out), se existir
    otimoPath = os.path.join(os.path.dirname(caminho), "outp.out")
    if os.path.exists(otimoPath):
        with open(otimoPath) as f:
            otimo = int(f.readline().strip())
        if otimo > 0:
            gap = 100.0 * (otimo - valorMax) / otimo
            print(f"otimo (combo):   {otimo}")
            print(f"gap:             {gap:.4f}%")


if __name__ == "__main__":
    main()
