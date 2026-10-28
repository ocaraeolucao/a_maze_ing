*This project has been created as part of the 42 curriculum by luvieira, jobezerr.*

# A-Maze-ing

## Description
A-Maze-ing é uma aplicação desenvolvida em Python 3.10+ para geração, solução e visualização interativa de labirintos 2D. O projeto suporta a criação de labirintos perfeitos (com caminho único entre entrada e saída) e imperfeitos (tabuleiros jogáveis no estilo Pac-Man com múltiplos caminhos e sem áreas abertas de 3x3), incorporando o padrão visual "42" em células bloqueadas quando as dimensões do mapa assim o permitem.

A solução do menor caminho é calculada de forma otimizada via algoritmo de Busca em Largura (BFS) e o resultado final é exportado em um arquivo de texto com codificação hexadecimal para a grade do labirinto e as coordenadas de solução.

<img src="https://images4.imgbox.com/cd/73/gmbF3JIH_o.png" alt="Visualização do Labirinto"/>

*Exemplo do labirinto gerado no terminal com caminho e cores personalizadas.*

---

## Instructions

### Instalação e Compilação do Pacote
Para instalar as dependências do projeto e construir o pacote reutilizável `mazegen` em formato Wheel (`.whl`):

```bash
make install
make build
```

### Execução
Para executar o programa principal com um arquivo de configuração:

```bash
make run
# Ou diretamente via interpretador:
python3 a_maze_ing.py config.txt
```

### Interações no Menu Interativo
- `1`: Re-gerar um novo labirinto mantendo as configurações atuais.
- `2`: Exibir / Ocultar o menor caminho do labirinto.
- `3`: Alternar as cores das paredes do labirinto.
- `4`: Sair da aplicação.

---

## Configuration File Format
O arquivo de configuração `config.txt` aceita pares chave-valor no formato `KEY=VALUE` (linhas iniciadas com `#` são tratadas como comentários). As chaves obrigatórias e opcionais são:

| Chave | Descrição | Exemplo |
| --- | --- | --- |
| `WIDTH` | Largura do labirinto em número de células | `WIDTH=20` |
| `HEIGHT` | Altura do labirinto em número de células | `HEIGHT=15` |
| `ENTRY` | Coordenadas da entrada no formato `x,y` | `ENTRY=0,0` |
| `EXIT` | Coordenadas da saída no formato `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Caminho do arquivo para exportação hexadecimal | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` para caminho único; `False` para múltiplos caminhos | `PERFECT=True` |
| `SEED` | (Opcional) Semente para reprodução determinística | `SEED=42` |

---

## Generation Algorithm & Technical Choices

### Algoritmo Escolhido
Foi utilizado o algoritmo **Recursive Backtracker (DFS)** implementado de forma iterativa com o uso de uma pilha explícita. Para o modo imperfeito (`PERFECT=False`), o algoritmo é complementado por rotinas de remoção controlada de paredes e criação de malhas/loops sem becos sem saída adicionais.

|Maze PERFECT=True | Maze PERFECT=False |
|:--- | :--- |
| <img src="https://images4.imgbox.com/12/0c/21ISMIoM_o.png" alt="Maze PERFECT=True"/> | <img src="https://images4.imgbox.com/02/fd/u0DeOpwW_o.png" alt="Maze PERFECT=False"/> |
|*Comparação entre o modo PERFECT=True (caminho único) e PERFECT=False (loops e múltiplos caminhos).*|

### Por que esta escolha?
1. **Corredores Longos e Sinuosos:** O DFS produz labirintos desafiadores e esteticamente agradáveis com caminhos bem definidos.
2. **Segurança de Memória:** A versão iterativa com pilha evita estourar o limite de recursão do Python (*recursion limit*) em grades de grande dimensão.
3. **Padrão "42":** Permite marcar previamente o conjunto de células do padrão "42" como células já visitadas/bloqueadas antes do algoritmo esculpir os corredores.

---

## Reusable Module (`mazegen`)
A lógica de geração e solução de labirintos está encapsulada no pacote `mazegen-0.1.0-py3-none-any.whl` localizado na raiz do repositório. Ele é independente da aplicação de terminal e pode ser instalado em qualquer ambiente Python.

### Exemplo de Uso do Módulo

```python
from maze_generator import MazeGenerator
from maze_solver import bfs_maze, reconstruct_maze_path, path_to_directions

# Instanciação do gerador
generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_pos=(19, 14),
    perfect=True,
    seed=42
)
maze = generator.generate()

# Resolução via BFS
parents = bfs_maze(maze, (0, 0), (19, 14))
path = reconstruct_maze_path(parents, (19, 14))
directions = path_to_directions(path)

print("Matriz gerada:", maze)
print("Caminho (N,E,S,W):", directions)
```

---

## Team & Project Management

### Divisão de Papéis
- **Lucas Vieira:** Desenvolvimento do motor de geração do labirinto (`maze_generator.py`), algoritmos de padrão "42", modo imperfeito e empacotamento (`pyproject.toml`, `LICENSE.md`).
- **João Victor:** Leitura e validação de configurações, algoritmo de solução BFS (`maze_solver.py`), renderização ASCII (`maze_display.py`), menu interativo (`a_maze_ing.py`), `Makefile` e documentação.

### Evolução do Planejamento
- **Fase 1:** Definição do contrato de tipos e funções entre os integrantes.
- **Fase 2:** Desenvolvimento paralelo da geração (Lucas) e da aplicação/solucionador (João).
- **Fase 3:** Integração dos módulos, refinamento do menu interativo e tratamento do padrão "42".
- **Fase 4:** Empacotamento em arquivo `.whl`, automação com `Makefile` e verificação estrita de tipos com `mypy`.

### O que funcionou bem e Melhorias
- **Positivo:** A separação clara de responsabilidades via contrato de interface permitiu um avanço contínuo sem conflitos de código.
- **A Melhorar:** Padronizar o gerenciamento de versões e testes em ambientes virtuais isolados desde o início do projeto.

### Ferramentas Utilizadas
- Python 3.10+, `mypy` (verificação estrita de tipos), `flake8` (conformidade PEP 8), `setuptools`/`build` (criação de pacotes) e Git.

---

## Resources & AI Usage

### Recursos
- Teoria dos Grafos, busca em profundidade (DFS) e busca em largura (BFS).
- Documentação oficial do Python (`typing`, `setuptools`, `mypy`).

### Uso de IA
Seguindo as diretrizes do Capítulo II do *subject*:
- **Debugging & Linters:** Auxílio na interpretação e resolução de avisos do `mypy --strict`.
- **Documentação:** Estruturação dos tópicos do `README.md` e verificação das exigências da 42.
- **Código:** Toda a lógica principal, manipulação de bits das paredes e algoritmos de busca foram compreendidos, implementados e validados pelos desenvolvedores.
