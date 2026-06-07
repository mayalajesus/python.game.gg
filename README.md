# python.game Bot

Bot do Discord responsavel por orquestrar a jornada gamificada do projeto **python.game**.

Ele deve funcionar como o nucleo da plataforma:

- criacao minimalista do servidor
- onboarding dos alunos
- liberacao de missoes
- recomendacao de conteudos
- validacao do formato de entrega
- avaliacao inicial das solucoes
- registro de XP
- controle de cargos
- rankings
- portfolio interno
- banco SQLite local dentro do projeto

## Estrutura

```text
python.game/
├─ pyproject.toml
├─ .env.example
├─ cronograma-python-game.md
├─ conteudos/
│  ├─ index-conteudos.json
│  ├─ schema-conteudo.json
│  └─ modulo-*/
├─ src/python_game/
│  ├─ bot.py
│  ├─ settings.py
│  ├─ content_repository.py
│  ├─ database.py
│  ├─ evaluator.py
│  └─ cogs/
│     ├─ setup.py
│     ├─ onboarding.py
│     └─ trail.py
└─ tests/
   └─ test_content_repository.py
```

Os conteudos recomendados ficam dentro da pasta do projeto, em:

```text
conteudos/
```

O bot usa `conteudos/index-conteudos.json` para localizar os arquivos individuais de cada etapa da trilha.

## Configuracao

Crie uma `.env` dentro de `python.game/` com:

```text
DISCORD_CLIENT_ID=id_do_app
DISCORD_BOT_TOKEN=token_do_bot
DISCORD_GUILD_ID=id_do_servidor_de_teste
COMMAND_PREFIX=/
CONTENT_INDEX_PATH=conteudos/index-conteudos.json
DATABASE_PATH=data/python_game.sqlite3
```

No projeto inteiro, as unicas configuracoes manuais sao:

- `.env`, para credenciais e IDs do Discord
- links de estudo em `conteudos/**.json`, apenas dentro de `recomendacoes.*`

Os demais campos dos JSONs sao parte da trilha e devem permanecer como definidos pelo projeto.

## Comandos principais

- `/setup_servidor`: cria categorias, canais, cargos e salas de estudo.
- `/iniciar`: registra o aluno, atribui o rank inicial e libera a primeira missao.
- `/guia`: mostra os comandos da Guilda.
- `/perfil`: mostra XP, rank, level e progresso.
- `/trilha`: lista o mapa da jornada.
- `/missao`: mostra ou ativa uma missao.
- `/conteudo`: mostra links cadastrados para a missao, se existirem.
- `/entregar`: avalia a solucao, registra tentativa, concede XP e avanca a missao.
- `/ranking`: mostra o placar de XP.
- `/registrar_projeto`: adiciona projeto ao portfolio interno.
- `/portfolio`: lista os projetos registrados.

Os materiais de estudo sao opcionais. Se os links ainda nao foram adicionados, o bot continua guiando o aluno pelo objetivo, criterios da missao, entrega e feedback.

## Banco de dados

O bot usa SQLite em `data/python_game.sqlite3`.

Esse arquivo guarda:

- alunos
- XP
- entregas
- progresso por conteudo
- projetos do portfolio
- configuracao basica do servidor

O banco e criado automaticamente na primeira execucao.

## Rodando localmente

```bash
cd python.game
python -m venv .venv
.venv/Scripts/activate
pip install -e ".[dev]"
python -m python_game.bot
```

## Regra de entrega

Mesmo com comandos slash no Discord, o bot mantem uma validacao de formato para entregas textuais.

Formato esperado:

````text
/entregar desafio_id: fundamentos_01

Codigo:
```python
seu codigo aqui
```

Explicacao:
Explique em poucas linhas como sua solucao funciona.
````

Se o aluno enviar fora desse modelo, o bot nao deve corrigir a atividade.
