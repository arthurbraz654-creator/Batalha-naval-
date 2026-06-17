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
fundo_tela = None

# ==========================================
# --- FUNÇÕES ---
# ==========================================

def tocar_som(nome):
    """Função auxiliar para tocar sons"""
    if sons and nome in sons and sons[nome] is not None:
        sons[nome].play()

def criar_navio(tabuleiro, tamanho):
    """Gera navios normais (1 a 3 casas) aleatoriamente"""
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
    """Gera o Pérola Negra"""
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

def criar_frota(tabuleiro, navios_1, navios_2, navios_3):
    """Posiciona o Pérola Negra e os navios já escolhidos na tela de configuração"""
    partes = 0
    partes += criar_galeao(tabuleiro)

    for _ in range(navios_1): partes += criar_navio(tabuleiro, 1)
    for _ in range(navios_2): partes += criar_navio(tabuleiro, 2)
    for _ in range(navios_3): partes += criar_navio(tabuleiro, 3)

    return partes

def realizar_tiro_computador():
    """Lógica do Computador"""
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
    """Carrega todas as imagens e sons (uma única vez, no início do programa)"""
    global fundo_tela, fonte

    pygame.mixer.init()
    fonte = pygame.font.SysFont("Georgia", 24, bold=True)
    pasta_raiz = os.path.dirname(os.path.abspath(__file__))

    def carregar_img(caminho_relativo, tamanho):
        """Tenta buscar a imagem no caminho. Se não achar, avisa no terminal"""
        try:
            img = pygame.image.load(os.path.join(pasta_raiz, *caminho_relativo)).convert_alpha()
            return pygame.transform.scale(img, tamanho)
        except (FileNotFoundError, pygame.error):
            print(f"AVISO: Imagem faltando -> {'/'.join(caminho_relativo)}")
            return None
            
    def carregar_som(nome_arquivo):
        try: return pygame.mixer.Sound(os.path.join(pasta_raiz, "Áudio", nome_arquivo))
        except (FileNotFoundError, pygame.error): return None

    # --- Carrega Sons ---
    sons["tiro"] = carregar_som("som_tiro.ogg")
    sons["acerto"] = carregar_som("som_acerto.ogg")
    sons["agua"] = carregar_som("som_agua.ogg")
    
    try:
        pygame.mixer.music.load(os.path.join(pasta_raiz, "Áudio", "musica_fundo.ogg"))
        pygame.mixer.music.play(-1) # -1 Toca em loop infinito
    except (FileNotFoundError, pygame.error):
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

def desenhar_tabuleiro(superficie, tabuleiro, offset_x, offset_y, titulo):
    """Desenha a matriz do jogo respeitando as camadas de empilhamento de imagem"""
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
# --- TELAS (MENU / FIM DE JOGO) ---
# ==========================================

def desenhar_texto_com_sombra(tela, texto, fonte, cor_texto, cor_sombra, pos_center):
    """Desenha um texto com uma sombra projetada por trás para dar destaque e profundidade."""
    # Desenha a sombra levemente deslocada (3 pixels para direita e para baixo)
    render_sombra = fonte.render(texto, True, cor_sombra)
    rect_sombra = render_sombra.get_rect(center=(pos_center[0] + 3, pos_center[1] + 3))
    tela.blit(render_sombra, rect_sombra)
    
    # Desenha o texto principal por cima
    render_texto = fonte.render(texto, True, cor_texto)
    rect_texto = render_texto.get_rect(center=pos_center)
    tela.blit(render_texto, rect_texto)

def desenhar_botao(tela, fonte_botao, rect, texto, cor_fundo, pos_mouse):
    """Desenha um botão estilo madeira/pirata com efeito hover."""
    cor_borda = (212, 175, 55)  # Dourado envelhecido
    cor_texto = (245, 245, 220) # Bege (estilo pergaminho)
    
    # Efeito Hover: se o mouse estiver sobre o botão, clareia um pouco a cor de fundo
    if rect.collidepoint(pos_mouse):
        cor_atual = (min(cor_fundo[0] + 30, 255), min(cor_fundo[1] + 30, 255), min(cor_fundo[2] + 30, 255))
    else:
        cor_atual = cor_fundo

    # Desenha o fundo do botão (Madeira)
    pygame.draw.rect(tela, cor_atual, rect, border_radius=8)
    # Desenha a borda externa (Dourada)
    pygame.draw.rect(tela, cor_borda, rect, 3, border_radius=8)
    # Desenha uma borda interna fina escura para dar impressão de placa cravada
    pygame.draw.rect(tela, (30, 20, 10), rect.inflate(-6, -6), 1, border_radius=6)

    # Usa a nossa nova função para desenhar o texto com sombra
    desenhar_texto_com_sombra(tela, texto, fonte_botao, cor_texto, (0, 0, 0), rect.center)

def tela_menu(tela, fonte_titulo, fonte_botao):
    """Tela inicial. Devolve True se o jogador apertar JOGAR, False se for SAIR"""
    pasta_raiz = os.path.dirname(os.path.abspath(__file__))
    try:
        imagem_fundo = pygame.image.load(os.path.join(pasta_raiz, "Imagens", "fotoDoMenu.jpeg")).convert()
        imagem_fundo = pygame.transform.smoothscale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
    except (FileNotFoundError, pygame.error):
        imagem_fundo = None

    botao_jogar = pygame.Rect(LARGURA_TELA // 2 - 180, ALTURA_TELA - 170, 360, 60)
    botao_sair = pygame.Rect(LARGURA_TELA // 2 - 180, ALTURA_TELA - 95, 360, 60)

    relogio = pygame.time.Clock()
    while True:
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    return True
                if botao_sair.collidepoint(evento.pos):
                    return False

        if imagem_fundo:
            tela.blit(imagem_fundo, (0, 0))
        else:
            tela.fill(COR_FUNDO)


        cor_titulo_ouro = (255, 215, 0)
        desenhar_texto_com_sombra(tela, "BATALHA NAVAL", fonte_titulo, cor_titulo_ouro, (0, 0, 0), (LARGURA_TELA // 2, 85))

        # Desenhando os botões usando uma cor de madeira escura (101, 67, 33)
        cor_madeira = (101, 67, 33)
        cor_madeira_escura = (80, 40, 20) # Opção para botões secundários (ex: SAIR)

        # sombra = pygame.Surface((LARGURA_TELA, 110))
        # sombra.set_alpha(160)
        # sombra.fill((255, 255, 255))
        # tela.blit(sombra, (0, 60))

        # titulo = fonte_titulo.render("BATALHA NAVAL", True, (0, 0, 0))
        # tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, 115)))

        desenhar_botao(tela, fonte_botao, botao_jogar, "JOGAR", cor_madeira, pos_mouse)
        desenhar_botao(tela, fonte_botao, botao_sair, "ABANDONAR NAVIO", cor_madeira_escura, pos_mouse)

        pygame.display.flip()
        relogio.tick(FPS)

def tela_fim(tela, fonte_titulo, fonte_botao, mensagem_fim):
    """Tela de resultado. Devolve 'jogar_de_novo' ou 'sair'"""
    botao_jogar_de_novo = pygame.Rect(LARGURA_TELA // 2 - 130, ALTURA_TELA - 170, 260, 60)
    botao_sair = pygame.Rect(LARGURA_TELA // 2 - 130, ALTURA_TELA - 95, 260, 60)
    cor_titulo = (60, 220, 90) if "VOCÊ" in mensagem_fim else (220, 60, 60)

    
    relogio = pygame.time.Clock()
    while True:
        pos_mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar_de_novo.collidepoint(evento.pos):
                    return "jogar_de_novo"
                if botao_sair.collidepoint(evento.pos):
                    return "sair"

        tela.fill(COR_FUNDO)

        titulo = fonte_titulo.render(mensagem_fim, True, cor_titulo)
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 80)))

        desenhar_botao(tela, fonte_botao, botao_jogar_de_novo, "JOGAR DE NOVO", (80, 40, 20), pos_mouse)
        desenhar_botao(tela, fonte_botao, botao_sair, "SAIR", (101, 67, 33), pos_mouse)
        pygame.display.flip()
        relogio.tick(FPS)

def tela_configurar_frota(tela, fonte_titulo, fonte_botao, fonte_label):
    """Tela gráfica para escolher a frota (substitui os input() de terminal).
    A mesma frota escolhida aqui é usada pelo jogador e pelo computador."""
    opcoes = [
        {"nome": "Jangadas (1 casa)", "valor": 3, "minimo": 0, "maximo": 6},
        {"nome": "Botes (2 casas)",   "valor": 2, "minimo": 0, "maximo": 4},
        {"nome": "Barcos (3 casas)",  "valor": 1, "minimo": 0, "maximo": 3},
    ]

    centro_x = LARGURA_TELA // 2
    posicoes_y = [230, 300, 370]

    botoes_menos = [pygame.Rect(centro_x - 170, y - 25, 50, 50) for y in posicoes_y]
    botoes_mais = [pygame.Rect(centro_x + 120, y - 25, 50, 50) for y in posicoes_y]
    botao_confirmar = pygame.Rect(centro_x - 130, ALTURA_TELA - 100, 260, 60)

    relogio = pygame.time.Clock()
    while True:
        pos_mouse = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, opcao in enumerate(opcoes):
                    if botoes_menos[i].collidepoint(evento.pos) and opcao["valor"] > opcao["minimo"]:
                        opcao["valor"] -= 1
                    if botoes_mais[i].collidepoint(evento.pos) and opcao["valor"] < opcao["maximo"]:
                        opcao["valor"] += 1

                if botao_confirmar.collidepoint(evento.pos):
                    return opcoes[0]["valor"], opcoes[1]["valor"], opcoes[2]["valor"]

        tela.fill(COR_FUNDO)

        titulo = fonte_titulo.render("ESCOLHA SUA FROTA", True, (255, 255, 255))
        tela.blit(titulo, titulo.get_rect(center=(centro_x, 90)))

        aviso = fonte_label.render("O Pérola Negra (22 casas) já vem incluso", True, (200, 200, 200))
        tela.blit(aviso, aviso.get_rect(center=(centro_x, 140)))

        for i, opcao in enumerate(opcoes):
            y = posicoes_y[i]

            rotulo = fonte_label.render(opcao["nome"], True, (255, 255, 255))
            tela.blit(rotulo, rotulo.get_rect(midright=(centro_x - 190, y)))

            desenhar_botao(tela, fonte_botao, botoes_menos[i], "-", (80, 40, 20), pos_mouse)
            desenhar_botao(tela, fonte_botao, botoes_mais[i], "+", (80, 40, 20), pos_mouse)

            valor_render = fonte_titulo.render(str(opcao["valor"]), True, (255, 255, 255))
            tela.blit(valor_render, valor_render.get_rect(center=(centro_x, y)))

        desenhar_botao(tela, fonte_botao, botao_confirmar, "JOGAR", (101, 67, 33), pos_mouse)

        pygame.display.flip()
        relogio.tick(FPS)

# ==========================================
# --- CONTROLE DE PARTIDA ---
# ==========================================

def nova_partida(navios_1, navios_2, navios_3):
    """Reseta os tabuleiros e monta as duas frotas com a configuração escolhida"""
    global tabuleiro_real_jogador, tabuleiro_real_computador
    global tabuleiro_ataques_jogador, tabuleiro_ataques_computador
    global acertos_jogador, acertos_computador
    global partes_navio_jogador, partes_navio_computador

    tabuleiro_real_jogador = [[AGUA for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
    tabuleiro_real_computador = [[AGUA for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
    tabuleiro_ataques_jogador = [[AGUA for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
    tabuleiro_ataques_computador = [[AGUA for _ in range(DIMENSAO)] for _ in range(DIMENSAO)]
    acertos_jogador = 0
    acertos_computador = 0

    partes_navio_jogador = criar_frota(tabuleiro_real_jogador, navios_1, navios_2, navios_3)
    partes_navio_computador = criar_frota(tabuleiro_real_computador, navios_1, navios_2, navios_3)

def jogar_partida(tela):
    """Roda uma partida até alguém vencer. Devolve a mensagem de resultado"""
    global acertos_jogador

    vez = "JOGADOR"
    mensagem_fim = ""
    clock = pygame.time.Clock()

    offset_x_jogador = MARGEM
    offset_x_ataque = MARGEM * 2 + (TAMANHO_CELULA * DIMENSAO)
    offset_y_geral = MARGEM

    while not mensagem_fim:

        if fundo_tela:
            tela.blit(fundo_tela, (0, 0))
        else:
            tela.fill(COR_FUNDO)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and vez == "JOGADOR":
                mouse_x, mouse_y = event.pos

                if (offset_x_ataque <= mouse_x < offset_x_ataque + (DIMENSAO * TAMANHO_CELULA)) and \
                   (offset_y_geral <= mouse_y < offset_y_geral + (DIMENSAO * TAMANHO_CELULA)):

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

        if vez == "COMPUTADOR":
            pygame.time.wait(200)
            acertou = realizar_tiro_computador()
            if not acertou:
                vez = "JOGADOR"

        if acertos_jogador == partes_navio_computador:
            mensagem_fim = "VOCÊ VENCEU!"
        elif acertos_computador == partes_navio_jogador:
            mensagem_fim = "O COMPUTADOR VENCEU!"

        desenhar_tabuleiro(tela, tabuleiro_real_jogador, offset_x_jogador, offset_y_geral, "SEUS NAVIOS")
        desenhar_tabuleiro(tela, tabuleiro_ataques_jogador, offset_x_ataque, offset_y_geral, "SEUS ATAQUES")

        pygame.display.flip()
        clock.tick(FPS)

    pygame.time.wait(700)  # deixa o tabuleiro final visível um instante
    return mensagem_fim

# ==========================================
# --- MAIN ---
# ==========================================

if __name__ == "__main__":

    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Batalha Naval - A Fúria do Pérola Negra")

    fonte_titulo = pygame.font.SysFont("Georgia", 72, bold=True)
    fonte_botao = pygame.font.SysFont("Georgia", 26, bold=True)
    fonte_label = pygame.font.SysFont("Georgia", 22, bold=True)

    inicializar_midias()

    app_rodando = True
    while app_rodando:

        if not tela_menu(tela, fonte_titulo, fonte_botao):
            break

        jogando = True
        while jogando:
            navios_1, navios_2, navios_3 = tela_configurar_frota(tela, fonte_titulo, fonte_botao, fonte_label)
            nova_partida(navios_1, navios_2, navios_3)
            mensagem_fim = jogar_partida(tela)
            escolha = tela_fim(tela, fonte_titulo, fonte_botao, mensagem_fim)
            if escolha == "sair":
                jogando = False
                app_rodando = False

    pygame.quit()
    sys.exit()
