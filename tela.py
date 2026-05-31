# imports

import pygame 
from pygame.locals import*
from sys import exit 

#funções:

pygame.init()

# variáveis globais:
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('BATALHA NAVAL')

#main:

while True: 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
