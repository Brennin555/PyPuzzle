from cmath import sqrt
import pygame
from pygame.locals import *
from sys import exit
from random import randint # Importa a função que gera números aleatórios

pygame.init()

musicaDeFundo = pygame.mixer.music.load('assets/sounds/aboutYou.mp3')
pygame.mixer.music.set_volume(0.05) #Valores entre 0 e 1
pygame.mixer.music.play(-1)

desafioConcluido = False
ativaCondicao = False
modos = [(0,0),(0,0),(0,0),(0,0)]
mediaPontos = 0
mediaTempo = 0
jogoAtual = 0

somAcerto = pygame.mixer.Sound('assets/sounds/smw_coin.wav')
somAcerto.set_volume(1)

somColisao = pygame.mixer.Sound('assets/sounds/punch.mp3')
somColisao.set_volume(1)

somRato = pygame.mixer.Sound('assets/sounds/aha.mp3')
somRato.set_volume(1)

largura,altura = 640,480
nCol,nLin = 0,0

numeroPecas = 4

pecasRestantes = numeroPecas
raiz= sqrt(numeroPecas)

if raiz.real.is_integer():
    nCol = int(raiz.real)
    nLin = int(raiz.real)
     
tela = pygame.display.set_mode((largura, altura), 0, 32)

x_mouse, y_mouse = 0,0
x_rato, y_rato =  int(largura/2),int(altura/2)
x_taco, y_taco = 300, 300
altura_taco = 80
sprite_taco = None
sprite_rato = None

tempo_rato = 500
velocidade = 10
x_controle = 0
y_controle = velocidade

x_puzzle_begin = 40
y_puzzle_begin = 50
x_puzzle_end = 300
y_puzzle_end = 430

peca_largura = int((x_puzzle_end - x_puzzle_begin)/nLin)
peca_altura = int((y_puzzle_end - y_puzzle_begin)/nCol)

clicouNaPeca = False
pecaSegueMouse = False

clicouNoTaco = False
tacoSegueMouse = False

pontos = 100
tempo = 0
fonte = pygame.font.SysFont("lucidaconsole", 20, True, True)

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
verde = (0, 255, 0)
corFundo = (200, 80, 80)
corObjetos = preto
transparente = (0, 0, 0, 0)


# Fundos
background_fase1 = pygame.image.load('assets/images/fundo_fase1.jpg').convert_alpha()
background_fase1 = pygame.transform.scale(background_fase1, (largura, altura))

background_fase2 = pygame.image.load('assets/images/fundo_fase2.jpg').convert_alpha()
background_fase2 = pygame.transform.scale(background_fase2, (largura, altura))

backgound_inicio = pygame.image.load('assets/images/fundo_inicio.jpg').convert_alpha()
backgound_inicio = pygame.transform.scale(backgound_inicio, (largura, altura))

# Criando clock
clock = pygame.time.Clock()

# Altera o título da janela
pygame.display.set_caption("PyPuzzle")

lista_rato = []
comprimento_inicial = 5
morreu = False
venceu = False
configurando = True
numeroPecas = 16
desenhoEscolhido = 1

desafio = True
zerou = False

x_peca_dist = (x_puzzle_end - x_puzzle_begin)/nLin
y_peca_dist = (y_puzzle_end - y_puzzle_begin)/nCol

matriz_coordenadas = []
matriz_pecas = []
matriz_sprites = []
   
    # Inicialização das matrizes
for i in range(nCol):
    linha = []
    linha_pecas = []
    linha_sprites = []
    
    for j in range(nLin):
        x = x_puzzle_begin + j * x_peca_dist
        y = y_puzzle_begin + i * y_peca_dist
        linha.append((x, y))
        
        x_p = int(randint(300, 600))
        y_p = int(randint(50, 430))
        linha_pecas.append((x_p, y_p))
        linha_sprites.append(f"{i}x{j}")
        
    matriz_coordenadas.append(linha)
    matriz_pecas.append(linha_pecas)
    matriz_sprites.append(linha_sprites)

pecaSegueMouse = False
MUDAR_DIRECAO_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MUDAR_DIRECAO_EVENT, tempo_rato)

CONTAR_TEMPO_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(CONTAR_TEMPO_EVENT, 1000)

def configs_iniciais(numeroPecas, desenhoEscolhido):
    global nCol, nLin, matriz_coordenadas, matriz_pecas, matriz_sprites, sprites, pecasRestantes, raiz, x_peca_dist, y_peca_dist, sprite_taco, peca_largura, peca_altura,altura_taco, sprite_rato, velocidade, x_controle, y_controle
    global background_venceu, background_perdeu, background_bonus
    
    x_controle = 0
    y_controle = velocidade

    
    pecasRestantes = numeroPecas
    print(f'Numero de peças: {numeroPecas}')
    raiz= sqrt(numeroPecas)

    if raiz.real.is_integer():
        nCol = int(raiz.real)
        nLin = int(raiz.real)
        
    peca_largura = int((x_puzzle_end - x_puzzle_begin)/nLin)
    peca_altura = int((y_puzzle_end - y_puzzle_begin)/nCol)
    
    x_peca_dist = (x_puzzle_end - x_puzzle_begin)/nLin
    y_peca_dist = (y_puzzle_end - y_puzzle_begin)/nCol
        
        # Inicialização das matrizes
    matriz_coordenadas = []
    matriz_pecas = []
    matriz_sprites = []
    for i in range(nCol):
        linha = []
        linha_pecas = []
        linha_sprites = []
        
        for j in range(nLin):
            x = x_puzzle_begin + j * x_peca_dist
            y = y_puzzle_begin + i * y_peca_dist
            linha.append((x, y))
            
            x_p = int(randint(300, 600))
            y_p = int(randint(50, 430))
            linha_pecas.append((x_p, y_p))
            linha_sprites.append(f"{i}x{j}")
            
        matriz_coordenadas.append(linha)
        matriz_pecas.append(linha_pecas)
        matriz_sprites.append(linha_sprites)

    # Carregar os sprites
    sprites = []
    for i in range(nCol):
        linha_sprites = []
        for j in range(nLin):
            try:     
                sprite_path = f'assets/fases/{desenhoEscolhido}-4x4/{matriz_sprites[i][j]}.jpg'
                sprite_ = pygame.image.load(sprite_path).convert_alpha()
                sprite_ = pygame.transform.scale(sprite_, (peca_largura, peca_altura))
                linha_sprites.append(sprite_)
            except pygame.error as e:
                print(f"Erro ao carregar sprite {sprite_path}: {e}")
                linha_sprites.append(None)
        sprites.append(linha_sprites)

    # Verifique se os sprites foram carregados corretamente
    for i in range(nCol):
        for j in range(nLin):
            if sprites[i][j] is None:
                print(f"Sprite não carregado em {i}, {j}")
                
    sprite_taco = pygame.image.load('assets/sprites/bat.png').convert_alpha()
    sprite_taco = pygame.transform.scale(sprite_taco, (20, altura_taco))
    
    sprite_rato = pygame.image.load('assets/sprites/rat.png').convert_alpha()
    sprite_rato = pygame.transform.scale(sprite_rato, (20, 50))
    
    background_venceu = pygame.image.load('assets/images/venceu.jpeg').convert_alpha()
    background_venceu = pygame.transform.scale(background_venceu, (largura, altura))
    
    background_perdeu = pygame.image.load('assets/images/perdeu.jpg').convert_alpha()
    background_perdeu = pygame.transform.scale(background_perdeu, (largura, altura))
    



def exibe_mensagem(mensagem, tamanho, cor, pos_x, pos_y):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{mensagem}'
    texto_formatado = fonte.render(mensagem, True, cor)
    tela.blit(texto_formatado, (pos_x, pos_y))

def reiniciar_jogo():
    global pontos, x_rato, y_rato, x_controle, y_controle, venceu, pecaSegueMouse, clicouNaPeca, venceu, configurando, x_taco, y_taco,velocidade, morreu, tempo
    pontos = 100
    tempo = 0
    velocidade = 10
    x_rato = int(largura/2)
    y_rato = int(altura/2)
    x_taco = 300
    y_taco = 300
    
    for i in range(nCol):
        for j in range(nLin):
            matriz_pecas[i][j] = (int(randint(300, 600)), int(randint(50, 430)))
    
    pecaSegueMouse = False
    clicouNaPeca = False
    x_controle = velocidade
    y_controle = 0
        
    configurando = True
    venceu = False
    morreu = False
    
def verificar_vitoria():
    global pecasRestantes
    pecasRestantes = 0
    for i in range(nCol):
        for j in range(nLin):
            if matriz_pecas[i][j] != matriz_coordenadas[i][j]:
                pecasRestantes+=1
                
    if pecasRestantes > 0:
        return False
    return True

def verificar_derrota():
    global pontos
    if pontos <= 0:
        return True
    return False

def verifica_zerou():
    global zerou
    zerou = True
    if zerou:
        return True
    return False
  
while True:
    clock.tick(30)
    
    morreu = verificar_derrota()  
    
    # ---------------------------------------------------------------------------------------------------------CONFIGURAÇÃO---------------------------------------------------------------------------------------------------------
    while configurando:
        tela.fill(azul)
        tela.blit(backgound_inicio, (0, 0))
        
        # Exibir título
        exibe_mensagem("QUEBRA-CABEÇA", 40, branco, largura/2 - 150, 20)
        
        # Mensagem para escolher o número de peças
        exibe_mensagem("Escolha o número de peças:", 30, branco, largura/2 - 200, 100)
        
        # Opções de 4x4 e 5x5 lado a lado
        if numeroPecas == 9:
            opcao1 = pygame.draw.rect(tela, verde, (largura/2 - 150, altura/2 - 70, 100, 50))
        else:
             opcao1 = pygame.draw.rect(tela, branco, (largura/2 - 150, altura/2 - 70, 100, 50))
        exibe_mensagem("3x3", 30, preto, largura/2 - 135, altura/2 - 63)
        
        if numeroPecas == 16:
             opcao2 = pygame.draw.rect(tela, verde, (largura/2 + 50, altura/2 - 70, 100, 50))
        else:
             opcao2 = pygame.draw.rect(tela, branco, (largura/2 + 50, altura/2 - 70, 100, 50))
        exibe_mensagem("4x4", 30, preto, largura/2 + 65, altura/2 - 63)
        
        # Mensagem para escolher o desenho do quebra-cabeça
        exibe_mensagem("Escolha o desenho:", 30, branco, largura/2 - 250, 220)
        
        # Opções de desenho 1 e 2 lado a lado
        if desenhoEscolhido == 1:
            desenho1 = pygame.draw.rect(tela, verde, (largura/2 - 150, altura/2 + 30, 100, 125))
        else:
            desenho1 = pygame.draw.rect(tela, branco, (largura/2 - 150, altura/2 + 30, 100, 125))
            
        imagem1 = pygame.image.load('assets/fases/1.jpeg').convert_alpha()
        imagem1 = pygame.transform.scale(imagem1, (95, 120))
        tela.blit(imagem1, (largura/2 - 150, altura/2 + 30))
        
        if desenhoEscolhido == 2:
            desenho2 = pygame.draw.rect(tela, verde, (largura/2 + 50, altura/2 + 30, 100, 125))
        else:
            desenho2 = pygame.draw.rect(tela, branco, (largura/2 + 50, altura/2 + 30, 100, 125))
        imagem2 = pygame.image.load('assets/fases/2.jpeg').convert_alpha()
        imagem2 = pygame.transform.scale(imagem2, (95, 120))
        tela.blit(imagem2, (largura/2 + 50, altura/2 + 30))
        
        # botao de iniciar
        botao_iniciar = pygame.draw.rect(tela, branco, (largura/2 - 60, altura - 50, 120, 50))
        exibe_mensagem("Iniciar", 30, preto, largura/2 - 50, altura - 50)
        
        trofeu = pygame.image.load('assets/images/trofeu.png').convert_alpha()
        trofeu = pygame.transform.scale(trofeu, (100, 100))
        
        trofeu_misterioso = pygame.image.load('assets/images/trofeuMisterio.png').convert_alpha()
        trofeu_misterioso = pygame.transform.scale(trofeu_misterioso, (100, 100))
        
        trofeuObj = pygame.Rect(520, 350, 100, 100)

        
        img_condicao_trofeu = pygame.image.load('assets/images/condicao.png').convert_alpha()
        img_condicao_trofeu = pygame.transform.scale(img_condicao_trofeu, (300, 400))
        
        background_bonus = pygame.image.load('assets/images/surpresa.jpg').convert_alpha()
        background_bonus = pygame.transform.scale(background_bonus, (largura, altura))
        
        trofeuGrande = pygame.image.load('assets/images/trofeuGrande.png').convert_alpha()
        trofeuGrande = pygame.transform.scale(trofeuGrande, (300, 400))
        
        
        exibe_mensagem("modo 1: " + str(modos[0]), 10, branco, 10, 420)
        exibe_mensagem("modo 2: " + str(modos[1]), 10, branco, 10, 432)
        exibe_mensagem("modo 3: " + str(modos[2]), 10, branco, 10, 444)
        exibe_mensagem("modo 4: " + str(modos[3]), 10, branco, 10, 456)
        
        exibe_mensagem("Média: (" + str(mediaPontos) + ", " + str(mediaTempo) + ")", 10, branco, 500, 456)

        
        if desafioConcluido:
            tela.blit(trofeu, (520, 350))
            exibe_mensagem("Desafio concluído!", 15, branco,500, 300)
            exibe_mensagem("Clique no troféu!", 15, branco, 500, 320)
        else:
            tela.blit(trofeu_misterioso, (520, 350))
            
        if ativaCondicao:
            tela.blit(img_condicao_trofeu, (300, 50))
        
        if botao_iniciar.collidepoint(x_mouse, y_mouse):
            botao_iniciar = pygame.draw.rect(tela, verde, (largura/2 - 60, altura - 50, 120, 50))
            exibe_mensagem("Iniciar", 30, preto, largura/2 - 50, altura - 50)
        
        if zerou:
            tela.blit(background_bonus, (0, 0))
            tela.blit(trofeuGrande, (325, 50))
            exibe_mensagem("Parabéns! Você zerou o jogo!", 20, preto, largura/2 + 10, 20)
            exibe_mensagem("Clique para continuar", 20, branco, largura/2 + 60, 440)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    zerou = False
                    break
            pygame.display.update()
            continue
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                x_mouse, y_mouse = event.pos
                if opcao1.collidepoint(x_mouse, y_mouse):
                    numeroPecas = 9
                    break
                if opcao2.collidepoint(x_mouse, y_mouse):
                    numeroPecas = 16
                    break
                if desenho1.collidepoint(x_mouse, y_mouse):
                    desenhoEscolhido = 1
                    break
                if desenho2.collidepoint(x_mouse, y_mouse):
                    desenhoEscolhido = 2
                    break
                if numeroPecas == 9 and desenhoEscolhido == 1:
                    jogoAtual = 1
                elif numeroPecas == 9 and desenhoEscolhido == 2:
                    jogoAtual = 2
                elif numeroPecas == 16 and desenhoEscolhido == 1:
                    jogoAtual = 3
                elif numeroPecas == 16 and desenhoEscolhido == 2:
                    jogoAtual = 4
                if botao_iniciar.collidepoint(x_mouse, y_mouse):
                    configurando = False
                    configs_iniciais(numeroPecas, desenhoEscolhido)
                    break
                if trofeuObj.collidepoint(x_mouse, y_mouse):
                    if desafioConcluido:
                        zerou = True
                        break
                
            if zerou and event.type != MOUSEBUTTONDOWN:
                tela.blit(background_bonus, (0, 0))
                tela.blit(trofeuGrande, (325, 50))
            elif event.type == MOUSEBUTTONDOWN:
                zerou = False
                    
            if event.type == MOUSEMOTION:
                x_mouse, y_mouse = event.pos
                if botao_iniciar.collidepoint(x_mouse, y_mouse):
                    botao_iniciar = pygame.draw.rect(tela, verde, (largura/2 - 60, altura - 50, 120, 50))
                    exibe_mensagem("Iniciar", 30, preto, largura/2 - 50, altura - 50)
                if trofeuObj.collidepoint(x_mouse, y_mouse):
                    if not desafioConcluido:    
                        ativaCondicao = True
                        break
                else:
                    ativaCondicao = False
                    break
           
        
        pygame.display.update()
        # ---------------------------------------------------------------------------------------------------------FIM CONFIGURAÇÃO---------------------------------------------------------------------------------------------------------
    
    
    tela.fill(corFundo)
    if jogoAtual == 1 or jogoAtual == 3:
        tela.blit(background_fase1, (0, 0))
    elif jogoAtual == 2 or jogoAtual == 4:
        tela.blit(background_fase2, (0, 0))
    
    exibe_mensagem("Tempo: " + str(tempo), 20, branco, 10, 10)
    mensagem = f'Pontos: {pontos}'
    textoFormatado = fonte.render(mensagem, True, branco)    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        x_controle_antigo = x_controle
        y_controle_antigo = y_controle
        
        if event.type == CONTAR_TEMPO_EVENT:
            tempo += 1
                            
        if event.type == MUDAR_DIRECAO_EVENT:
            tempo_rato = randint(500, 2000)
            x_controle = randint(-1, 1) * velocidade
            if x_controle == 0:
                y_controle = randint(-1, 1) * velocidade
                if y_controle == 0:
                    x_controle = velocidade
                    y_controle = 0
            else:
                y_controle = 0
        
        # if event.type == KEYDOWN:
        #     if event.key == K_LEFT:
        #         x_controle = -velocidade
        #         y_controle = 0
        #     if event.key == K_RIGHT:
        #         x_controle = velocidade
        #         y_controle = 0
        #     if event.key == K_UP:
        #         x_controle = 0
        #         y_controle = -velocidade
        #     if event.key == K_DOWN:
        #         x_controle = 0
        #         y_controle = velocidade
        #     if event.key == K_r:
        #         reiniciar_jogo()
                
        if x_controle ==0:
            if x_controle_antigo == 0 and ((y_controle >0 and y_controle_antigo <0) or (y_controle <0 and y_controle_antigo >0)):
                sprite_rato = pygame.transform.rotate(sprite_rato, 180)# print("inverteu vertical")
            if x_controle_antigo<0:
                if y_controle<0: sprite_rato = pygame.transform.rotate(sprite_rato, -90) # print("esquerda pra cima")
                if y_controle>0: sprite_rato = pygame.transform.rotate(sprite_rato, 90) # print("esquerda pra baixo")
            elif x_controle_antigo>0:
                if y_controle<0: sprite_rato = pygame.transform.rotate(sprite_rato, 90) # print("direita pra cima")
                if y_controle>0: sprite_rato = pygame.transform.rotate(sprite_rato, -90) # print("direita pra baixo")
        
        if y_controle ==0:
            if y_controle_antigo == 0 and ((x_controle >0 and x_controle_antigo <0) or (x_controle <0 and x_controle_antigo >0)):
                sprite_rato = pygame.transform.rotate(sprite_rato, 180) # print("inverteu horizontal")
            if y_controle_antigo<0:
                if x_controle<0: sprite_rato = pygame.transform.rotate(sprite_rato, 90) # print("cima pra esquerda")
                if x_controle>0: sprite_rato = pygame.transform.rotate(sprite_rato, -90) # print("cima pra direita")
            elif y_controle_antigo>0:
                if x_controle<0: sprite_rato = pygame.transform.rotate(sprite_rato, -90) # print("baixo pra esquerda")
                if x_controle>0: sprite_rato = pygame.transform.rotate(sprite_rato, 90) # print("baixo pra direita")
                
        if event.type == MOUSEBUTTONDOWN:
            x_mouse, y_mouse = event.pos
            if not pecaSegueMouse:
                for i in range(nCol):
                    for j in range(nLin):
                        x_peca, y_peca = matriz_pecas[i][j]
                        if (x_mouse >= x_peca and x_mouse <= (x_peca + x_peca_dist) and y_mouse >= y_peca and y_mouse <= (y_peca + y_peca_dist)) and matriz_pecas[i][j] != matriz_coordenadas[i][j]:
                            pecaSegueMouse = True
                            clicouNaPeca = True
                            peca_selecionada = (i, j)
                            break
                    if pecaSegueMouse:
                        break
            elif clicouNaPeca:
                pecaSegueMouse = False
                clicouNaPeca = False
                i, j = peca_selecionada
                if abs(matriz_pecas[i][j][0] - matriz_coordenadas[i][j][0]) < 10 and abs(matriz_pecas[i][j][1] - matriz_coordenadas[i][j][1]) < 10:
                    matriz_pecas[i][j] = matriz_coordenadas[i][j]
                    somAcerto.play()
                    pontos += 10
                    velocidade += 1
                    venceu = verificar_vitoria()
            
            if not tacoSegueMouse:
                if x_mouse >= x_taco and x_mouse <= (x_taco + 20) and y_mouse >= y_taco and y_mouse <= (y_taco + altura_taco):
                    tacoSegueMouse = True
                    clicouNoTaco = True
                    break
                if tacoSegueMouse:
                    break
            elif clicouNoTaco:
                tacoSegueMouse = False
                clicouNoTaco = False
                x_taco = x_mouse - 10
                y_taco = y_mouse - 50

    
        if event.type == MOUSEMOTION and pecaSegueMouse:
            x_mouse, y_mouse = event.pos
            x_peca = x_mouse - x_peca_dist / 2
            y_peca = y_mouse - y_peca_dist / 2
            
            peca_rect = pygame.Rect(x_peca, y_peca, x_peca_dist, y_peca_dist)
            for i in range(nCol):
                    for j in range(nLin):
                        if i == peca_selecionada[0] and j == peca_selecionada[1]:
                            matriz_pecas[i][j] = (x_peca, y_peca)
                            
                            if rato.colliderect(peca_rect) and pecaSegueMouse:
                                pecaSegueMouse = False
                                clicouNaPeca = False
                                #pegar valor inteiro da velocidade
                                pontos -= int(abs(velocidade - 5))
                                velocidade += 1
                                matriz_pecas[i][j] = (int(randint(300, 600)), int(randint(50, 430)))
                                play = somRato.play()
                                break
                        if not pecaSegueMouse:
                            break
                        
        if event.type == MOUSEMOTION and tacoSegueMouse:
            x_mouse, y_mouse = event.pos
            x_taco = x_mouse - 10
            y_taco = y_mouse - 50
            
            taco_rect = pygame.Rect(x_taco, y_taco, 20, altura_taco)
            if rato.colliderect(taco_rect) and tacoSegueMouse:
                tacoSegueMouse = False
                clicouNoTaco = False
                if velocidade>2:
                    velocidade = velocidade - 0.5
                somColisao.play()
                break
            
    x_rato += x_controle
    y_rato += y_controle
            
    puzzle = pygame.draw.rect(tela, branco, (x_puzzle_begin, y_puzzle_begin, x_puzzle_end - x_puzzle_begin, y_puzzle_end - y_puzzle_begin), 1)
    
    for i in range(nCol):
        for j in range(nLin):
            x, y = matriz_coordenadas[i][j]
            pygame.draw.rect(tela, branco, (x, y, x_peca_dist, y_peca_dist), 1)
            
    
    for i in range(nCol):
        for j in range(nLin):
            x_peca, y_peca = matriz_pecas[i][j]
            if sprites[i][j] is not None:
                tela.blit(sprites[i][j], (x_peca, y_peca))
                
    rato = pygame.Rect(x_rato, y_rato, 20, 50)

    tela.blit(sprite_rato, (x_rato, y_rato))
    tela.blit(sprite_taco, (x_taco, y_taco))
    lista_cabeca = []
    lista_cabeca.append(x_rato)   
    lista_cabeca.append(y_rato)    
    lista_rato.append(lista_cabeca)


    while morreu:
        tela.fill(preto)
        tela.blit(background_perdeu, (0, 0))
        exibe_mensagem("Você perdeu! :c", 30, branco, largura/2 +45,50)
        exibe_mensagem("Sua pontuação: " + str(pontos), 30, branco, largura/2, 100)
        exibe_mensagem("Pressione R", 30, branco, largura/2 + 50, 200)
        exibe_mensagem("para tentar de novo", 30, branco, largura/2, 250)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    reiniciar_jogo()
        pygame.display.update()
        
        
        
    while venceu:
        tela.fill(preto)
        tela.blit(background_venceu, (0, 0))
        exibe_mensagem("Você venceu! :)", 30, preto, largura/2 +45,50)
        exibe_mensagem("Sua pontuação: " + str(pontos), 30, preto, largura/2, 100)
        exibe_mensagem("Seu tempo: " + str(tempo), 30, preto, largura/2, 150)
        exibe_mensagem("Pressione R", 30, preto, largura/2 + 50, 200)
        exibe_mensagem("para tentar de novo", 30, preto, largura/2, 250)
        
        if pontos > modos[jogoAtual-1][0]:
            modos[jogoAtual-1] = [pontos, tempo]
            mediaPontos = (modos[0][0] + modos[1][0] + modos[2][0] + modos[3][0]) / 4
            mediaTempo = (modos[0][1] + modos[1][1] + modos[2][1] + modos[3][1]) / 4
            
        if mediaPontos >= 180 and mediaTempo <= 60:
            desafioConcluido = True
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    reiniciar_jogo()
                              
        pygame.display.update()
        
            
    if x_rato > largura:
        x_rato = 0
    if x_rato < 0:
        x_rato = largura
    if y_rato < 0:
        y_rato = altura
    if y_rato > altura:
        y_rato = 0
    
    tela.blit(textoFormatado, (450, 40))
    pygame.display.update()