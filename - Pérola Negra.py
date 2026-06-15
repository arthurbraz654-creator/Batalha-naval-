# ==========================================
# --- BIBLIOTECAS ---
# ==========================================

import os
import random
import sys
import pygame

# ==========================================
# --- VARIÁVEIS GLOBAIS ---
# ==========================================

# Constantes Básicas do Jogo
AGUA = 0
ERRO = 101 # Representa o tiro na água (água remexida)

# IDs específicos para as embarcações normais
JANGADA = 1
BOTE_ESQ = 2
BOTE_DIR = 3
BOTE_CIMA = 4
BOTE_BAIXO = 5
BARCO_ESQ = 6
BARCO_MEIO_H = 7
BARCO_DIR = 8
BARCO_CIMA = 9
BARCO_MEIO_V = 10
BARCO_BAIXO = 11

# Como ele tem 24 pedaços (3 colunas x 8 linhas), reservamos um bloco de IDs só para ele
ID_BASE_PEROLA_NEGRA = 200 

# Lista Mestra: Define tudo o que é considerado "Navio" para a lógica de registrar acertos
TIPOS_NAVIO = [
    JANGADA, 
    BOTE_ESQ, BOTE_DIR, BOTE_CIMA, BOTE_BAIXO,
    BARCO_ESQ, BARCO_MEIO_H, BARCO_DIR, BARCO_CIMA, BARCO_MEIO_V, BARCO_BAIXO
]
# Adiciona todos os 24 IDs do Pérola Negra na lista de alvos válidos
TIPOS_NAVIO.extend(range(ID_BASE_PEROLA_NEGRA, ID_BASE_PEROLA_NEGRA + 24))

# Constantes do Tabuleiro e Dimensões Visuais
DIMENSAO = 12 # Tabuleiro 12x12
TAMANHO_CELULA = 40
TAMANHO_DANO = 20 # Metade do tamanho da célula para não tampar o navio inteiro
MARGEM = 50
LARGURA_TELA = (TAMANHO_CELULA * DIMENSAO * 2) + (MARGEM * 3) # 2 Tabuleiros lado a lado
ALTURA_TELA = (TAMANHO_CELULA * DIMENSAO) + (MARGEM * 2)
FPS = 30

# Cores usadas como "plano B" caso os sprites não carreguem
COR_FUNDO = (30, 30, 40)
COR_TEXTO = (255, 255, 255)
CORES_CELULA = {
    AGUA: (0, 105, 148),
    "ACERTO_FALLBACK": (255, 50, 50),
    ERRO: (200, 200, 200)
}
COR_PADRAO_NAVIO = (100, 100, 100)

# Matrizes que representam o "cérebro" do jogo
tabuleiro_real_jogador = [[AGUA for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
tabuleiro_real_computador = [[AGUA for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
tabuleiro_ataques_jogador = [[AGUA for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
tabuleiro_ataques_computador = [[AGUA for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]

# Contadores de condição de vitória
acertos_jogador = 0
acertos_computador = 0
partes_navio_jogador = 0
partes_navio_computador = 0

# Dicionários globais que guardarão as imagens, sons e a fonte do texto
sprites = {}
sons = {}
fonte = None

# ==========================================
# --- FUNÇÕES ---
# ==========================================

def tocar_som(nome):
    """Função auxiliar para tocar sons apenas se eles existirem e tiverem sido carregados."""
    if sons and nome in sons and sons[nome] is not None:
        sons[nome].play()

def criar_navio(tabuleiro, tamanho):
    """Gera navios normais (1 a 3 casas) aleatoriamente no tabuleiro."""
    while True:
        linha = random.randint(0, DIMENSAO - 1)
        coluna = random.randint(0, DIMENSAO - 1)
        direcao = random.choice(["H", "V"])
        pode_colocar = True

        # Lógica para Navios Horizontais
        if direcao == "H":
            if coluna + tamanho - 1 >= DIMENSAO: # Verifica se não vaza do mapa
                continue
            for i in range(tamanho): # Verifica se já tem navio ali
                if tabuleiro[linha][coluna + i] != AGUA:
                    pode_colocar = False
                    break
            
            if pode_colocar:
                for i in range(tamanho): # Atribui o ID correto da imagem
                    if tamanho == 1:
                        tabuleiro[linha][coluna + i] = JANGADA
                    elif tamanho == 2:
                        if i == 0: tabuleiro[linha][coluna + i] = BOTE_ESQ
                        else: tabuleiro[linha][coluna + i] = BOTE_DIR
                    elif tamanho == 3:
                        if i == 0: tabuleiro[linha][coluna + i] = BARCO_ESQ
                        elif i == 1: tabuleiro[linha][coluna + i] = BARCO_MEIO_H
                        else: tabuleiro[linha][coluna + i] = BARCO_DIR
                return tamanho

        # Lógica para Navios Verticais
        else: 
            if linha + tamanho - 1 >= DIMENSAO:
                continue
            for i in range(tamanho):
                if tabuleiro[linha + i][coluna] != AGUA:
                    pode_colocar = False
                    break
            
            if pode_colocar:
                for i in range(tamanho):
                    if tamanho == 1:
                        tabuleiro[linha + i][coluna] = JANGADA
                    elif tamanho == 2:
                        if i == 0: tabuleiro[linha + i][coluna] = BOTE_CIMA
                        else: tabuleiro[linha + i][coluna] = BOTE_BAIXO
                    elif tamanho == 3:
                        if i == 0: tabuleiro[linha + i][coluna] = BARCO_CIMA
                        elif i == 1: tabuleiro[linha + i][coluna] = BARCO_MEIO_V
                        else: tabuleiro[linha + i][coluna] = BARCO_BAIXO
                return tamanho

def criar_galeao(tabuleiro):
    """Gera o Pérola Negra de tamanho 3x8 no tabuleiro."""
    while True:
        # Garante que o navio inteiro caiba dentro das dimensões (12x12)
        linha_inicial = random.randint(0, DIMENSAO - 8)  
        coluna_inicial = random.randint(0, DIMENSAO - 3) 
        
        pode_colocar = True
        
        for l in range(8):
            for c in range(3):
                if l == 0 and c in [0, 2]:
                    continue
                if tabuleiro[linha_inicial + l][coluna_inicial + c] != AGUA:
                    pode_colocar = False
                    break
            if not pode_colocar:
                break
                
        if pode_colocar:
            for l in range(8):
                for c in range(3):
                    if l == 0 and c in [0, 2]:
                        continue # Não coloca hitbox nas quinas superiores
                    id_fatia = ID_BASE_PEROLA_NEGRA + (l * 3) + c
                    tabuleiro[linha_inicial + l][coluna_inicial + c] = id_fatia
            return 22

def criar_frota(tabuleiro):
    """Orquestra a criação de todos os navios de um jogador."""
    partes = 0
    partes += criar_galeao(tabuleiro)
    print("-> Pérola Negra (3x8) posicionado nas águas!")

    try:
        navios_1 = int(input("Jangadas (1 casa): "))
        navios_2 = int(input("Botes (2 casas): "))
        navios_3 = int(input("Barcos (3 casas): "))
    except ValueError:
        print("Entrada inválida. Usando frota padrão (3, 2, 1).")
        navios_1, navios_2, navios_3 = 3, 2, 1

    for _ in range(navios_1): partes += criar_navio(tabuleiro, 1)
    for _ in range(navios_2): partes += criar_navio(tabuleiro, 2)
    for _ in range(navios_3): partes += criar_navio(tabuleiro, 3)

    return partes

def realizar_tiro_computador():
    """Lógica da Inteligência Artificial (e também da retaliação do Boss)."""
    global acertos_computador
    
    linha_pc = random.randint(0, DIMENSAO - 1)
    coluna_pc = random.randint(0, DIMENSAO - 1)
    
    # PC nunca atira onde já atirou antes
    while tabuleiro_ataques_computador[linha_pc][coluna_pc] != AGUA:
        linha_pc = random.randint(0, DIMENSAO - 1)
        coluna_pc = random.randint(0, DIMENSAO - 1)
        
    tocar_som("tiro")
    pygame.time.wait(200)
    
    id_alvo_pc = tabuleiro_real_jogador[linha_pc][coluna_pc]
    
    if id_alvo_pc in TIPOS_NAVIO:
        balas = random.randint(1, 3)
        valor_acerto = id_alvo_pc + (balas * 1000)
        
        tabuleiro_real_jogador[linha_pc][coluna_pc] = valor_acerto
        tabuleiro_ataques_computador[linha_pc][coluna_pc] = valor_acerto
        acertos_computador += 1
        tocar_som("acerto")
        return True
    else:
        tabuleiro_ataques_computador[linha_pc][coluna_pc] = ERRO
        tabuleiro_real_jogador[linha_pc][coluna_pc] = ERRO 
        tocar_som("agua")
        return False

# ==========================================
# --- FUNÇÕES GRÁFICAS ---
# ==========================================

def inicializar_midias():
    """Carrega todas as imagens e sons das pastas específicas."""
    pygame.init()
    pygame.mixer.init()
    
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Batalha Naval - A Fúria do Pérola Negra")
    fonte_local = pygame.font.SysFont("Arial", 24, bold=True)
    pasta_raiz = os.path.dirname(os.path.abspath(__file__))

    def carregar_img(caminho_relativo, tamanho):
        """Tenta buscar a imagem no caminho. Se não achar, avisa amigavelmente no terminal."""
        try:
            img = pygame.image.load(os.path.join(pasta_raiz, *caminho_relativo)).convert_alpha()
            return pygame.transform.scale(img, tamanho)
        except FileNotFoundError:
            print(f"AVISO: Imagem faltando -> {'/'.join(caminho_relativo)}")
            return None
            
    def carregar_som(nome_arquivo):
        try: return pygame.mixer.Sound(os.path.join(pasta_raiz, "Áudio", nome_arquivo))
        except FileNotFoundError: return None

    # --- Carrega Sons ---
    sons["tiro"] = carregar_som("som_tiro.ogg")
    sons["acerto"] = carregar_som("som_acerto.ogg")
    sons["agua"] = carregar_som("som_agua.ogg")
    
    try:
        pygame.mixer.music.load(os.path.join(pasta_raiz, "Áudio", "musica_fundo.ogg"))
        pygame.mixer.music.play(-1) # -1 Toca em loop infinito
    except FileNotFoundError:
        pass 

    fundo_tela = carregar_img(["Imagens", "Parallax", "fundo.png"], (LARGURA_TELA, ALTURA_TELA))
    
    sprites[AGUA] = carregar_img(["Imagens", "Gráficos", "agua.png"], (TAMANHO_CELULA, TAMANHO_CELULA))
    sprites[ERRO] = carregar_img(["Imagens", "Gráficos", "agua_remexida.png"], (TAMANHO_CELULA, TAMANHO_CELULA))
    
    t_dano = (TAMANHO_DANO, TAMANHO_DANO) # Tamanho 20x20
    sprites["dano_1"] = carregar_img(["Imagens", "Gráficos", "dano_1.png"], t_dano)
    sprites["dano_2"] = carregar_img(["Imagens", "Gráficos", "dano_2.png"], t_dano)
    sprites["dano_3"] = carregar_img(["Imagens", "Gráficos", "dano_3.png"], t_dano)

    sprites[JANGADA] = carregar_img(["Imagens", "Embarcações", "jangada.png"], (TAMANHO_CELULA, TAMANHO_CELULA))

    bote_esq = carregar_img(["Imagens", "Embarcações", "4 - bote_esq.png"], (TAMANHO_CELULA, TAMANHO_CELULA))
    bote_dir = carregar_img(["Imagens", "Embarcações", "5 - bote_dir.png"], (TAMANHO_CELULA, TAMANHO_CELULA))
    sprites[BOTE_ESQ] = bote_esq
    sprites[BOTE_DIR] = bote_dir
    # Rotaciona para gerar os barcos verticais
    if bote_esq: sprites[BOTE_CIMA] = pygame.transform.rotate(bote_esq, -90)
    if bote_dir: sprites[BOTE_BAIXO] = pygame.transform.rotate(bote_dir, -90)

    barco_esq = carregar_img(["Imagens", "Embarcações", "1 - barco_esq.png"], (TAMANHO_CELULA, TAMANHO_CELULA))
    barco_meio = carregar_img(["Imagens", "Embarcações", "2 - barco_meio.png"], (TAMANHO_CELULA, TAMANHO_CELULA))
    barco_dir = carregar_img(["Imagens", "Embarcações", "3 - barco_dir.png"], (TAMANHO_CELULA, TAMANHO_CELULA))
    sprites[BARCO_ESQ] = barco_esq
    sprites[BARCO_MEIO_H] = barco_meio
    sprites[BARCO_DIR] = barco_dir
    if barco_esq: sprites[BARCO_CIMA] = pygame.transform.rotate(barco_esq, -90)
    if barco_meio: sprites[BARCO_MEIO_V] = pygame.transform.rotate(barco_meio, -90)
    if barco_dir: sprites[BARCO_BAIXO] = pygame.transform.rotate(barco_dir, -90)

    # Carrega e fatia o Pérola Negra
    img_perola = carregar_img(["Imagens", "Embarcações", "pérola_negra.png"], (TAMANHO_CELULA * 3, TAMANHO_CELULA * 8))
    if img_perola:
        for l in range(8):
            for c in range(3):
                retangulo = pygame.Rect(c * TAMANHO_CELULA, l * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA)
                sprites[ID_BASE_PEROLA_NEGRA + (l * 3) + c] = img_perola.subsurface(retangulo)

    for chave in list(sprites.keys()):
        if sprites[chave] is None:
            del sprites[chave]

    return tela, fundo_tela, fonte_local

def desenhar_tabuleiro(superficie, tabuleiro, offset_x, offset_y, titulo):
    """Desenha a matriz do jogo respeitando as camadas de empilhamento de imagem."""
    if fonte:
        texto = fonte.render(titulo, True, COR_TEXTO)
        superficie.blit(texto, (offset_x, offset_y - 35))

    for linha in range(DIMENSAO):
        for coluna in range(DIMENSAO):
            x = offset_x + (coluna * TAMANHO_CELULA)
            y = offset_y + (linha * TAMANHO_CELULA)
            valor = tabuleiro[linha][coluna]
            
            # --- CAMADA 1: Fundo Fixo ---
            # Sempre desenha água por baixo de tudo para não bugar a transparência
            if sprites and AGUA in sprites:
                superficie.blit(sprites[AGUA], (x, y))
            else:
                pygame.draw.rect(superficie, CORES_CELULA[AGUA], (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
            
            # --- CAMADA 2: Navios Intactos ou Erros ---
            if valor == ERRO:
                if sprites and ERRO in sprites:
                    superficie.blit(sprites[ERRO], (x, y))
                else:
                    pygame.draw.rect(superficie, CORES_CELULA[ERRO], (x, y, TAMANHO_CELULA, TAMANHO_CELULA))

            elif valor in TIPOS_NAVIO:
                if sprites and valor in sprites:
                    superficie.blit(sprites[valor], (x, y))
                else:
                    pygame.draw.rect(superficie, COR_PADRAO_NAVIO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
            
            # --- CAMADA 3: Tiros Acertados ---
            elif valor >= 1000:
                # O ID foi multiplicado. Ex: 3205 = 3 balas no pedaço de navio 205.
                qtd_balas = valor // 1000
                id_navio = valor % 1000
                
                # Desenha o pedaço do navio normal primeiro
                if sprites and id_navio in sprites:
                    superficie.blit(sprites[id_navio], (x, y))
                else:
                    pygame.draw.rect(superficie, COR_PADRAO_NAVIO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
                
                # Desenha os buracos de bala por cima, centralizados na célula
                dano_key = f"dano_{qtd_balas}"
                if sprites and dano_key in sprites:
                    offset_centralizar = (TAMANHO_CELULA - TAMANHO_DANO) // 2
                    coordenadas_centralizadas = (x + offset_centralizar, y + offset_centralizar)
                    superficie.blit(sprites[dano_key], coordenadas_centralizadas)
                else:
                    pygame.draw.rect(superficie, CORES_CELULA["ACERTO_FALLBACK"], (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 4)
            
            # --- CAMADA 4: Linhas de Grade ---
            pygame.draw.rect(superficie, (0, 0, 0), (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)

# ==========================================
# --- MAIN ---
# ==========================================

if __name__ == "__main__":
    
    # 1. Fase de Configuração no Terminal
    print("=============================")
    print("   CONFIGURAÇÃO DA PARTIDA   ")
    print("=============================\n")
    
    print(">>> FROTA DO JOGADOR <<<")
    partes_navio_jogador = criar_frota(tabuleiro_real_jogador)
    
    print("\n>>> FROTA DO COMPUTADOR <<<")
    partes_navio_computador = criar_frota(tabuleiro_real_computador)

    # 2. Inicialização da Interface Gráfica
    tela, fundo_tela, fonte = inicializar_midias()
    clock = pygame.time.Clock()

    rodando = True
    vez = "JOGADOR"
    mensagem_fim = ""

    # Offsets para colocar os dois tabuleiros lado a lado
    offset_x_jogador = MARGEM
    offset_x_ataque = MARGEM * 2 + (TAMANHO_CELULA * DIMENSAO)
    offset_y_geral = MARGEM

    # 3. Game Loop
    while rodando:
        
        if fundo_tela: 
            tela.blit(fundo_tela, (0, 0))
        else: 
            tela.fill(COR_FUNDO)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and vez == "JOGADOR" and not mensagem_fim:
                mouse_x, mouse_y = event.pos
                
                if (offset_x_ataque <= mouse_x < offset_x_ataque + (DIMENSAO * TAMANHO_CELULA)) and \
                   (offset_y_geral <= mouse_y < offset_y_geral + (DIMENSAO * TAMANHO_CELULA)):
                    
                    # Converte a coordenada XY do mouse para Linha e Coluna da Matriz
                    coluna = (mouse_x - offset_x_ataque) // TAMANHO_CELULA
                    linha = (mouse_y - offset_y_geral) // TAMANHO_CELULA
                    
                    if tabuleiro_ataques_jogador[linha][coluna] == AGUA:
                        
                        tocar_som("tiro")
                        pygame.time.wait(200)
                        
                        id_alvo = tabuleiro_real_computador[linha][coluna]
                        
                        if id_alvo in TIPOS_NAVIO:
                            balas = random.randint(1, 3)
                            valor_acerto = id_alvo + (balas * 1000) 
                            
                            tabuleiro_real_computador[linha][coluna] = valor_acerto
                            tabuleiro_ataques_jogador[linha][coluna] = valor_acerto
                            acertos_jogador += 1
                            tocar_som("acerto")
                            
                            # Se atirar no Pérola Negra, ele atira de volta
                            if ID_BASE_PEROLA_NEGRA <= id_alvo <= ID_BASE_PEROLA_NEGRA + 23:
                                pygame.time.wait(400)
                                realizar_tiro_computador() 
                                
                        else:
                            tabuleiro_ataques_jogador[linha][coluna] = ERRO
                            tocar_som("agua")
                            vez = "COMPUTADOR"

        if vez == "COMPUTADOR" and not mensagem_fim:
            pygame.time.wait(600)
            acertou = realizar_tiro_computador()
            if not acertou:
                vez = "JOGADOR"
                
        if acertos_jogador == partes_navio_computador:
            mensagem_fim = "VOCÊ VENCEU!"
        elif acertos_computador == partes_navio_jogador:
            mensagem_fim = "O COMPUTADOR VENCEU!"

        # Renderização dos Tabuleiros
        desenhar_tabuleiro(tela, tabuleiro_real_jogador, offset_x_jogador, offset_y_geral, "SEUS NAVIOS")
        desenhar_tabuleiro(tela, tabuleiro_ataques_jogador, offset_x_ataque, offset_y_geral, "SEUS ATAQUES")

        if mensagem_fim:
            texto_fim = fonte.render(mensagem_fim, True, (0, 255, 0) if "VOCÊ" in mensagem_fim else (255, 0, 0))
            rect_texto = texto_fim.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA - MARGEM // 2))
            
            # Caixa preta translúcida atrás do texto para dar leitura
            fundo_texto = pygame.Surface((rect_texto.width + 20, rect_texto.height + 10))
            fundo_texto.fill((0, 0, 0))
            fundo_texto.set_alpha(180)
            tela.blit(fundo_texto, (rect_texto.x - 10, rect_texto.y - 5))
            tela.blit(texto_fim, rect_texto)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
