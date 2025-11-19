import pygame
import random
import sys


def show_game_over(screen, font, pontos):
    screen.fill((0, 0, 0))
    grande = pygame.font.SysFont(None, 64)
    texto_go = grande.render('Game Over', True, (255, 0, 0))
    texto_pts = font.render(f'Pontos: {pontos}', True, (255, 255, 255))
    texto_instr = font.render("Pressione R para reiniciar ou Q para sair", True, (200, 200, 200))
    screen.blit(texto_go, (screen.get_width() // 2 - texto_go.get_width() // 2, 180))
    screen.blit(texto_pts, (screen.get_width() // 2 - texto_pts.get_width() // 2, 260))
    screen.blit(texto_instr, (screen.get_width() // 2 - texto_instr.get_width() // 2, 320))
    pygame.display.update()


def game_over_loop():
    # Retorna 'restart' ou 'quit'
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return 'quit'
        pygame.time.wait(50)


def main():
    pygame.init()

    # Dimensões da tela
    largura = 400
    altura = 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Jogo de Corrida')

    # Cores
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    vermelho = (255, 0, 0)
    azul = (0, 0, 255)

    # Carro do jogador
    carro_largura = 50
    carro_altura = 80
    velocidade = 6

    # Inimigo
    inimigo_largura = 80
    inimigo_altura = 50

    # Pontuação
    pontos = 0
    fonte = pygame.font.SysFont(None, 36)

    # Clock
    clock = pygame.time.Clock()

    def reset():
        carro_x = largura // 2 - carro_largura // 2
        carro_y = altura - carro_altura
        inimigo_x = random.randint(0, largura - inimigo_largura)
        inimigo_y = -inimigo_altura
        velocidade_inimigo = 6
        pontos_local = 0
        return carro_x, carro_y, inimigo_x, inimigo_y, velocidade_inimigo, pontos_local

    carro_x, carro_y, inimigo_x, inimigo_y, velocidade_inimigo, pontos = reset()

    rodando = True
    while rodando:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        # Movimento do jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and carro_x > 0:
            carro_x -= velocidade
        if teclas[pygame.K_RIGHT] and carro_x < largura - carro_largura:
            carro_x += velocidade

        # Movimento do inimigo
        inimigo_y += velocidade_inimigo
        if inimigo_y > altura:
            inimigo_y = -inimigo_altura
            inimigo_x = random.randint(0, largura - inimigo_largura)
            pontos += 1
            velocidade_inimigo = min(velocidade_inimigo + 0.3, 12)  # limita velocidade máxima

        # Retângulos
        jogador_rect = pygame.Rect(carro_x, carro_y, carro_largura, carro_altura)
        inimigo_rect = pygame.Rect(inimigo_x, inimigo_y, inimigo_largura, inimigo_altura)

        # Colisão
        tela.fill(preto)
        if jogador_rect.colliderect(inimigo_rect):
            show_game_over(tela, fonte, pontos)
            escolha = game_over_loop()
            if escolha == 'restart':
                carro_x, carro_y, inimigo_x, inimigo_y, velocidade_inimigo, pontos = reset()
                continue
            else:
                break

        # Desenho
        pygame.draw.rect(tela, azul, jogador_rect)
        pygame.draw.rect(tela, vermelho, inimigo_rect)

        texto = fonte.render(f'Pontos: {pontos}', True, branco)
        tela.blit(texto, (10, 10))

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
