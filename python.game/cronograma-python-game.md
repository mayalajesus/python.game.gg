# python.game - Cronograma de Estudo e Recomendacao de Conteudos

## Visao Geral

O cronograma do **python.game** leva o aluno do zero em Python ate um nivel avancado com foco em Engenharia de Dados.

A jornada foi pensada para ser executada dentro do Discord, com o bot atuando como mentor, avaliador, registrador de progresso e recomendador de conteudos.

Formato base:

- Duracao estimada: 24 semanas
- Frequencia: 5 dias por semana
- Tempo diario sugerido: 30 a 60 minutos
- Metodo: aprender pouco, praticar todo dia, entregar missoes reais
- Resultado final: portfolio com projetos progressivos de Python e Engenharia de Dados

## Como o Bot Deve Recomendar Conteudos

Antes de cada desafio, o bot deve recomendar conteudos curtos e direcionados. O objetivo nao e despejar teoria, mas preparar o aluno para concluir a missao.

Os links recomendados devem ficar em arquivos JSON individuais dentro da pasta `conteudos/`.

Cada conteudo da trilha possui um arquivo proprio para que links sejam adicionados manualmente depois, sem precisar alterar o cronograma inteiro ou o codigo do bot.

No projeto inteiro, a unica edicao manual esperada e:

- preencher a `.env`
- adicionar links de estudo nos campos `recomendacoes.*`

Todos os demais campos dos JSONs fazem parte da trilha e devem ser tratados como configuracao do projeto, nao como conteudo manual.

Arquivos de apoio:

- `conteudos/index-conteudos.json`: indice com todos os conteudos da trilha
- `conteudos/schema-conteudo.json`: modelo dos campos esperados
- `conteudos/modulo-*/`: pastas com os JSONs individuais de cada conteudo

Cada conteudo da trilha deve ter:

- Explicacao curta do conceito
- Recomendacao de leitura
- Recomendacao de video ou aula
- Exemplo guiado
- Exercicio de aquecimento
- Missao pratica
- Criterios de validacao
- Conteudo de reforco, caso o aluno erre

### Modelo de recomendacao do bot

```text
🎒 Nova missao desbloqueada: O Cofre das Variaveis

Antes de iniciar, estude estes recursos:

📖 Leitura curta:
Variaveis, tipos basicos e boas praticas de nomes.

🎥 Aula recomendada:
Procure uma aula curta sobre "variaveis em Python para iniciantes".

🧪 Exemplo guiado:
Crie variaveis para nome, nivel, classe e XP do personagem.

⚔️ Missao:
Criar uma ficha de personagem usando variaveis e print().

✅ Para ser aprovado:
- Usar nomes de variaveis em snake_case
- Usar pelo menos 4 variaveis
- Exibir as informacoes no terminal
- Enviar no formato solicitado
```

### Regra obrigatoria de envio

O bot so deve corrigir exercicios enviados no modelo pedido.

Modelo padrao:

````text
/entregar desafio_id: fundamentos_01

Codigo:
```python
seu codigo aqui
```

Explicacao:
Explique em poucas linhas como sua solucao funciona.

Repositorio:
link do GitHub, quando solicitado.
````

Se o aluno enviar fora do formato:

````text
⚠️ Entrega fora do formato.

Eu ainda nao posso corrigir esta missao.

Envie novamente usando:

/entregar desafio_id: fundamentos_01

Codigo:
```python
seu codigo aqui
```

Explicacao:
Explique em poucas linhas como sua solucao funciona.
````

### Tipos de recomendacao por dificuldade

Quando o aluno errar, o bot deve identificar o tipo de erro e recomendar reforco especifico.

| Tipo de erro | Recomendacao do bot |
|---|---|
| Erro de sintaxe | Revisar escrita do Python, parenteses, aspas, indentacao e dois-pontos |
| Erro de logica | Rever o enunciado, criar exemplos de entrada e saida, testar passo a passo |
| Conceito incorreto | Reassistir conteudo principal e fazer exercicio de aquecimento |
| Codigo ilegivel | Revisar nomes de variaveis, organizacao e comentarios uteis |
| Entrega incompleta | Conferir checklist da missao antes de reenviar |
| Fora do formato | Reenviar no modelo padrao antes da correcao |

## Marcos da Jornada

| Marco | Rank | Foco | Competencia |
|---|---|---|---|
| 0% | 🥚 Novato | Onboarding | Entender a jornada e configurar perfil |
| 25% | ⚔️ Aventureiro | Fundamentos | Criar scripts simples e automatizacoes locais |
| 50% | 🔮 Mago das Funcoes | Python intermediario | Criar programas organizados, reutilizaveis e testaveis |
| 75% | 📊 Analista Arcano | Dados e SQL | Manipular, consultar e transformar dados |
| 100% | 👑 Mestre dos Dados | Engenharia de Dados | Construir pipelines, APIs, automacoes e projeto final |

---

# Cronograma Completo

## Semana 0 - Onboarding: Entrada na Guilda

Rank inicial: 🥚 Novato

Objetivo:
Preparar o aluno para a experiencia, explicar regras, formato de entrega, XP, cargos e portfolio.

Conteudos:

- Como funciona o python.game
- Como ganhar XP
- Como enviar exercicios
- Como pedir ajuda
- Como registrar projetos no portfolio
- Como usar GitHub durante a jornada

Missao principal:

**Juramento da Guilda**

O aluno deve concluir o onboarding, aceitar as regras, escolher um nome de aventureiro e receber o cargo inicial.

Recomendacao do bot:

- Ler o canal de boas-vindas
- Ler o canal como-funciona
- Fazer o comando `/iniciar`
- Fazer uma entrega teste no formato correto

Validacao:

- Confirmou onboarding
- Recebeu cargo 🥚 Novato
- Entendeu o formato de entrega
- Foi registrado no sistema de XP

---

## Modulo 1 - Recruta: O Despertar do Codigo

Duracao: Semanas 1 a 4

Foco:
Fundamentos de Python, terminal, variaveis, tipos, input, operadores e condicionais.

Cargo sugerido ao concluir:
⚔️ Aventureiro

### Semana 1 - Preparando o Equipamento

Conteudos:

- Terminal
- Criacao de pastas
- Instalacao do Python
- VS Code
- Primeiro script
- `print()`
- Comentarios
- Variaveis

Missoes:

- Base da Guilda: criar estrutura de pastas pelo terminal
- Teste da Lamina: configurar Python e VS Code
- Banner da Taverna: primeiro script com `print()`
- Grimorio de Regras: comentarios no codigo
- Inventario Inicial: variaveis de personagem

Recomendacoes do bot:

- Tutorial curto de terminal
- Documentacao inicial do Python
- Aula curta sobre VS Code para Python
- Conteudo sobre `print()`, comentarios e variaveis

Projeto da semana:

**Ficha Inicial do Aventureiro**

Criar um script que imprime nome, classe, nivel inicial, guilda e mensagem de entrada.

### Semana 2 - Manipulando o Mundo

Conteudos:

- `str`
- `int`
- `float`
- `type()`
- Operadores matematicos
- F-strings
- `input()`
- Conversao de tipos

Missoes:

- Status do Personagem
- Calculadora de Dano
- Ficha Formatada
- Terminal de Registro da Guilda
- Loja de Pocoes

Recomendacoes do bot:

- Tipos de dados em Python
- Operadores aritmeticos
- F-strings
- Entrada de dados com `input()`
- Conversao com `int()`, `float()` e `str()`

Projeto da semana:

**Loja da Guilda**

Criar um programa que recebe itens, quantidade, preco, calcula total e troco.

### Semana 3 - Acampamento de Revisao

Conteudos:

- Revisao de terminal
- Revisao de variaveis
- Revisao de tipos
- Revisao de input
- Revisao de F-strings

Missoes:

- Simulador de Loot
- Divisor de XP
- Ficha com multiplas linhas
- Recriacao de scripts sem consultar resposta
- Desafio de entrega no formato correto

Recomendacoes do bot:

- Conteudos de reforco personalizados conforme erros anteriores
- Lista de exercicios curtos
- Checklist de dominio minimo

Projeto da semana:

**Diario do Recruta**

Criar um pequeno programa que registra informacoes do aluno e gera uma mensagem formatada de progresso.

### Semana 4 - Os Caminhos da Escolha

Conteudos:

- Booleanos
- Operadores relacionais
- `and`
- `or`
- `not`
- `if`
- `else`
- `elif`

Missoes:

- Verificador de Nivel Minimo
- Requisitos de Quest
- Alerta de HP Baixo
- Cofre da Guilda
- Sistema de Ranks por XP

Recomendacoes do bot:

- Booleanos e comparacoes
- Logica condicional
- Indentacao em Python
- Exemplos de `if`, `elif` e `else`

Projeto do modulo:

**O Teste do Recruta**

Criar um simulador de arena onde o usuario cadastra um heroi, escolhe atributos e o programa decide vitoria, empate ou derrota com base em condicionais.

Validacao do modulo:

- Script roda sem erro
- Usa `input()`
- Usa casting
- Usa operadores
- Usa `if`, `elif` e `else`
- Entrega esta no formato correto

---

## Modulo 2 - Aventureiro: Repeticao, Listas e Inventarios

Duracao: Semanas 5 a 7

Foco:
Loops, listas, tuplas, dicionarios e manipulacao de colecoes.

Cargo sugerido ao concluir:
🛡️ Cacador de Bugs

### Semana 5 - Loops: A Roda das Missoes

Conteudos:

- `while`
- `for`
- `range()`
- `break`
- `continue`
- Contadores
- Acumuladores

Missoes:

- Contador de Treino Diario
- Simulador de Rodadas de Batalha
- Calculadora de XP acumulado
- Menu interativo da Guilda
- Lista de tarefas com repeticao

Recomendacoes do bot:

- Loops `while` e `for`
- Quando usar repeticao
- Como evitar loop infinito
- Exercicios de contadores e acumuladores

Projeto da semana:

**Treinador de XP**

Criar um programa que recebe varias missoes concluidas e calcula o XP total do dia.

### Semana 6 - Listas e Tuplas: Inventario Organizado

Conteudos:

- Listas
- Indices
- `append()`
- `remove()`
- `len()`
- Ordenacao simples
- Tuplas

Missoes:

- Inventario de Itens
- Lista de Membros da Guilda
- Controle de Missoes Pendentes
- Organizador de Loot
- Ranking local em lista

Recomendacoes do bot:

- Estruturas de dados basicas
- Listas em Python
- Iteracao em listas
- Diferenca entre lista e tupla

Projeto da semana:

**Inventario da Guilda**

Criar um programa que permite adicionar, listar e remover itens do inventario.

### Semana 7 - Dicionarios: O Registro dos Herois

Conteudos:

- Dicionarios
- Chave e valor
- Dicionarios aninhados
- Lista de dicionarios
- Busca de dados
- Atualizacao de dados

Missoes:

- Cadastro de Heroi
- Registro de XP por aluno
- Busca de membro por nome
- Atualizacao de nivel
- Mini ranking por dicionario

Recomendacoes do bot:

- Dicionarios em Python
- Como representar dados reais
- Lista de dicionarios
- Estruturas usadas em APIs e JSON

Projeto do modulo:

**Painel de Membros da Guilda**

Criar um programa em terminal que cadastra membros, registra XP e mostra ranking.

Validacao do modulo:

- Usa loops
- Usa listas
- Usa dicionarios
- Tem menu interativo
- Permite cadastrar, listar e consultar dados

---

## Modulo 3 - Mago das Funcoes: Codigo Reutilizavel

Duracao: Semanas 8 a 10

Foco:
Funcoes, organizacao, tratamento de erros, modulos e boas praticas.

Cargo sugerido ao concluir:
🔮 Mago das Funcoes

### Semana 8 - Funcoes: Feiticos Reutilizaveis

Conteudos:

- `def`
- Parametros
- Retorno
- Escopo
- Funcoes pequenas
- Reutilizacao

Missoes:

- Funcao de calcular XP
- Funcao de validar nivel
- Funcao de formatar ficha
- Funcao de gerar ranking
- Refatorar projeto antigo usando funcoes

Recomendacoes do bot:

- Funcoes em Python
- Diferenca entre `print` e `return`
- Como quebrar problemas grandes em partes pequenas

Projeto da semana:

**Biblioteca de Feiticos da Guilda**

Criar um arquivo com funcoes reutilizaveis para XP, ranking e validacao.

### Semana 9 - Erros, Excecoes e Depuracao

Conteudos:

- Erros comuns
- `try`
- `except`
- `else`
- `finally`
- Validacao de entrada
- Debugging basico

Missoes:

- Corrigir scripts quebrados
- Validar input numerico
- Tratar divisao por zero
- Criar mensagens de erro amigaveis
- Refazer loja da guilda com tratamento de erro

Recomendacoes do bot:

- Erros mais comuns em Python
- Como ler traceback
- Tratamento de excecoes
- Debugging no VS Code

Projeto da semana:

**Cacador de Bugs**

Corrigir uma colecao de scripts com erros e documentar o que foi ajustado.

### Semana 10 - Modulos, Pacotes e Git

Conteudos:

- `import`
- Modulos proprios
- Organizacao de arquivos
- Ambiente virtual
- `pip`
- Git basico
- GitHub basico

Missoes:

- Separar projeto em arquivos
- Criar ambiente virtual
- Instalar pacote externo
- Criar primeiro repositorio
- Fazer primeiro commit

Recomendacoes do bot:

- Modulos em Python
- Ambientes virtuais
- Git e GitHub para iniciantes
- Como organizar um projeto Python

Projeto do modulo:

**Sistema Modular da Guilda**

Transformar o painel de membros em um projeto organizado com arquivos separados, ambiente virtual e repositorio no GitHub.

Validacao do modulo:

- Usa funcoes
- Tem tratamento de erro
- Codigo separado em modulos
- Projeto esta no GitHub
- README explica como rodar

---

## Modulo 4 - Guardiao dos Dados: Arquivos, APIs e Automacao

Duracao: Semanas 11 a 13

Foco:
Manipular arquivos, CSV, JSON, APIs, automacoes e web scraping basico.

Cargo sugerido ao concluir:
📚 Guardiao dos Dados

### Semana 11 - Arquivos: Pergaminhos da Guilda

Conteudos:

- Leitura de arquivos
- Escrita de arquivos
- `with open`
- Caminhos
- CSV
- JSON

Missoes:

- Ler arquivo de missoes
- Salvar historico de XP
- Gerar relatorio em `.txt`
- Ler CSV de alunos
- Criar JSON de perfil

Recomendacoes do bot:

- Manipulacao de arquivos em Python
- CSV com biblioteca padrao
- JSON em Python
- Cuidados com caminhos de arquivos

Projeto da semana:

**Registro Permanente da Guilda**

Criar um programa que salva alunos, XP e missoes em arquivos CSV ou JSON.

### Semana 12 - APIs: Portais Externos

Conteudos:

- HTTP
- Request e response
- Status code
- `requests`
- JSON de API
- Parametros

Missoes:

- Consumir API publica
- Ler status code
- Extrair campos de JSON
- Salvar resposta em arquivo
- Criar relatorio simples da API

Recomendacoes do bot:

- O que e uma API
- Como funciona HTTP
- Biblioteca `requests`
- JSON vindo de APIs

Projeto da semana:

**Invocador de APIs**

Consumir uma API publica, extrair dados relevantes e salvar um relatorio local.

### Semana 13 - Automacao e Web Scraping Basico

Conteudos:

- Automacao de tarefas
- Requisicoes em paginas simples
- HTML basico
- BeautifulSoup
- Cuidados eticos
- Agendamento local

Missoes:

- Automatizar organizacao de arquivos
- Baixar dados de uma URL
- Extrair titulos de uma pagina
- Gerar relatorio automatico
- Documentar limites eticos do scraping

Recomendacoes do bot:

- Automacao com Python
- HTML basico para scraping
- BeautifulSoup
- Boas praticas e limites de scraping

Projeto do modulo:

**Coletor de Dados da Guilda**

Criar um coletor que busca dados externos, salva em JSON/CSV e gera um resumo no terminal.

Validacao do modulo:

- Le arquivos
- Escreve arquivos
- Consome API
- Trata erros de requisicao
- Salva dados estruturados
- README inclui fonte dos dados

---

## Modulo 5 - Arquiteto de Classes: Python Intermediario e Qualidade

Duracao: Semanas 14 a 16

Foco:
Orientacao a Objetos, testes, qualidade, logging e padroes de projeto simples.

Cargo sugerido ao concluir:
🏰 Arquiteto de Classes

### Semana 14 - Orientacao a Objetos

Conteudos:

- Classe
- Objeto
- Atributos
- Metodos
- `__init__`
- Encapsulamento simples

Missoes:

- Classe Heroi
- Classe Missao
- Classe Aluno
- Classe Ranking
- Refatorar cadastro usando objetos

Recomendacoes do bot:

- Orientacao a Objetos em Python
- Classes e objetos
- Quando usar OOP
- Exemplos de modelagem simples

Projeto da semana:

**Sistema de Personagens da Guilda**

Criar classes para aluno, missao, conquista e ranking.

### Semana 15 - Testes e Qualidade

Conteudos:

- Testes automatizados
- `pytest`
- Funcoes testaveis
- Casos de teste
- Organizacao
- README melhorado

Missoes:

- Testar funcao de XP
- Testar validacao de rank
- Testar cadastro
- Testar erros esperados
- Criar checklist de qualidade

Recomendacoes do bot:

- Introducao a testes com `pytest`
- Como escrever funcoes testaveis
- Boas praticas de README
- Como revisar o proprio codigo

Projeto da semana:

**Arena de Testes**

Adicionar testes automatizados ao sistema da guilda.

### Semana 16 - Python Avancado Essencial

Conteudos:

- List comprehension
- Dictionary comprehension
- `lambda`
- `map`
- `filter`
- `sorted`
- `datetime`
- `logging`
- Type hints

Missoes:

- Melhorar rankings com `sorted`
- Usar comprehensions para filtrar dados
- Criar logs de execucao
- Adicionar type hints
- Trabalhar com datas de missoes

Recomendacoes do bot:

- Python intermediario e avancado pratico
- Comprehensions
- Logging
- Type hints
- Datas em Python

Projeto do modulo:

**Core do Bot em Python**

Criar uma simulacao local do sistema do bot: registrar aluno, registrar XP, subir nivel, gerar ranking e salvar logs.

Validacao do modulo:

- Usa classes
- Usa testes
- Usa logging
- Usa type hints
- Tem README e estrutura clara

---

## Modulo 6 - Analista Arcano: Dados, SQL e Pandas

Duracao: Semanas 17 a 19

Foco:
SQL, bancos relacionais, Pandas, limpeza de dados e analise.

Cargo sugerido ao concluir:
📊 Analista Arcano

### Semana 17 - SQL e Bancos de Dados

Conteudos:

- O que e banco de dados
- Tabelas
- Linhas e colunas
- `SELECT`
- `WHERE`
- `ORDER BY`
- `GROUP BY`
- `JOIN`
- SQLite

Missoes:

- Criar banco local SQLite
- Criar tabela de alunos
- Inserir dados
- Consultar ranking
- Fazer consultas com filtros e agrupamentos

Recomendacoes do bot:

- SQL para iniciantes
- SQLite com Python
- Consultas basicas
- Relacionamento entre tabelas

Projeto da semana:

**Banco da Guilda**

Criar um banco SQLite para armazenar alunos, missoes, XP e conquistas.

### Semana 18 - Pandas: Manipulando Dados

Conteudos:

- DataFrame
- Series
- Leitura de CSV
- Filtros
- Colunas
- Agregacoes
- Tratamento de valores nulos

Missoes:

- Ler CSV de alunos
- Filtrar alunos por XP
- Calcular media de XP
- Encontrar top 10
- Limpar dados faltantes

Recomendacoes do bot:

- Pandas para iniciantes
- DataFrames
- Limpeza de dados
- Agregacoes

Projeto da semana:

**Relatorio dos Aventureiros**

Gerar relatorio com Pandas mostrando ranking, progresso medio, alunos ativos e missoes concluidas.

### Semana 19 - Visualizacao e Analise

Conteudos:

- Matplotlib
- Seaborn
- Graficos simples
- Indicadores
- Analise exploratoria
- Storytelling com dados

Missoes:

- Grafico de XP por aluno
- Grafico de progresso por semana
- Analise de missoes mais dificeis
- Relatorio com insights
- Exportar resultado

Recomendacoes do bot:

- Visualizacao de dados com Python
- Matplotlib basico
- Seaborn basico
- Como contar uma historia com dados

Projeto do modulo:

**Dashboard Offline da Guilda**

Criar um notebook ou script que analisa dados da comunidade e gera graficos de progresso.

Validacao do modulo:

- Usa SQL
- Usa Pandas
- Gera graficos
- Apresenta insights
- Salva relatorio ou notebook

---

## Modulo 7 - Engenheiro da Guilda: ETL, Pipelines e Infraestrutura

Duracao: Semanas 20 a 22

Foco:
Engenharia de Dados aplicada, pipelines, ETL, boas praticas, Docker e orquestracao introdutoria.

Cargo sugerido ao concluir:
⚙️ Engenheiro da Guilda

### Semana 20 - ETL e Pipelines

Conteudos:

- Extract, Transform, Load
- Pipeline de dados
- Dados brutos e dados tratados
- Validacao de dados
- Idempotencia
- Logs

Missoes:

- Extrair dados de API
- Transformar dados com Pandas
- Salvar dados tratados
- Criar logs do pipeline
- Reexecutar pipeline sem duplicar dados

Recomendacoes do bot:

- Conceitos de ETL
- Pipeline de dados com Python
- Logs em processos de dados
- Validacao de dados

Projeto da semana:

**Pipeline de XP da Guilda**

Criar um pipeline que extrai dados de alunos, transforma, calcula rankings e salva a versao tratada.

### Semana 21 - Banco, Modelagem e Carga

Conteudos:

- Modelagem simples
- Chaves primarias
- Chaves estrangeiras
- Normalizacao basica
- Carga em banco
- SQLAlchemy ou sqlite3

Missoes:

- Modelar tabelas da guilda
- Criar schema SQL
- Carregar dados tratados
- Consultar indicadores
- Validar integridade

Recomendacoes do bot:

- Modelagem de dados
- SQL aplicado a projetos
- Carga de dados com Python
- Boas praticas de schema

Projeto da semana:

**Data Mart da Guilda**

Criar tabelas para alunos, missoes, entregas, XP e conquistas, carregando dados via Python.

### Semana 22 - Docker, CLI e Orquestracao Intro

Conteudos:

- Variaveis de ambiente
- Arquivo `.env`
- CLI com argumentos
- Docker basico
- Agendamento
- Airflow, Prefect ou Dagster como visao geral

Missoes:

- Criar script executavel por CLI
- Separar configuracoes em `.env`
- Criar Dockerfile simples
- Simular agendamento do pipeline
- Documentar execucao

Recomendacoes do bot:

- Variaveis de ambiente
- Docker para iniciantes
- CLI em Python
- Conceito de orquestracao de pipelines

Projeto do modulo:

**Pipeline Executavel da Guilda**

Empacotar o pipeline para rodar por comando, com configuracao, logs, banco e documentacao.

Validacao do modulo:

- Pipeline executa de ponta a ponta
- Tem logs
- Usa banco
- Tem configuracao separada
- README ensina a rodar
- Dados nao duplicam em reexecucao

---

## Modulo 8 - Mestre dos Dados: Python Avancado e Projeto Final

Duracao: Semanas 23 a 24

Foco:
Consolidar Python avancado e Engenharia de Dados em um projeto final de portfolio.

Cargo sugerido ao concluir:
👑 Mestre dos Dados

### Semana 23 - Python Avancado para Engenharia de Dados

Conteudos:

- Decorators
- Generators
- Context managers
- Dataclasses
- Pydantic ou validacao de dados
- Async intro
- Boas praticas de arquitetura
- Performance basica

Missoes:

- Criar decorator de log
- Criar generator para ler dados em lotes
- Criar context manager para recursos
- Validar dados com modelos
- Refatorar pipeline com boas praticas

Recomendacoes do bot:

- Decorators em Python
- Generators para processamento eficiente
- Context managers
- Dataclasses e validacao
- Arquitetura simples para projetos de dados

Projeto da semana:

**Motor Avancado de Pipeline**

Melhorar o pipeline existente usando validacao, logs, processamento em lotes e organizacao profissional.

### Semana 24 - Projeto Final: Guild Analytics Platform

Conteudos:

- Projeto de ponta a ponta
- Extracao
- Transformacao
- Carga
- Analise
- API ou dashboard simples
- Documentacao de portfolio
- Apresentacao do projeto

Missao final:

**Guild Analytics Platform**

Construir uma plataforma de dados da guilda que:

- Coleta dados de alunos, XP, missoes e entregas
- Salva dados brutos
- Transforma dados
- Carrega dados em banco
- Gera rankings
- Produz indicadores
- Exporta relatorios
- Possui README profissional
- Possui arquitetura explicada
- Possui prints ou graficos no portfolio

Recomendacoes do bot:

- Como estruturar projeto final
- Como escrever README profissional
- Como explicar arquitetura de dados
- Como apresentar projeto no GitHub
- Como preparar portfolio para LinkedIn

Validacao final:

- Projeto roda do inicio ao fim
- Tem repositorio publico ou privado organizado
- Tem README completo
- Tem dados de exemplo
- Tem scripts claros
- Tem logs
- Tem testes essenciais
- Tem analise ou dashboard
- Tem explicacao do problema, solucao e arquitetura

Recompensa:

- Cargo 👑 Mestre dos Dados
- Badge Projeto Final Concluido
- Destaque no ranking de projetos
- Registro no portfolio interno

---

# Matriz de Conteudos Recomendados pelo Bot

Esta matriz ajuda a transformar cada tema da trilha em recomendacoes automaticas.

| Tema | Antes da missao o bot recomenda | Se errar, o bot recomenda |
|---|---|---|
| Terminal | Comandos basicos, navegacao, criacao de pastas | Repetir missao guiada de `cd`, `dir`/`ls`, `mkdir` |
| Python setup | Instalacao, PATH, VS Code | Verificar versao do Python e extensao do VS Code |
| Print e comentarios | Sintaxe basica e documentacao | Revisar aspas, parenteses e comentarios com `#` |
| Variaveis | Nomeacao, atribuicao, snake_case | Refazer ficha com nomes claros |
| Tipos | `str`, `int`, `float`, `bool` | Usar `type()` para investigar variaveis |
| Input e casting | Entrada de dados e conversao | Revisar que `input()` sempre retorna texto |
| Condicionais | Comparacoes, `if`, `elif`, `else` | Testar entradas diferentes e revisar indentacao |
| Loops | `for`, `while`, contadores | Identificar condicao de parada |
| Listas | Indices, adicionar, remover, iterar | Criar inventario simples antes da missao |
| Dicionarios | Chave/valor, dados estruturados | Montar cadastro de um unico aluno antes de varios |
| Funcoes | Parametros, retorno, escopo | Diferenciar `return` de `print` |
| Erros | `try/except`, traceback | Ler a mensagem de erro linha por linha |
| Modulos | `import`, arquivos separados | Reorganizar projeto minimo com dois arquivos |
| Git | Commit, repositorio, README | Refazer fluxo: init, add, commit, push |
| Arquivos | `open`, CSV, JSON | Validar caminho e formato do arquivo |
| APIs | HTTP, JSON, status code | Imprimir resposta antes de transformar |
| OOP | Classes, objetos, metodos | Modelar uma classe simples antes do sistema completo |
| Testes | `pytest`, casos de teste | Testar uma funcao pequena e previsivel |
| SQL | SELECT, WHERE, JOIN | Fazer consultas pequenas no SQLite |
| Pandas | DataFrame, filtros, agregacoes | Inspecionar `head()`, `info()` e `describe()` |
| Visualizacao | Graficos e insights | Comecar com grafico de barras simples |
| ETL | Extrair, transformar, carregar | Separar pipeline em tres funcoes |
| Docker | Dockerfile e execucao | Rodar localmente antes de containerizar |
| Orquestracao | Agendamento e dependencia de tarefas | Desenhar fluxo do pipeline antes do codigo |
| Python avancado | Decorators, generators, dataclasses | Aplicar um conceito por vez em exemplo pequeno |
| Projeto final | Arquitetura, README, portfolio | Revisar checklist final e corrigir lacunas |

---

# XP Sugerido por Tipo de Entrega

| Atividade | XP |
|---|---:|
| Leitura marcada como concluida | 10 |
| Aula ou conteudo recomendado concluido | 10 |
| Exercicio de aquecimento | 30 |
| Missao diaria | 100 |
| Projeto semanal | 300 |
| Projeto de modulo | 600 |
| Ajudar outro membro | 20 |
| Compartilhar projeto | 50 |
| Corrigir entrega apos feedback | 40 |
| Projeto final aprovado | 1500 |

---

# Portfolio Progressivo

Ao final da jornada, o aluno deve ter pelo menos estes projetos:

1. Ficha Inicial do Aventureiro
2. Loja da Guilda
3. Teste do Recruta
4. Painel de Membros da Guilda
5. Sistema Modular da Guilda
6. Coletor de Dados da Guilda
7. Sistema de Personagens da Guilda
8. Core do Bot em Python
9. Banco da Guilda
10. Dashboard Offline da Guilda
11. Pipeline de XP da Guilda
12. Data Mart da Guilda
13. Pipeline Executavel da Guilda
14. Motor Avancado de Pipeline
15. Guild Analytics Platform

Esses projetos formam uma narrativa de portfolio: o aluno nao apenas estudou Python, ele construiu uma plataforma de dados progressivamente.

---

# Comportamento Esperado do Bot na Trilha

O bot deve agir como mentor de guilda.

Funcoes durante o cronograma:

- Liberar conteudos por semana
- Recomendar estudo antes de cada missao
- Explicar o objetivo da missao
- Mostrar criterio de aprovacao
- Validar formato da entrega
- Executar testes automaticos quando possivel
- Usar avaliador inteligente para analisar legibilidade, organizacao e uso dos conceitos
- Dar feedback objetivo
- Recomendar reforco personalizado
- Registrar XP
- Atualizar nivel
- Atribuir cargos
- Registrar projetos no portfolio interno
- Atualizar ranking

### Fluxo de uma missao

```text
1. Bot libera conteudo
2. Bot recomenda materiais
3. Aluno estuda
4. Bot libera desafio
5. Aluno envia no formato correto
6. Bot valida formato
7. Bot executa testes
8. Avaliador inteligente analisa qualidade
9. Bot retorna feedback
10. Bot registra XP ou pede ajuste
```

### Exemplo de feedback aprovado

```text
✅ Missao aprovada: Loja da Guilda

XP recebido: +100

Pontos fortes:
- Voce usou conversao de tipos corretamente
- O calculo do troco esta correto
- A mensagem final ficou clara

Melhoria recomendada:
- Use nomes de variaveis mais especificos, como quantidade_pocoes em vez de qtd

Proxima missao desbloqueada:
⚔️ Sistema de Ranks por XP
```

### Exemplo de feedback com correcao necessaria

```text
🛠️ Missao ainda nao aprovada

Motivo:
O programa quebra quando o usuario digita um numero decimal.

Reforco recomendado:
Revise conversao de tipos com `float()` e refaca o exercicio de aquecimento "Loja de Pocoes".

Reenvie no mesmo formato quando corrigir.
```

---

# Resultado Final da Jornada

Ao concluir o cronograma, o aluno deve ser capaz de:

- Programar em Python com autonomia
- Criar scripts interativos
- Organizar projetos em arquivos e modulos
- Usar Git e GitHub
- Consumir APIs
- Manipular arquivos CSV e JSON
- Trabalhar com SQL
- Analisar dados com Pandas
- Criar graficos e relatorios
- Construir pipelines ETL
- Usar logs, testes e boas praticas
- Entender Docker e orquestracao em nivel introdutorio
- Criar um projeto final de Engenharia de Dados
- Apresentar um portfolio profissional

Rank final:

👑 **Mestre dos Dados**
