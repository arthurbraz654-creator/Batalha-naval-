# imports:
import os  
import random

# funções: 



# variaveis globais: 
tabuleiro_real = [["~" for _ in range(10)] for _ in range (10)] 
tabuleiro_jogador = [["~" for _ in range(10)]for _ in range (10)]
quantidade_de_navios = 0
navios_colocados = 0
bomba1 = 0
bomba2 = 0 


# main: 
quantidade_de_navios = int(input("Digite a quantidade de navios que vc deseja: "))

while True:
    while navios_colocados < quantidade_de_navios:
        linha = random.randint(0,9)
        coluna = random.randint(0,9)

        if tabuleiro_real[linha][coluna] == "~":
            tabuleiro_real[linha][coluna] = "N"
            navios_colocados +=1 

    for linha in tabuleiro_real:
        print(" ".join(linha))

    print("\n")


    for linha in tabuleiro_jogador:
        print(" ".join(linha) )

    print ("\n")

    bomba1,bomba2 = input("Digite a linha e a coluna que vc quer acertar: ").split(",")
    bomba1 = int(bomba1)
    bomba2 = int(bomba2)

    if (tabuleiro_real[bomba1][bomba2] == "N" ):
        print("parabéns vc acertou!")
        tabuleiro_jogador[bomba1][bomba2] = "X"
        for linha in tabuleiro_jogador:
            print(" ".join(linha))

    elif (tabuleiro_real[bomba1][bomba2] == "X"):
        print("Essa casa já havia sido selecionada essa casa.")
        for linha in tabuleiro_jogador:
            print(" ".join(linha))
    
    elif (tabuleiro_jogador[bomba1][bomba2] == "0"):
        print("Essa casa já havia sido selecionada essa casa.")
        for linha in tabuleiro_jogador:
            print(" ".join(linha))
        
    else:
        print("Acertou a água")
        tabuleiro_jogador[bomba1][bomba2] = "0"
        for linha in tabuleiro_jogador:
            print(" ".join(linha))
    
    sel = input("Deseja continuar(S/N): ")
    if (sel == "S" or sel == "s"):
        input("Presssione Enter ...")
        os.system("Cls")
        pass
    elif (sel == "N" or sel == "n"):
        input("Pressione Enter ...")
        os.system("Cls")
        break 
    else:
        print("Dígito inválido. ")