# python.game Bot

Bot do Discord responsavel por orquestrar a jornada gamificada do projeto **python.game**.

Ele deve funcionar como o nucleo da plataforma:

- onboarding dos alunos
- liberacao de missoes
- recomendacao de conteudos
- validacao do formato de entrega
- registro de XP
- controle de cargos
- rankings
- portfolio interno

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
│  └─ cogs/
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

Crie uma `.env` na raiz do workspace ou dentro de `python.game/` com:

```text
DISCORD_CLIENT_ID=id_do_app
DISCORD_BOT_TOKEN=token_do_bot
DISCORD_GUILD_ID=id_do_servidor_de_teste
COMMAND_PREFIX=/
CONTENT_INDEX_PATH=conteudos/index-conteudos.json
```

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
