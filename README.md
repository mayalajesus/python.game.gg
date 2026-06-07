# python.game.gg

**python.game.gg** e uma plataforma gamificada de aprendizado de Python construida sobre o Discord.

O projeto transforma o estudo de programacao em uma campanha viva: alunos entram em uma Guilda, recebem missoes, ganham XP, sobem de rank, criam projetos reais e avancam com a comunidade.

O bot e o mestre de cerimonia dessa jornada. Ele abre o mapa, registra progresso, organiza entregas, protege os canais e ajuda cada aluno a transformar pratica diaria em portfolio.

---

## O que este bot faz

- Cria uma estrutura minimalista de servidor Discord
- Organiza onboarding de novos alunos
- Registra jogadores, XP, levels e ranks
- Libera missoes da trilha Python
- Avalia entregas com criterios tecnicos
- Registra progresso em banco SQLite local
- Gera ranking da Guilda
- Mantem portfolio interno de projetos
- Aplica cargos automaticamente
- Modera spam, flood, mencoes em massa e convites externos
- Funciona mesmo sem materiais de estudo cadastrados

Os materiais de estudo sao opcionais. A unica edicao manual esperada nos conteudos e adicionar links em `recomendacoes.*`.

---

## Experiencia do aluno

```text
Entrou no servidor
  -> /iniciar
  -> recebe a primeira missao
  -> estuda pelo objetivo da missao
  -> entrega codigo
  -> recebe feedback
  -> ganha XP
  -> sobe de rank
  -> registra projetos no portfolio
```

A proposta nao e apenas assistir conteudo. A proposta e aparecer na Guilda, praticar com consistencia, construir junto e sair com entregas reais.

---

## Ranks da Guilda

| Rank | Papel na jornada |
|---|---|
| Novato | Entrada na Guilda |
| Aventureiro | Primeiras missoes concluidas |
| Cacador de Bugs | Depuracao, erros e pratica |
| Mago das Funcoes | Funcoes e codigo reutilizavel |
| Guardiao dos Dados | Arquivos, registros e dados estruturados |
| Arquiteto de Classes | OOP, testes e organizacao |
| Invocador de APIs | APIs, HTTP e coleta externa |
| Analista Arcano | Pandas, SQL, graficos e analise |
| Engenheiro da Guilda | ETL, pipelines e bancos |
| Mestre dos Dados | Projeto final e portfolio avancado |

Os cargos no Discord sao sincronizados automaticamente com o XP do aluno.

---

## Comandos principais

| Comando | Funcao |
|---|---|
| `/setup_servidor` | Cria categorias, canais, cargos, salas de estudo e permissoes |
| `/iniciar` | Registra o aluno e libera a primeira missao |
| `/guia` | Mostra os comandos principais |
| `/perfil` | Mostra XP, level, rank e progresso |
| `/trilha` | Lista o mapa da jornada |
| `/missao` | Mostra ou ativa uma missao |
| `/conteudo` | Mostra links cadastrados para uma missao, quando existirem |
| `/entregar` | Avalia uma solucao, registra tentativa e concede XP |
| `/ranking` | Mostra o ranking de XP |
| `/registrar_projeto` | Adiciona projeto ao portfolio interno |
| `/portfolio` | Lista projetos registrados |
| `/mod_status` | Mostra historico de moderacao de um membro |
| `/mod_limpar` | Remove mensagens recentes de um canal |

Primeiro comando apos adicionar o bot no servidor:

```text
/setup_servidor
```

Depois teste a jornada:

```text
/iniciar
/missao
/perfil
```

---

## Estrutura criada no Discord

```text
START
├─ boas-vindas
├─ como-funciona
└─ iniciar-jornada

PYTHON.GAME
├─ chat-da-guilda
├─ trilha-python
├─ entregas
├─ ranking
└─ conquistas

SALAS DE ESTUDO
├─ quarto-silencioso
└─ area-do-cafe
```

Permissoes aplicadas pelo bot:

- canais de boas-vindas e explicacao ficam em leitura
- canais da trilha, ranking e conquistas ficam em leitura para alunos e escrita para o bot
- chat da Guilda permite conversa dos alunos onboardados
- entregas permite envio de codigo e anexos
- quarto silencioso permite conectar, mas bloqueia fala
- area do cafe permite conversa por voz

---

## Moderacao e anti-spam

O bot possui uma camada de moderacao conservadora:

- detecta excesso de mensagens em poucos segundos
- detecta mensagens repetidas
- detecta mencoes em massa
- detecta convites externos
- detecta rajadas de links
- remove mensagens quando possui permissao
- registra eventos no SQLite
- aplica timeout em reincidencias quando possui permissao para moderar membros

Eventos de moderacao ficam salvos no banco local para consulta posterior.

---

## Banco de dados

O projeto usa SQLite local.

Arquivo padrao:

```text
data/python_game.sqlite3
```

O banco e criado automaticamente na primeira execucao e armazena:

- alunos
- XP
- ranks
- entregas
- progresso por conteudo
- projetos do portfolio
- configuracao basica do servidor
- eventos de moderacao

O arquivo SQLite nao deve ser versionado.

---

## Conteudos e materiais de estudo

A trilha fica em:

```text
conteudos/
```

Cada conteudo possui um JSON proprio. O bot usa esses arquivos para saber:

- id da missao
- titulo
- modulo
- semana
- objetivo
- conceitos
- XP sugerido
- projeto relacionado
- criterios de validacao

A unica parte que deve ser preenchida manualmente nos JSONs e:

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

Se nao houver links cadastrados, o bot segue normalmente pela missao.

---

## Requisitos

- Python 3.11+
- Um bot Discord criado no Developer Portal
- Token do bot
- ID do servidor de teste
- Permissoes do bot no servidor:
  - gerenciar canais
  - gerenciar cargos
  - enviar mensagens
  - ler historico de mensagens
  - gerenciar mensagens
  - moderar membros
  - usar comandos de aplicativo

---

## Configuracao

Crie um arquivo `.env` na raiz do projeto:

```text
DISCORD_CLIENT_ID=id_do_app
DISCORD_BOT_TOKEN=token_do_bot
DISCORD_GUILD_ID=id_do_servidor_de_teste
COMMAND_PREFIX=/
CONTENT_INDEX_PATH=conteudos/index-conteudos.json
DATABASE_PATH=data/python_game.sqlite3
```

No projeto inteiro, as unicas configuracoes manuais esperadas sao:

- `.env`
- links de estudo nos campos `recomendacoes.*`

---

## Instalacao

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -e ".[dev]"
```

Rodando o bot:

```bash
python -m python_game.bot
```

Quando aparecer no terminal que os slash commands foram sincronizados e o bot conectou ao Gateway, use no Discord:

```text
/setup_servidor
```

---

## Entregas

O comando principal de entrega e:

```text
/entregar
```

Campos esperados:

- `desafio_id`
- `codigo`
- `explicacao`
- `repositorio`, opcional

Tambem existe validacao de formato textual para entregas coladas no canal:

````text
/entregar desafio_id: fundamentos_01

Codigo:
```python
seu codigo aqui
```

Explicacao:
Explique em poucas linhas como sua solucao funciona.
````

Se o envio textual estiver fora do modelo, o bot orienta o reenvio antes da correcao.

---

## Arquitetura

```text
src/python_game/
├─ bot.py                  # inicializacao do bot e registro de cogs
├─ settings.py             # leitura da .env
├─ content_repository.py   # leitura da trilha em JSON
├─ database.py             # SQLite e persistencia do jogo
├─ evaluator.py            # avaliacao inicial das entregas
├─ ranks.py                # ranks, XP minimo e cargos
├─ embeds.py               # mensagens visuais do Discord
├─ discord_helpers.py      # utilitarios de Discord
└─ cogs/
   ├─ setup.py             # criacao do servidor
   ├─ onboarding.py        # iniciar, perfil e guia
   ├─ trail.py             # missoes, entregas, ranking e portfolio
   └─ moderation.py        # anti-spam e comandos de moderacao
```

---

## Testes

```bash
python -m pytest tests
```

Validacoes cobertas:

- carregamento da trilha
- validacao de formato de entrega
- avaliacao de solucoes
- banco SQLite
- ranking
- eventos de moderacao
- protecao contra campos manuais extras nos JSONs

---

## Roadmap

- Backup automatico do banco
- Painel administrativo web
- Relatorios de progresso por turma
- Exportacao de portfolio
- Deploy 24/7
- Avaliacao tecnica mais profunda
- Sistema de temporadas e eventos especiais

---

## Status

MVP operacional.

O bot ja esta preparado para criar o servidor, iniciar alunos, liberar missoes, avaliar entregas, registrar XP, gerar ranking, manter portfolio e aplicar moderacao basica.
