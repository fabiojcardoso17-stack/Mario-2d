"""
Jogo 2D simples em Pygame - versão final mínima (Opção A)
Inclui: menu, pausa, controle de som, salvamento de recorde (save.json)
Idade para todos (conteúdo familiar)
"""

import sys
import os
import random
import json
import pygame

# --- Configurações ---
LARGURA, ALTURA = 900, 600
FPS = 60
COR_CEU = (135, 206, 235)
COR_PLATAFORMA = (100, 50, 20)
COR_MARIO = (255, 0, 0)
COR_MOEDA = (255, 215, 0)
COR_INIMIGO = (0, 0, 0)
GRAVIDADE = 0.8
FORCA_PULO = 16
VELOCIDADE = 5

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
SAVE_FILE = os.path.join(os.path.dirname(__file__), 'save.json')

pygame.init()
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mario 2D - Versão Final Mínima")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 26)
large_font = pygame.font.SysFont(None, 48)

# Áudio
SOM_PULO = None
SOM_MOEDA = None
SOM_HIT = None
MUSICA = None
mixer_ok = False
volume = 0.6
muted = False

try:
    pygame.mixer.init()
    mixer_ok = True
    if os.path.exists(os.path.join(ASSETS_DIR, 'jump.wav')):
        SOM_PULO = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'jump.wav'))
    if os.path.exists(os.path.join(ASSETS_DIR, 'coin.wav')):
        SOM_MOEDA = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'coin.wav'))
    if os.path.exists(os.path.join(ASSETS_DIR, 'hit.wav')):
        SOM_HIT = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'hit.wav'))
    if os.path.exists(os.path.join(ASSETS_DIR, 'music.ogg')):
        MUSICA = os.path.join(ASSETS_DIR, 'music.ogg')
        pygame.mixer.music.load(MUSICA)
        pygame.mixer.music.play(-1)
    # aplicar volume inicial
    pygame.mixer.music.set_volume(volume if not muted else 0)
    if SOM_PULO: SOM_PULO.set_volume(volume if not muted else 0)
    if SOM_MOEDA: SOM_MOEDA.set_volume(volume if not muted else 0)
    if SOM_HIT: SOM_HIT.set_volume(volume if not muted else 0)
except Exception:
    mixer_ok = False
    SOM_PULO = SOM_MOEDA = SOM_HIT = None


def load_save():
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('highscore', 0)
        return 0
    except Exception:
        return 0


def save_highscore(value):
    try:
        data = {'highscore': value}
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception:
        pass


class Jogador:
    def __init__(self, x, y, w=32, h=48):
        self.rect = pygame.Rect(x, y, w, h)
        self.vel_y = 0
        self.no_chao = False
        self.vidas = 3
        self.score = 0
        self.invencivel_tempo = 0
        # tentar carregar sprite
        self.sprite = None
        caminho = os.path.join(ASSETS_DIR, 'mario.png')
        if os.path.exists(caminho):
            try:
                self.sprite = pygame.image.load(caminho).convert_alpha()
                self.sprite = pygame.transform.scale(self.sprite, (w, h))
            except Exception:
                self.sprite = None

    def aplicar_gravidade(self):
        self.vel_y += GRAVIDADE
        self.rect.y += int(self.vel_y)

    def pular(self):
        if self.no_chao:
            self.vel_y = -FORCA_PULO
            self.no_chao = False
            if SOM_PULO and not muted:
                SOM_PULO.play()

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

        # manter dentro da janela horizontal
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

        # invencibilidade decresce com tempo
        if self.invencivel_tempo > 0:
            self.invencivel_tempo -= 1

    def desenhar(self, surface):
        if self.sprite:
            surface.blit(self.sprite, self.rect)
        else:
            # pisca se invencível
            if self.invencivel_tempo > 0 and (self.invencivel_tempo // 6) % 2 == 0:
                return
            pygame.draw.rect(surface, COR_MARIO, self.rect)


class Moeda:
    def __init__(self, x, y, r=10):
        self.pos = pygame.Vector2(x, y)
        self.r = r
        self.collected = False
        self.sprite = None
        caminho = os.path.join(ASSETS_DIR, 'coin.png')
        if os.path.exists(caminho):
            try:
                self.sprite = pygame.image.load(caminho).convert_alpha()
                self.sprite = pygame.transform.scale(self.sprite, (r*2, r*2))
            except Exception:
                self.sprite = None

    def desenhar(self, surface):
        if self.collected:
            return
        if self.sprite:
            rect = self.sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
            surface.blit(self.sprite, rect)
        else:
            pygame.draw.circle(surface, COR_MOEDA, (int(self.pos.x), int(self.pos.y)), self.r)

    def obter_rect(self):
        return pygame.Rect(int(self.pos.x - self.r), int(self.pos.y - self.r), self.r*2, self.r*2)


class Inimigo:
    def __init__(self, x1, x2, y, w=32, h=32, velocidade=2):
        self.rect = pygame.Rect(x1, y - h, w, h)
        self.x1 = x1
        self.x2 = x2
        self.vel = velocidade
        self.sprite = None
        caminho = os.path.join(ASSETS_DIR, 'enemy.png')
        if os.path.exists(caminho):
            try:
                self.sprite = pygame.image.load(caminho).convert_alpha()
                self.sprite = pygame.transform.scale(self.sprite, (w, h))
            except Exception:
                self.sprite = None

    def atualizar(self):
        self.rect.x += self.vel
        if self.rect.x < min(self.x1, self.x2):
            self.rect.x = min(self.x1, self.x2)
            self.vel *= -1
        if self.rect.x > max(self.x1, self.x2):
            self.rect.x = max(self.x1, self.x2)
            self.vel *= -1

    def desenhar(self, surface):
        if self.sprite:
            surface.blit(self.sprite, self.rect)
        else:
            pygame.draw.rect(surface, COR_INIMIGO, self.rect)


def criar_plataformas():
    plataformas = []
    # Chão
    plataformas.append(pygame.Rect(0, ALTURA - 40, LARGURA, 40))
    # Plataformas adicionais (x, y, w, h)
    plataformas.append(pygame.Rect(120, ALTURA - 140, 220, 20))
    plataformas.append(pygame.Rect(420, ALTURA - 220, 200, 20))
    plataformas.append(pygame.Rect(300, ALTURA - 320, 150, 20))
    plataformas.append(pygame.Rect(640, ALTURA - 300, 180, 20))
    return plataformas


def desenhar_plataformas(surface, plataformas):
    for p in plataformas:
        pygame.draw.rect(surface, COR_PLATAFORMA, p)


def criar_moedas(plataformas):
    moedas = []
    # Coloca moedas sobre as plataformas em posições fixas
    for p in plataformas[1:]:
        # três moedas distribuídas pela plataforma
        for i in range(3):
            x = p.x + 20 + i * (p.width - 40) / 2
            y = p.y - 18
            moedas.append(Moeda(int(x), int(y)))
    # algumas moedas soltas no chão
    moedas.append(Moeda(60, ALTURA - 70))
    moedas.append(Moeda(820, ALTURA - 70))
    return moedas


def criar_inimigos(plataformas):
    inimigos = []
    # cria inimigos que patrulham sobre plataformas específicas
    # vincular em cada plataforma um inimigo (onde couber)
    for p in plataformas[1:]:
        x1 = p.x + 10
        x2 = p.x + p.width - 42
        y = p.y
        if x2 - x1 > 40:
            inimigos.append(Inimigo(x1, x2, y, w=32, h=32, velocidade=random.choice([1,2,3])))
    return inimigos


def reset_fase(jogador=None):
    plataformas = criar_plataformas()
    moedas = criar_moedas(plataformas)
    inimigos = criar_inimigos(plataformas)
    if jogador:
        jogador.rect.x = 50
        jogador.rect.y = ALTURA - 100
        jogador.vel_y = 0
        jogador.no_chao = False
        jogador.invencivel_tempo = 0
    return plataformas, moedas, inimigos


def desenhar_hud(surface, jogador, highscore):
    texto = font.render(f"Pontuação: {jogador.score}", True, (0,0,0))
    surface.blit(texto, (12, 8))
    vidas = font.render(f"Vidas: {jogador.vidas}", True, (0,0,0))
    surface.blit(vidas, (12, 36))
    hs = font.render(f"Recorde: {highscore}", True, (0,0,0))
    surface.blit(hs, (12, 64))


def desenhar_texto_central(surface, linhas):
    # linhas: lista de (texto, font, cor)
    y = ALTURA//2 - (len(linhas)*30)//2
    for texto, fnt, cor in linhas:
        surf = fnt.render(texto, True, cor)
        surface.blit(surf, (LARGURA//2 - surf.get_width()//2, y))
        y += surf.get_height() + 8


def aplicar_volume():
    if not mixer_ok:
        return
    vol = 0 if muted else max(0.0, min(1.0, volume))
    pygame.mixer.music.set_volume(vol)
    if SOM_PULO: SOM_PULO.set_volume(vol)
    if SOM_MOEDA: SOM_MOEDA.set_volume(vol)
    if SOM_HIT: SOM_HIT.set_volume(vol)


def menu_loop():
    mostrando_instr = False
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'quit'
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return 'play'
                if evento.key == pygame.K_i:
                    mostrando_instr = not mostrando_instr
                if evento.key == pygame.K_q or evento.key == pygame.K_ESCAPE:
                    return 'quit'
                if evento.key == pygame.K_m:
                    toggle_mute()
                if evento.key == pygame.K_PLUS or evento.key == pygame.K_EQUALS:
                    change_volume(0.1)
                if evento.key == pygame.K_MINUS:
                    change_volume(-0.1)

        janela.fill(COR_CEU)
        desenhar_texto_central(janela, [
            ("Mario 2D - Versão Final Mínima", large_font, (10,10,10)),
            ("Pressione Enter para jogar", font, (0,0,0)),
            ("I: Instruções   M: Mutar   +/-: Volume   Q/Esc: Sair", font, (0,0,0)),
        ])
        if mostrando_instr:
            instr = [
                ("Controles:", large_font, (0,0,0)),
                ("A/D ou ←/→: mover", font, (0,0,0)),
                ("Espaço: pular   P: pausa   R: reiniciar (após Game Over)", font, (0,0,0)),
                ("Colete moedas, derrote inimigos pulando sobre eles. Boa sorte!", font, (0,0,0))
            ]
            y = ALTURA//2 + 80
            for texto, fnt, cor in instr:
                surf = fnt.render(texto, True, cor)
                janela.blit(surf, (LARGURA//2 - surf.get_width()//2, y))
                y += surf.get_height() + 6

        pygame.display.flip()
        clock.tick(FPS)


def toggle_mute():
    global muted
    muted = not muted
    aplicar_volume()


def change_volume(delta):
    global volume, muted
    volume = max(0.0, min(1.0, volume + delta))
    if muted and volume > 0:
        muted = False
    aplicar_volume()


def main():
    highscore = load_save()
    jogador = Jogador(50, ALTURA - 100)
    plataformas, moedas, inimigos = reset_fase(jogador)

    # menu
    escolha = menu_loop()
    if escolha != 'play':
        pygame.quit()
        sys.exit()

    rodando = True
    jogo_rodando = True
    pausado = False

    while rodando:
        dt = clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                if evento.key == pygame.K_SPACE and jogo_rodando and not pausado:
                    jogador.pular()
                if evento.key == pygame.K_r and not jogo_rodando:
                    # reiniciar tudo
                    jogador.vidas = 3
                    jogador.score = 0
                    plataformas, moedas, inimigos = reset_fase(jogador)
                    jogo_rodando = True
                if evento.key == pygame.K_p and jogo_rodando:
                    pausado = not pausado
                if evento.key == pygame.K_m:
                    toggle_mute()
                if evento.key == pygame.K_PLUS or evento.key == pygame.K_EQUALS:
                    change_volume(0.1)
                if evento.key == pygame.K_MINUS:
                    change_volume(-0.1)

        if not jogo_rodando:
            # Game Over screen
            janela.fill(COR_CEU)
            texto_go = large_font.render("GAME OVER", True, (200,20,20))
            sub = font.render("Pressione R para reiniciar ou Esc para sair", True, (0,0,0))
            recorde_txt = font.render(f"Recorde: {highscore}", True, (0,0,0))
            janela.blit(texto_go, (LARGURA//2 - texto_go.get_width()//2, ALTURA//2 - 40))
            janela.blit(sub, (LARGURA//2 - sub.get_width()//2, ALTURA//2 + 10))
            janela.blit(recorde_txt, (LARGURA//2 - recorde_txt.get_width()//2, ALTURA//2 + 40))
            pygame.display.flip()
            continue

        if pausado:
            # somente renderizar sobreposição de pausa
            janela.fill(COR_CEU)
            desenhar_plataformas(janela, plataformas)
            for moeda in moedas:
                moeda.desenhar(janela)
            for inimigo in inimigos:
                inimigo.desenhar(janela)
            jogador.desenhar(janela)
            desenhar_hud(janela, jogador, highscore)
            pause_text = large_font.render("PAUSADO", True, (10,10,10))
            janela.blit(pause_text, (LARGURA//2 - pause_text.get_width()//2, ALTURA//2 - 20))
            pygame.display.flip()
            continue

        teclas = pygame.key.get_pressed()
        dx = 0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx = -VELOCIDADE
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx = VELOCIDADE

        jogador.mover(dx)
        jogador.atualizar_colisoes(plataformas)

        # Atualizar inimigos
        for inimigo in inimigos:
            inimigo.atualizar()

        # Checar colisões com moedas
        for moeda in moedas:
            if not moeda.collected and jogador.rect.colliderect(moeda.obter_rect()):
                moeda.collected = True
                jogador.score += 10
                if SOM_MOEDA and not muted:
                    SOM_MOEDA.play()

        # Checar colisões com inimigos
        for inimigo in inimigos:
            if jogador.rect.colliderect(inimigo.rect):
                if jogador.invencivel_tempo <= 0:
                    # permitir pular sobre inimigo: se jogador estiver caindo
                    if jogador.vel_y > 0 and jogador.rect.bottom - inimigo.rect.top < 20:
                        # inimigo derrotado
                        try:
                            inimigos.remove(inimigo)
                        except ValueError:
                            pass
                        jogador.vel_y = -FORCA_PULO // 2
                        jogador.score += 20
                        break
                    else:
                        jogador.vidas -= 1
                        jogador.invencivel_tempo = FPS * 2  # 2 segundos de invencibilidade
                        jogador.rect.x = 50
                        jogador.rect.y = ALTURA - 100
                        jogador.vel_y = 0
                        if SOM_HIT and not muted:
                            SOM_HIT.play()
                        if jogador.vidas <= 0:
                            jogo_rodando = False
                            # verificar recorde
                            if jogador.score > highscore:
                                highscore = jogador.score
                                save_highscore(highscore)
                        break

        # Desenho
        janela.fill(COR_CEU)
        desenhar_plataformas(janela, plataformas)

        for moeda in moedas:
            moeda.desenhar(janela)

        for inimigo in inimigos:
            inimigo.desenhar(janela)

        jogador.desenhar(janela)

        desenhar_hud(janela, jogador, highscore)

        instrucoes = font.render("A/D ou ←/→: mover   Espaço: pular   P: pausa   M: mutar   +/-: volume", True, (0,0,0))
        janela.blit(instrucoes, (LARGURA - instrucoes.get_width() - 14, 8))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    aplicar_volume()
    main()
