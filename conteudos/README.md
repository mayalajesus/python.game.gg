# Conteudos da Trilha python.game

Esta pasta guarda os arquivos JSON de cada conteudo da trilha.

A ideia e simples: o cronograma define a jornada, e estes JSONs guardam os links que o bot deve recomendar para cada etapa.

## Como preencher

Abra o JSON do conteudo desejado e adicione links nos campos:

- `recomendacoes.pdfs`
- `recomendacoes.videos`
- `recomendacoes.artigos`
- `recomendacoes.sites_oficiais`
- `recomendacoes.documentacao`
- `recomendacoes.cursos`
- `recomendacoes.repositorios`
- `recomendacoes.ferramentas`
- `recomendacoes.outros`

Exemplo:

```json
{
  "titulo": "Variaveis - Baus de Memoria",
  "recomendacoes": {
    "videos": [
      "https://exemplo.com/aula-variaveis"
    ],
    "documentacao": [
      "https://docs.python.org/3/tutorial/introduction.html"
    ]
  }
}
```

## Arquivos principais

- `index-conteudos.json`: lista todos os conteudos e seus arquivos.
- `schema-conteudo.json`: explica os campos esperados em cada JSON.
- Pastas `modulo-*`: contem os arquivos individuais de cada conteudo.

## Regra para o bot

Antes de liberar uma missao, o bot deve buscar o JSON daquele conteudo e mostrar as recomendacoes preenchidas.

Se algum campo estiver vazio, o bot pode simplesmente ignorar esse tipo de recurso.

Exemplo:

```text
Conteudo: Variaveis - Baus de Memoria

Videos recomendados:
- link 1
- link 2

Documentacao:
- link oficial
```

