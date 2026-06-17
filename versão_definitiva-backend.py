import os
import random


# Constantes:

AGUA = 0
NAVIO = 1
ACERTO = 2
ERRO = 3


# Variáveis:


tabuleiro_real = [[AGUA for _ in range(10)] for _ in range(10)]
tabuleiro_jogador = [[AGUA for _ in range(10)] for _ in range(10)]

acertos = 0
partes_navio = 0


# Funções:


def mostrar_tabuleiro(tabuleiro):

    simbolos = {
        AGUA: "~",
        NAVIO: "N",
        ACERTO: "X",
        ERRO: "O"
    }

    for linha in tabuleiro:

        for valor in linha:
            print(simbolos[valor], end=" ")

        print()


def posicao_valida(linha, coluna):

    return 0 <= linha < 10 and 0 <= coluna < 10


def criar_navio(tamanho):

    global partes_navio

    while True:

        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        direcao = random.choice(["H", "V"])

        pode_colocar = True

        # Horizontal
        if direcao == "H":

            if coluna + tamanho - 1 >= 10:
                continue

            for i in range(tamanho):

                if tabuleiro_real[linha][coluna + i] != AGUA:
                    pode_colocar = False
                    break

            if pode_colocar:

                for i in range(tamanho):
                    tabuleiro_real[linha][coluna + i] = NAVIO

                partes_navio += tamanho
                return

        # Vertical
        else:

            if linha + tamanho - 1 >= 10:
                continue

            for i in range(tamanho):

                if tabuleiro_real[linha + i][coluna] != AGUA:
                    pode_colocar = False
                    break

            if pode_colocar:

                for i in range(tamanho):
                    tabuleiro_real[linha + i][coluna] = NAVIO

                partes_navio += tamanho
                return



# Criacao da navios: 


quantidade_navios_1 = int(
    input("Quantidade de navios de 1 casa: ")
)

quantidade_navios_2 = int(
    input("Quantidade de navios de 2 casas: ")
)

quantidade_navios_3 = int(
    input("Quantidade de navios de 3 casas: ")
)

quantidade_navios_4 = int(
    input("Quantidade de navios de 4 casas: ")
)

quantidade_navios_5 = int(
    input("Quantidade de navios de 5 casas: ")
)

for i in range(quantidade_navios_1):
    criar_navio(1)

for i in range(quantidade_navios_2):
    criar_navio(2)

for i in range(quantidade_navios_3):
    criar_navio(3)

for i in range(quantidade_navios_4):
    criar_navio(4)

for i in range(quantidade_navios_5):
    criar_navio(5)


# Loop principal


while True:

    os.system("cls")

    print("TABULEIRO DO JOGADOR\n")

    mostrar_tabuleiro(tabuleiro_jogador)

    print(f"\nPartes destruídas: {acertos}/{partes_navio}")

    try:

        linha, coluna = map(
            int,
            input(
                "\nDigite a linha e coluna do tiro (ex: 3,5): "
            ).split(",")
        )

        if not posicao_valida(linha, coluna):

            print("Posição inválida!")
            input("Pressione ENTER...")
            continue

        if tabuleiro_jogador[linha][coluna] != AGUA:

            print("Você já atirou nessa posição!")
            input("Pressione ENTER...")
            continue

        # Acerto

        if tabuleiro_real[linha][coluna] == NAVIO:

            print("ACERTOU!")

            tabuleiro_real[linha][coluna] = ACERTO
            tabuleiro_jogador[linha][coluna] = ACERTO

            acertos += 1

        # Erro

        else:

            print("ÁGUA!")

            tabuleiro_jogador[linha][coluna] = ERRO

        # Vitória

        if acertos == partes_navio:

            os.system("cls")

            print("PARABÉNS!")
            print("VOCÊ DESTRUIU TODOS OS NAVIOS!\n")

            mostrar_tabuleiro(tabuleiro_jogador)

            break

        input("\nPressione ENTER...")

    except ValueError:

        print("Entrada inválida!")
        input("Pressione ENTER...")