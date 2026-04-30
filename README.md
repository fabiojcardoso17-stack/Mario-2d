# Mario-2d

Um jogo 2D simples inspirado em Mario, adequado para "idade para todos" (conteúdo familiar).

Esta versão final mínima (Opção A) inclui:
- Menu inicial e tela de instruções
- Pausa durante o jogo
- Controle de som: M para mutar/desmutar, + / - para ajustar volume
- Salvamento automático do recorde (high score) em save.json
- Moedas colecionáveis, inimigos, pontuação e vidas

Arquivos principais:
- main.py: código principal do jogo (movimento, gravidade, pulo, plataformas, moedas, inimigos, HUD, menu, som, save)
- requirements.txt: dependências.
- .gitignore
- assets/: pasta para sprites e sons (opcional)
- save.json: arquivo para armazenar recorde (gerado automaticamente se não existir)

Como executar (ambiente com Python 3.8+):
1. Criar e ativar um ambiente virtual (recomendado)
   - macOS/Linux:
     python -m venv venv
     source venv/bin/activate
   - Windows:
     python -m venv venv
     venv\Scripts\activate
2. Instalar dependências:
   pip install -r requirements.txt
3. Executar o jogo:
   python main.py

Controles (novos e antigos):
- Enter: iniciar o jogo a partir do menu
- I: abrir instruções no menu
- Q / Esc: sair do menu / sair do jogo
- A / ← : mover para a esquerda
- D / → : mover para a direita
- Espaço : pular
- P : pausar / despausar o jogo
- M : mutar / desmutar o áudio
- + / - : aumentar / diminuir volume
- R : reiniciar após game over

Onde o recorde é salvo:
- O arquivo save.json contém o campo "highscore". Se o jogador bater o recorde, o valor é atualizado automaticamente.

Assets opcionais:
- Coloque em assets/ para substituir os desenhos simples:
  - mario.png (player)
  - coin.png (moeda)
  - enemy.png (inimigo)
  - jump.wav, coin.wav, hit.wav, music.ogg (sons/música)

Se os arquivos de assets não existirem, o jogo usará formas básicas.

Próximos passos sugeridos:
- Animação do jogador (parado/andar/pular)
- Fases em JSON e câmera com scroll lateral
- Workflow para criar builds (PyInstaller)

Contribuições são bem-vindas!
