# CookBook

## Sobre

Um gerador de livros de receita em LaTeX automático. Escreva receitas simples em arquivos `.txt` e use o script para construir um belo `.pdf` baseado em LaTeX e compilando-as.

## Requerimentos

+ Python 2.7
+ LaTeX

### Instalando LaTeX no macOS

`brew cask install mactex`

`brew cask install texmaker`

### Executando o script

`python builder.py`

## Escrevendo Receitas

Toda receita é representada por um arquivo `.txt` e uma imagem (qualquer formato comum como `.png`, `.jpg` etc). É importante notar que TODA receita requer uma imagem. Imagens em formato paisagem são esteticamente melhores. Esses arquivos devem ser colocados na pasta `recipes` e devem seguir o seguinte padrão:

```
\nome:
Nome da Receita

\ds:
salgado

\serve:
4

\kcal:
300

\ingredientes:
igrediente 1
ingrediente 2
ingrediente 3

\dicas:
dica 1
dica 2
dica 3

\historia:
Toda a história deve estar escrita em uma linha.

\modo:
Passo 1
Passo 2
Passo 3

\index:
0
```

### Explicação dos campos

Campos em negrito são obrigatórios e não poderão ser omitidos das receitas.

+ __`\nome` Nome da Receita.__ 
+ `\ds`: Doce ou salgado. Ainda não é utilizado.
+ `\serve`: Quantas pessoas a receita serve (número inteiro).
+ `\kcal`: Calorias da receita (número inteiro).
+ __`\ingredientes`: Ingredientes necessários. Um por linha.__
+ `\dicas`: Dicas de preparo. Uma por linha.
+ `\historia`: História da receita. Deve estar escrita por inteiro em uma linha.
+ __`\modo`: Modo de Preparo. Um passo por linha.__
+ __`\index`: Índice da receita. Determina a ordem no livro.__
