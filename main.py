"""
Jogo 2D simples em Pygame - código em Português
Idade para todos (conteúdo familiar)
"""

import sys
import pygame

# --- Configurações ---
LARGURA, ALTURA = 800, 600
FPS = 60
COR_CEU = (135, 206, 235)
COR_PLATAFORMA = (100, 50, 20)
COR_MARIO = (255, 0, 0)
GRAVIDADE = 0.8
FORCA_PULO = 16
VELOCIDADE = 5

pygame.init()
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mario 2D - Versão Inicial")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


class Jogador:
    def __init__(self, x, y, w=32, h=48):
        self.rect = pygame.Rect(x, y, w, h)
        self.vel_y = 0
        self.no_chao = False

    def aplicar_gravidade(self):
        self.vel_y += GRAVIDADE
        self.rect.y += int(self.vel_y)

    def pular(self):
        if self.no_chao:
            self.vel_y = -FORCA_PULO
            self.no_chao = False

    def mover(self, dx):
        self.rect.x += dx

    def atualizar_colisoes(self, plataformas):
        # Colisões verticais
        self.aplicar_gravidade()
        self.no_chao = False
        for p in plataformas:
            if self.rect.colliderect(p):
                # colisão vindo de cima
                if self.vel_y > 0 and self.rect.bottom <= p.top + 20:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.no_chao = True
                # colisão vindo de baixo (teto)
                elif self.vel_y < 0 and self.rect.top >= p.bottom - 20:
                    self.rect.top = p.bottom
                    self.vel_y = 0

    def desenhar(self, surface):
        pygame.draw.rect(surface, COR_MARIO, self.rect)


def criar_plataformas():
    plataformas = []
    # Chão
    plataformas.append(pygame.Rect(0, ALTURA - 40, LARGURA, 40))
    # Plataformas adicionais
    plataformas.append(pygame.Rect(150, ALTURA - 150, 200, 20))
    plataformas.append(pygame.Rect(450, ALTURA - 230, 180, 20))
    plataformas.append(pygame.Rect(320, ALTURA - 320, 120, 20))
    return plataformas


def desenhar_plataformas(surface, plataformas):
    for p in plataformas:
        pygame.draw.rect(surface, COR_PLATAFORMA, p)


def main():
    jogador = Jogador(50, ALTURA - 100)
    plataformas = criar_plataformas()

    rodando = True
    while rodando:
        dt = clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                if evento.key == pygame.K_SPACE:
                    jogador.pular()

        teclas = pygame.key.get_pressed()
        dx = 0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx = -VELOCIDADE
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx = VELOCIDADE

        # Mover horizontalmente e checar colisões simples com paredes da janela
        jogador.mover(dx)
        if jogador.rect.left < 0:
            jogador.rect.left = 0
        if jogador.rect.right > LARGURA:
            jogador.rect.right = LARGURA

        # Atualizar física e colisões com plataformas
        jogador.atualizar_colisoes(plataformas)

        # Desenho
        janela.fill(COR_CEU)
        desenhar_plataformas(janela, plataformas)
        jogador.desenhar(janela)

        # Instruções na tela
        texto = font.render("A/D ou ←/→: mover   Espaço: pular   Esc: sair", True, (0, 0, 0))
        janela.blit(texto, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
