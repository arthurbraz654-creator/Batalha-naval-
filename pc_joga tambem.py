# imports: 
import random 
import os 

# funções: 


# Variáveis globais:
tabuleiro_real = [["~" for _ in range(10)] for _ in range (10)] 
tabuleiro_jogo = [["~" for _ in range(10)]for _ in range (10)]
quantidade_de_navios = 0
navios_colocados = 0
bomba1 = 0
bomba2 = 0 

bomba1_pc = 0
bomba2_pc = 0

# main: 
quantidade_de_navios = int(input("Defina a quantidade de navios que o jogador e o Usuário terão: "))

while True:
    while navios_colocados*2 < quantidade_de_navios:
        print ("Turno do jogador: ")
        linha,coluna = (input("Digite a linha e a coluna separado por vírgulas:").split(","))
        linha = int(linha)
        coluna = int(coluna)
        input("Pressione Enter")

        print ("Turno do Computador: ")
        linha_pc = random.randint(0,9)
        coluna_pc = random.randint(0,9)
        input("Pressione Enter")
        
        if (linha != linha_pc and coluna != coluna_pc):
            if tabuleiro_real[linha][coluna] == "~":
                tabuleiro_real[linha][coluna] = "N"
                navios_colocados +=1 

            if tabuleiro_real[linha_pc][coluna_pc] == "~":
                tabuleiro_real[linha_pc][coluna_pc] = "P"
                navios_colocados +=1 
        
        else:
            # tratando caso o random iguale as casas 
            if (linha > 0 and linha < 9) and (coluna > 0 and coluna < 9 ):
                if tabuleiro_real[linha][coluna] == "~":
                    tabuleiro_real[linha][coluna] = "N"
                    navios_colocados +=1 
                
                #usando as linhas como critério de desempate; por enquanto.
                linha_pc = linha +1

                if tabuleiro_real[linha_pc][coluna_pc] == "~":
                    tabuleiro_real[linha_pc][coluna_pc] = "P"
                    navios_colocados +=1                 

            elif (linha == 9 and coluna == 9):
                if tabuleiro_real[linha][coluna] == "~":
                    tabuleiro_real[linha][coluna] = "N"
                    navios_colocados +=1

                linha_pc = linha - 1

                if tabuleiro_real[linha_pc][coluna_pc] == "~":
                    tabuleiro_real[linha_pc][coluna_pc] = "P"
                    navios_colocados +=1
            
            elif (linha == 0 and coluna == 0):
                if tabuleiro_real[linha][coluna] == "~":
                    tabuleiro_real[linha][coluna] = "N"
                    navios_colocados +=1

                linha_pc = linha + 1

                if tabuleiro_real[linha_pc][coluna_pc] == "~":
                    tabuleiro_real[linha_pc][coluna_pc] = "P"
                    navios_colocados +=1



    for linha in tabuleiro_real:
        print(" ".join(linha))

    print("\n")


    for linha in tabuleiro_jogo:
        print(" ".join(linha) )

    print ("\n Turno do Jogador \n")
    
    bomba1,bomba2 = input("Digite a linha e a coluna que vc quer acertar: ").split(",")
    bomba1 = int(bomba1)
    bomba2 = int(bomba2)

    print ("\n Turno do Computador \n")

    bomba1_pc = random.randint(0,9)
    bomba2_pc = random.randint(0,9)

    if (bomba1 == bomba1_pc == 0) and (bomba2 == bomba2_pc == 0):
        bomba1_pc = bomba1+1
    
    elif (bomba1 == bomba1_pc == 9) and (bomba2 == bomba2_pc == 9):
        bomba1_pc = bomba1-1

    elif (bomba1 == bomba1_pc < 9) and (bomba2 == bomba2_pc > 0):
        bomba1_pc == bomba1+1 

    print ("\n")

    for linha in tabuleiro_jogo:
        print(" ".join(linha) )
    
    print("\n")
    
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

