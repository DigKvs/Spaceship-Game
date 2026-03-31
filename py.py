import pygame
import random
import sys


pygame.init()
pygame.mixer.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Collector")
clock = pygame.time.Clock()

BRANCO, PRETO = (255, 255, 255), (0, 0, 0)
AZUL, AMARELO = (50, 150, 255), (255, 215, 0)
VERMELHO, CINZA = (255, 50, 50), (30, 30, 30)
VERDE = (0, 255, 100)

fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
fonte_padrao = pygame.font.SysFont("Arial", 28)

def carregar_imagem(caminho, tamanho, rotacionar=0):
    try:
        img = pygame.image.load(caminho).convert_alpha()
        img = pygame.transform.scale(img, tamanho)
        if rotacionar != 0: img = pygame.transform.rotate(img, rotacionar)
        return img
    except:
        surf = pygame.Surface(tamanho); surf.fill((255, 0, 255))
        return surf

IMAGEM_NAVE = carregar_imagem("imgs/spaceship.png", (50, 50))
IMAGEM_METEORO_BASE = carregar_imagem("imgs/meteor.png", (40, 40), rotacionar=-90)
IMAGEM_MOEDA = carregar_imagem("imgs/coin.png", (30, 30))

imagem_meteoro_atual = IMAGEM_METEORO_BASE

try:
    pygame.mixer.music.load("sons/Crossing the Universe.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
except:
    print("Aviso: Trilha sonora não encontrada.")

try:
    som_moeda = pygame.mixer.Sound("sons/super-mario-coin-sound.mp3")
    som_moeda.set_volume(0.25)
    som_derrota = pygame.mixer.Sound("sons/your_team_lost.mp3") 
    som_derrota.set_volume(0.3)
    
except:
    som_moeda = None
    som_derrota = None
    print("Aviso: Arquivos de som não encontrados na pasta /sons")

estrelas = [[random.randint(0, LARGURA), random.randint(0, ALTURA)] for _ in range(100)]

def desenhar_texto(texto, fonte, cor, x, y, centralizado=False):
    imagem_texto = fonte.render(texto, True, cor)
    pos = (x - imagem_texto.get_width() // 2, y) if centralizado else (x, y)
    tela.blit(imagem_texto, pos)

def main():
    global imagem_meteoro_atual
    estado_jogo = "MENU" 
    jogador = pygame.Rect(LARGURA//2 - 25, ALTURA - 80, 50, 50)
    vel_jogador = 8
    moedas, meteoros = [], []
    pontos = 0
    temporizador_spawn = 0
    
    dificuldade_spawn = 25
    chance_moeda = 6
    tamanho_met = 40
    vel_objetos = 6

    while True:
        clock.tick(60)
        tela.fill(PRETO)
        
        for e in estrelas:
            e[1] += 1
            if e[1] > ALTURA: e[1] = 0
            pygame.draw.circle(tela, (100, 100, 100), e, 1)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE and estado_jogo in ["JOGANDO", "PAUSA"]:
                    estado_jogo = "PAUSA" if estado_jogo == "JOGANDO" else "JOGANDO"

                if estado_jogo == "MENU" and evento.key == pygame.K_SPACE:
                    estado_jogo = "ESCOLHA_DIFICULDADE"

                elif estado_jogo == "ESCOLHA_DIFICULDADE":
                    if evento.key == pygame.K_1: # Facil
                        dificuldade_spawn = 40
                        chance_moeda = 9
                        tamanho_met = 30
                        vel_objetos = 4
                        estado_jogo = "JOGANDO"
                    
                    elif evento.key == pygame.K_2: # Médio
                        dificuldade_spawn = 25
                        chance_moeda = 6
                        tamanho_met = 40
                        vel_objetos = 6
                        estado_jogo = "JOGANDO"
                    
                    elif evento.key == pygame.K_3: # Dificil
                        dificuldade_spawn = 15
                        chance_moeda = 3
                        tamanho_met = 80
                        vel_objetos = 8
                        estado_jogo = "JOGANDO"
                    
                    elif evento.key == pygame.K_4: # Impossivel
                        dificuldade_spawn = 7
                        chance_moeda = 1
                        tamanho_met = 60
                        vel_objetos = 11
                        estado_jogo = "JOGANDO"

                    if estado_jogo == "JOGANDO":
                        imagem_meteoro_atual = pygame.transform.scale(IMAGEM_METEORO_BASE, (tamanho_met, tamanho_met))
                        jogador.x, pontos = LARGURA//2 - 25, 0
                        moedas.clear(); meteoros.clear()

                elif estado_jogo in ["GAME_OVER", "VITORIA"] and evento.key == pygame.K_SPACE:
                    estado_jogo = "MENU"

        if estado_jogo == "MENU":
            desenhar_texto("SPACE COLLECTOR", fonte_titulo, AZUL, LARGURA//2, 120, True)
            pygame.draw.rect(tela, CINZA, (LARGURA//2 - 200, 280, 400, 120), border_radius=10)
            desenhar_texto("COMANDOS:", fonte_padrao, AMARELO, LARGURA//2, 290, True)
            desenhar_texto("SETAS - Mover | ESC - Pausar", fonte_padrao, BRANCO, LARGURA//2, 330, True)
            
            if pygame.time.get_ticks() % 1000 < 500:
                desenhar_texto("PRESSIONE ESPAÇO PARA INICIAR", fonte_padrao, BRANCO, LARGURA//2, 480, True)

        elif estado_jogo == "ESCOLHA_DIFICULDADE":
            desenhar_texto("NÍVEL DE DIFICULDADE", fonte_titulo, AMARELO, LARGURA//2, 120, True)
            desenhar_texto("Selecione a dificuldade (1-4):", fonte_padrao, BRANCO, LARGURA//2, 220, True)
            desenhar_texto("1 - FÁCIL", fonte_padrao, VERDE, LARGURA//2, 280, True)
            desenhar_texto("2 - MÉDIO", fonte_padrao, BRANCO, LARGURA//2, 320, True)
            desenhar_texto("3 - DIFÍCIL", fonte_padrao, AMARELO, LARGURA//2, 360, True)
            desenhar_texto("4 - IMPOSSÍVEL (Boa Sorte!)", fonte_padrao, VERMELHO, LARGURA//2, 400, True)

        elif estado_jogo == "PAUSA":
            desenhar_texto("JOGO PAUSADO", fonte_titulo, AMARELO, LARGURA//2, 250, True)
            desenhar_texto("Pressione ESC para retornar", fonte_padrao, BRANCO, LARGURA//2, 350, True)

        elif estado_jogo == "JOGANDO":
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and jogador.left > 0: jogador.x -= vel_jogador
            if teclas[pygame.K_RIGHT] and jogador.right < LARGURA: jogador.x += vel_jogador
                
            temporizador_spawn += 1
            if temporizador_spawn > dificuldade_spawn:
                temporizador_spawn = 0
                if random.randint(1, 10) <= chance_moeda:
                    moedas.append(pygame.Rect(random.randint(0, LARGURA-30), -30, 30, 30))
                else:
                    meteoros.append(pygame.Rect(random.randint(0, LARGURA-tamanho_met), -tamanho_met, tamanho_met, tamanho_met))
            
            for m in moedas[:]:
                m.y += vel_objetos
                if m.colliderect(jogador):
                    pontos += 1
                    if som_moeda: som_moeda.play()
                    moedas.remove(m)
                elif m.y > ALTURA: moedas.remove(m)
            
            for met in meteoros[:]:
                met.y += (vel_objetos + 1)
                if met.colliderect(jogador): 
                    if som_derrota: som_derrota.play()
                    estado_jogo = "GAME_OVER" 
                elif met.y > ALTURA: meteoros.remove(met)
                    
            if pontos >= 10: estado_jogo = "VITORIA"

            tela.blit(IMAGEM_NAVE, (jogador.x, jogador.y))
            for m in moedas: tela.blit(IMAGEM_MOEDA, (m.x, m.y))
            for met in meteoros: 
                tela.blit(imagem_meteoro_atual, (met.x, met.y))
            
            desenhar_texto(f"MOEDAS: {pontos}/10", fonte_padrao, BRANCO, 20, 20)
            
        elif estado_jogo == "GAME_OVER":
            desenhar_texto("MISSÃO FALHOU!", fonte_titulo, VERMELHO, LARGURA//2, 200, True)
            desenhar_texto("Pressione ESPAÇO para voltar ao Menu", fonte_padrao, BRANCO, LARGURA//2, 350, True)
            
        elif estado_jogo == "VITORIA":
            desenhar_texto("MISSÃO CUMPRIDA!", fonte_titulo, AZUL, LARGURA//2, 200, True)
            desenhar_texto("Pressione ESPAÇO para voltar ao Menu", fonte_padrao, BRANCO, LARGURA//2, 350, True)

        pygame.display.flip()

if __name__ == "__main__":
    main()