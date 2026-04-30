# Mario-2d

Um jogo 2D simples inspirado em Mario, adequado para "idade para todos" (conteúdo familiar).

Este repositório contém uma versão inicial em Python usando Pygame. O objetivo é ter uma base didática com código em Português para facilitar aprendizado e personalização.

Conteúdo:
- main.py: código principal do jogo (movimento, gravidade, pulo, plataformas).
- requirements.txt: dependências.
- .gitignore: arquivos e pastas para ignorar.
- assets/: pasta para colocar sprites e sons.

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

Próximos passos sugeridos:
- Adicionar sprites do personagem e inimigos em assets/
- Implementar pontuação e fases
- Adicionar som de pulos e efeitos
- Ajustar dificuldade e criação de inimigos

Contribuições são bem-vindas!