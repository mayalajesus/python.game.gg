# Python.Game

> Uma Guilda de Programadores no Discord para aprender Python com missões, XP, ranks, feedback técnico e projetos reais.

**Python.Game** transforma o aprendizado de Python em uma jornada gamificada inspirada em progressão de RPG.

Em vez de apenas consumir aulas, o jogador entra na Guilda, recebe missões práticas, entrega código, ganha XP, sobe de rank e constrói um portfólio com projetos reais. A trilha começa nos fundamentos de Python e avança até competências voltadas para **Engenharia de Dados**.

```text
Aprender Python
  -> praticar com missões
  -> receber feedback
  -> acumular XP
  -> subir de rank
  -> construir portfólio
  -> avançar para Dados
```

---

## 1. Hero Section

Python.Game é um bot de Discord criado para transformar estudo em progressão.

O servidor nasce como uma Guilda minimalista: poucos canais, onboarding guiado, missões visíveis por etapa, ranking da comunidade, conquistas sociais e um mapa claro da jornada.

Cada entrega movimenta o jogo. Cada projeto fortalece o portfólio. Cada rank mostra que o jogador saiu da teoria e construiu alguma coisa.

---

## 2. Visão Geral

### O que é

Python.Game é uma plataforma gamificada de aprendizado de Python construída sobre o Discord.

O bot organiza a experiência, cria a estrutura do servidor, registra progresso, libera missões, avalia entregas, distribui XP, gerencia cargos e mantém a comunidade protegida.

### Qual problema resolve

Muita gente desiste de programação nos primeiros meses por falta de direção, excesso de teoria, pouco feedback, sensação de estagnação e ausência de comunidade.

Python.Game resolve isso criando uma jornada prática:

- direção clara por missões
- progressão visível por XP e ranks
- feedback sobre entregas
- comunidade para troca e consistência
- portfólio construído ao longo da trilha
- foco em prática, não em consumo passivo

### Por que existe

Porque aprender programação funciona melhor quando existe ciclo de ação:

```text
Estudar -> praticar -> entregar -> receber feedback -> melhorar -> repetir
```

---

## 3. Jornada do Jogador

O jogador não entra no servidor vendo tudo de uma vez.

Ele passa por um onboarding curto, ganha o cargo de Aprendiz e só então acessa a trilha principal.

```text
🏰 Entrar na Guilda
        ↓
🧭 Passar pelo onboarding
        ↓
🎒 Tornar-se Aprendiz
        ↓
📜 Receber missão
        ↓
📚 Estudar
        ↓
📦 Entregar código
        ↓
🧠 Receber feedback
        ↓
⭐ Ganhar XP
        ↓
🏆 Subir de rank
        ↓
📂 Construir portfólio
```

A jornada foi desenhada para criar senso de avanço sem transformar o projeto em um curso tradicional.

---

## 4. Sistema de Progressão

Python.Game usa progressão de jogo para tornar o aprendizado visível.

### XP

Cada atividade relevante gera experiência.

Exemplos:

| Atividade | XP |
|---|---:|
| Entrada na Guilda | 10 |
| Aula ou etapa concluída | 10 |
| Exercício concluído | 30 |
| Missão principal | 100 |
| Projeto concluído | 300 |
| Ajudar outro membro | 20 |
| Compartilhar projeto | 50 |

### Levels

O level representa progresso acumulado.

O bot calcula o level a partir do XP registrado no banco local.

### Ranks

Os ranks são cargos do Discord sincronizados automaticamente pelo bot.

| Rank | XP mínimo | Papel na jornada |
|---|---:|---|
| 🥚 Novato | 0 | Entrada na Guilda |
| ⚔️ Aventureiro | 300 | Primeiras missões concluídas |
| 🛡️ Caçador de Bugs | 900 | Depuração, erros e prática |
| 🔮 Mago das Funções | 1600 | Funções e código reutilizável |
| 📚 Guardião dos Dados | 2600 | Arquivos, registros e dados estruturados |
| 🏰 Arquiteto de Classes | 3800 | OOP, testes e organização |
| 🌐 Invocador de APIs | 5200 | APIs, HTTP e coleta externa |
| 📊 Analista Arcano | 6800 | Pandas, SQL, gráficos e análise |
| ⚙️ Engenheiro da Guilda | 8400 | ETL, pipelines e bancos |
| 👑 Mestre dos Dados | 10500 | Projeto final e portfólio avançado |

### Conquistas

Conquistas são anúncios sociais publicados pelo bot quando um jogador completa marcos importantes.

Exemplo:

```text
🏆 Conquista Desbloqueada

Usuário:
@Dominic

Conquista:
Primeira Função

Descrição:
Criou sua primeira função Python.
```

---

## 5. O Mestre da Guilda (Bot)

O bot é o núcleo da plataforma.

Ele atua como mestre da jornada, organizador do servidor e registrador de progresso.

Responsabilidades principais:

- criar categorias, canais, embeds e botões
- guiar onboarding de novos jogadores
- liberar canais após entrada na Guilda
- registrar jogadores no SQLite
- registrar XP, levels e ranks
- sincronizar cargos do Discord
- publicar missões no feed da trilha
- validar modelo de entrega
- avaliar soluções enviadas
- retornar feedback técnico
- liberar próxima missão após aprovação
- anunciar conquistas
- atualizar ranking
- registrar projetos no portfólio
- aplicar moderação e anti-spam

### Guarda da Guilda

A camada de moderação protege a comunidade contra:

- excesso de mensagens em poucos segundos
- mensagens repetidas
- menções em massa
- convites externos
- rajadas de links

Quando o bot possui permissão, ele remove mensagens, registra eventos no banco e aplica timeout em reincidências.

---

## 6. Estrutura do Servidor

O servidor é minimalista e guiado.

```text
🏰 START
├─ 01-👋-bem-vindo
├─ 02-🎯-como-funciona
└─ 03-✅-iniciar-jornada

🌎 PYTHON.GAME
├─ 🗺️-mapa-da-jornada
├─ 🧩-trilha-python
├─ 📦-entregas
├─ 🏆-ranking
└─ 📜-conquistas

🏕️ COMUNIDADE
├─ 💬-chat-da-guilda
├─ 🕯️ sala-de-foco
└─ ☕ area-do-cafe
```

### 🏰 START

Área de onboarding.

| Canal | Função |
|---|---|
| `01-👋-bem-vindo` | Recebe o jogador e cria curiosidade |
| `02-🎯-como-funciona` | Explica a jornada em poucos segundos |
| `03-✅-iniciar-jornada` | Registra o jogador e libera o cargo `🎒 Aprendiz` |

### 🌎 PYTHON.GAME

Área principal de estudo e progressão.

| Canal | Função |
|---|---|
| `🗺️-mapa-da-jornada` | Mostra a progressão completa da trilha |
| `🧩-trilha-python` | Feed de missões, somente bot envia mensagens |
| `📦-entregas` | Canal para entregas dos jogadores |
| `🏆-ranking` | Ranking da Guilda atualizado pelo bot |
| `📜-conquistas` | Anúncios sociais de conquistas |

### 🏕️ COMUNIDADE

Área social.

| Canal | Função |
|---|---|
| `💬-chat-da-guilda` | Taverna social para networking e progresso |
| `🕯️ sala-de-foco` | Estudo silencioso, microfone bloqueado |
| `☕ area-do-cafe` | Voz aberta para conversa, carreira, tecnologia e comunidade |

### Permissões

- Visitantes veem apenas o START
- Canais da trilha são liberados após o cargo `🎒 Aprendiz`
- `🧩-trilha-python`, `🏆-ranking` e `📜-conquistas` são canais de bot
- `📦-entregas` aceita mensagens e anexos
- `🕯️ sala-de-foco` permite conectar, mas bloqueia fala
- `☕ area-do-cafe` permite conversa por voz

---

## 7. Comandos

| Comando | Função |
|---|---|
| `/setup_servidor` | Cria categorias, canais, cargos, botões e permissões |
| `/iniciar` | Inicia a jornada por comando, como alternativa ao botão |
| `/guia` | Mostra comandos principais |
| `/perfil` | Mostra XP, level, rank e progresso |
| `/trilha` | Lista conteúdos cadastrados na trilha |
| `/missao` | Mostra ou ativa uma missão |
| `/conteudo` | Mostra links cadastrados para uma missão, quando existirem |
| `/formato` | Mostra o modelo oficial de entrega |
| `/validar_entrega` | Valida se uma entrega textual está no formato correto |
| `/entregar` | Avalia uma solução, registra tentativa e concede XP |
| `/ranking` | Mostra ranking de XP |
| `/registrar_projeto` | Adiciona projeto ao portfólio interno |
| `/portfolio` | Lista projetos registrados |
| `/mod_status` | Mostra histórico de moderação de um membro |
| `/mod_limpar` | Remove mensagens recentes de um canal |

Primeiro comando após adicionar o bot:

```text
/setup_servidor
```

Esse comando pode ser executado novamente para reorganizar a estrutura sem duplicar os canais principais.

---

## 8. Arquitetura

```text
src/python_game/
├─ bot.py
├─ settings.py
├─ content_repository.py
├─ database.py
├─ delivery_validation.py
├─ evaluator.py
├─ game_service.py
├─ ranks.py
├─ embeds.py
├─ views.py
├─ discord_helpers.py
└─ cogs/
   ├─ setup.py
   ├─ onboarding.py
   ├─ trail.py
   └─ moderation.py
```

| Módulo | Responsabilidade |
|---|---|
| `bot.py` | Inicialização do bot, intents, cogs e views persistentes |
| `settings.py` | Leitura da `.env` |
| `content_repository.py` | Carregamento dos JSONs da trilha |
| `database.py` | Persistência SQLite |
| `delivery_validation.py` | Validação do modelo textual de entrega |
| `evaluator.py` | Avaliação inicial das soluções |
| `game_service.py` | Fluxo central de entrada do jogador |
| `ranks.py` | Definição dos ranks e limites de XP |
| `embeds.py` | Embeds reutilizáveis |
| `views.py` | Botões e views do Discord |
| `discord_helpers.py` | Utilitários de cargos, ranks e validações |
| `cogs/setup.py` | Criação e organização do servidor |
| `cogs/onboarding.py` | Entrada, perfil e guia |
| `cogs/trail.py` | Missões, entregas, ranking e portfólio |
| `cogs/moderation.py` | Anti-spam e comandos de moderação |

---

## 9. Banco de Dados

Python.Game usa SQLite local.

Arquivo padrão:

```text
data/python_game.sqlite3
```

O banco é criado automaticamente na primeira execução.

Ele armazena:

- jogadores
- XP
- levels
- ranks
- eventos de XP
- entregas
- progresso por conteúdo
- projetos do portfólio
- configuração do servidor
- eventos de moderação

O arquivo SQLite não deve ser versionado.

---

## 10. Conteúdos e Missões

A trilha fica em:

```text
conteudos/
```

Cada missão possui um JSON próprio.

O bot usa esses arquivos para carregar:

- id da missão
- título
- módulo
- semana
- ordem
- nível
- objetivo
- conceitos
- XP sugerido
- projeto relacionado
- formato de entrega
- critérios de validação

### Materiais de estudo

Os materiais são opcionais.

A única parte dos JSONs que deve ser preenchida manualmente é:

```text
recomendacoes.pdfs
recomendacoes.videos
recomendacoes.artigos
recomendacoes.sites_oficiais
recomendacoes.documentacao
recomendacoes.cursos
recomendacoes.repositorios
recomendacoes.ferramentas
recomendacoes.outros
```

Se uma missão não tiver links cadastrados, o bot segue normalmente sem avisar o jogador sobre ausência de material.

### Entrega

No canal `📦-entregas`, o modelo social é:

```text
Missão: ambiente_desenvolvimento
Github: sem repositorio
Observações: instalei o ambiente e validei as ferramentas.
```

Para correção técnica, XP e progressão automática, use:

```text
/entregar
```

Campos esperados:

- `desafio_id`
- `codigo`
- `explicacao`
- `repositorio`, opcional

Na missão 0, o campo `codigo` deve trazer as evidências:

```text
python --version
git --version
```

E o campo `explicacao` deve listar o checklist dos apps instalados.

O bot só inicia a correção quando a entrega chega no modelo esperado.

---

## 11. Instalação

### Requisitos

- Python 3.11+
- Um bot criado no Discord Developer Portal
- Token do bot
- ID do servidor de teste
- Permissões do bot no servidor:
  - gerenciar canais
  - gerenciar cargos
  - enviar mensagens
  - ler histórico de mensagens
  - gerenciar mensagens
  - moderar membros
  - usar comandos de aplicativo

### Instalar dependências

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -e ".[dev]"
```

### Rodar o bot

```bash
python -m python_game.bot
```

Quando o terminal indicar que o bot conectou ao Gateway, use no Discord:

```text
/setup_servidor
```

---

## 12. Configuração

Crie um arquivo `.env` na raiz do projeto:

```text
DISCORD_CLIENT_ID=id_do_app
DISCORD_BOT_TOKEN=token_do_bot
DISCORD_GUILD_ID=id_do_servidor_de_teste
COMMAND_PREFIX=/
CONTENT_INDEX_PATH=conteudos/index-conteudos.json
DATABASE_PATH=data/python_game.sqlite3
```

No projeto inteiro, as únicas configurações manuais esperadas são:

- `.env`
- links de estudo nos campos `recomendacoes.*`

---

## 13. Desenvolvimento

### Testes

```bash
python -m pytest tests
```

Validações cobertas:

- carregamento da trilha
- validação de formato de entrega
- avaliação de soluções
- banco SQLite
- ranking
- eventos de moderação
- proteção contra campos manuais extras nos JSONs

### Estrutura do projeto

```text
python.game/
├─ conteudos/
├─ src/python_game/
├─ tests/
├─ pyproject.toml
├─ cronograma-python-game.md
└─ README.md
```

### Contribuição

Boas contribuições para este projeto devem preservar três princípios:

- a jornada precisa continuar clara para o jogador
- a estrutura do Discord deve permanecer minimalista
- o bot não deve depender de materiais de estudo para funcionar

Sugestões de contribuição:

- novos testes
- melhoria de validação das entregas
- novas conquistas
- evolução do avaliador técnico
- melhorias no setup do servidor
- expansão da trilha de Engenharia de Dados
- ferramentas de backup e operação

---

## 14. Roadmap

```text
[x] Estrutura guiada do servidor
[x] Onboarding com botões
[x] Cargo inicial de Aprendiz
[x] Sistema de XP
[x] Levels
[x] Ranks automáticos
[x] Feed de missões
[x] Validação de entrega
[x] Avaliação técnica inicial
[x] Ranking
[x] Conquistas sociais
[x] Portfólio interno
[x] Moderação e anti-spam
[x] Banco SQLite local
[ ] Backup automático do banco
[ ] Painel administrativo web
[ ] Relatórios de progresso por turma
[ ] Exportação de portfólio
[ ] Deploy 24/7
[ ] Avaliação técnica mais profunda
[ ] Temporadas
[ ] Eventos especiais
```

---

## Status

**MVP operacional.**

Python.Game já está preparado para criar o servidor, iniciar jogadores, liberar missões, avaliar entregas, registrar XP, gerar ranking, anunciar conquistas, manter portfólio e proteger a comunidade.
