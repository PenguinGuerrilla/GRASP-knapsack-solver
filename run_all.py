# Roda o GRASP (solver.py) em todas as instancias e salva resultados em CSV.

import csv
import os
import sys
import time

from solver import (
    leArquivo,
    geraPopInicial,
    gulosoAleatorio,
    calculaValorMochila,
)

DIR_INSTANCIAS = "problemInstances"
SAIDA_CSV = "resultados.csv"


def resolveInstancia(caminhoIn, nIterMax):
    capacidade, elementos = leArquivo(caminhoIn)

    popInicial = geraPopInicial(elementos, capacidade)
    melhorSolucao = popInicial
    valorMax = calculaValorMochila(popInicial, capacidade)

    for _ in range(nIterMax):
        popNova = gulosoAleatorio(melhorSolucao, elementos, capacidade)
        valorNovo = calculaValorMochila(popNova, capacidade)
        if valorNovo > valorMax:
            valorMax = valorNovo
            melhorSolucao = popNova

    return valorMax


def barraProgresso(atual, total, t0, largura=40):
    frac = atual / total
    cheio = int(largura * frac)
    barra = "#" * cheio + "-" * (largura - cheio)
    decorrido = time.time() - t0
    eta = decorrido / atual * (total - atual) if atual else 0
    sys.stdout.write(
        f"\r[{barra}] {atual}/{total} ({frac*100:5.1f}%) "
        f"decorrido {decorrido:5.0f}s eta {eta:5.0f}s"
    )
    sys.stdout.flush()


def leOtimo(pasta):
    caminho = os.path.join(pasta, "outp.out")
    if not os.path.exists(caminho):
        return -1
    with open(caminho) as f:
        try:
            return int(f.readline().strip())
        except (ValueError, IndexError):
            return -1


def main():
    nIterMax = int(sys.argv[1]) if len(sys.argv) > 1 else 1000

    instancias = sorted(os.listdir(DIR_INSTANCIAS))
    total = len(instancias)
    t0 = time.time()

    with open(SAIDA_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["instancia", "valor_encontrado", "otimo", "gap_pct", "tempo_s"])

        for i, nome in enumerate(instancias, 1):
            pasta = os.path.join(DIR_INSTANCIAS, nome)
            caminhoIn = os.path.join(pasta, "test.in")
            if not os.path.isfile(caminhoIn):
                continue

            t0 = time.time()
            valor = resolveInstancia(caminhoIn, nIterMax)
            tempo = time.time() - t0

            otimo = leOtimo(pasta)
            gap = 100.0 * (otimo - valor) / otimo if otimo > 0 else ""

            writer.writerow([
                nome,
                valor,
                otimo,
                f"{gap:.6f}" if gap != "" else "",
                f"{tempo:.3f}",
            ])
            f.flush()

            barraProgresso(i, total, t0)

    print()  # nova linha apos a barra


if __name__ == "__main__":
    main()
