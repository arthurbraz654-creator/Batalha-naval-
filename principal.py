# imports:

import pygame
import constantes
import os 

from pygame.locals import*

# main:

class game:
    def _init_(self):
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((constantes.LARGURA,constantes.ALTURA)) 
        pygame.display.set_caption(constantes.TITULO)
        self.relogio = pygame.time.Clock()
        self.funciona = True

        def new_game(self):
            self.sprites = pygame.sprite.Group()
            self.rodar()

        def in_game(self):
            self.jogando = True
            while self.jogando:
                self.relogio.tick(constantes.FRAMES)
                self.eventos()
                self.atualizar_sprites()
                self.desenhar_sprites()
        
        def eventos(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.jogando:
                        self.jogando = False
                    self.funciona = False

        def atualizar_sprites(self):
            self.sprites.update
        
        def desenhar_sprites(self):
            self.tela.fill(constantes.PRETO)
            self.sprites.draw(self.tela)
            pygame.display.flip()

        def chamar_arquivo(self):
            diretorio_imagens = os.path.join(os.get.cwd(),'Imagens')
            self.diretorio_sons = os.path.join(os.get.cwd(),'Sons')


        def chamar_tela_start(self):
            pass

        def chamar_game_over (self):
            pass

g = game()
g.chamar_tela_start()

while g.funciona:
    g.new_game()
    g.chamar_game_over()





