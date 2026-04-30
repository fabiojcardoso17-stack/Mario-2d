# Mario-2d

Um jogo 2D simples inspirado em Mario, adequado para "idade para todos" (conteúdo familiar).

Esta versão foi incrementada para incluir:
- Moedas colecionáveis
- Inimigos simples que patrulham plataformas
- Pontuação e vidas
- Tela de fim de jogo e reinício (pressione R para reiniciar)
- Carregamento opcional de sprites e sons em assets/ (se não existirem, o jogo usa formas simples)

Arquivos principais:
- main.py: código principal do jogo (movimento, gravidade, pulo, plataformas, moedas, inimigos, HUD)
- requirements.txt: dependências.
- .gitignore: arquivos e pastas para ignorar.
- assets/: pasta para sprites e sons (opcional)

Como executar (ambiente com Python 3.8+):
1. Criar e ativar um ambiente virtual (recomendado):
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate   # Windows
2. Instalar dependências:
   pip install -r requirements.txt
3. Executar o jogo:
   python main.py

Controles:
- A / ← : mover para a esquerda
- D / → : mover para a direita
- Espaço : pular
- Esc : sair
- R : reiniciar após game over

Assets opcionais:
- assets/mario.png — sprite do jogador
- assets/coin.png — sprite da moeda
- assets/enemy.png — sprite do inimigo
- assets/jump.wav, assets/coin.wav, assets/hit.wav — sons opcionais

Se os arquivos de assets não existirem, o jogo usará formas desenhadas com retângulos/círculos.

Próximos passos sugeridos:
- Adicionar sprites reais e ajustar colisões conforme necessário
- Implementar múltiplas fases com mapas externos (JSON/CSV)
- Adicionar animação do jogador e inimigos
- Salvar recordes e sistema de vidas/continuações

Contribuições são bem-vindas!
