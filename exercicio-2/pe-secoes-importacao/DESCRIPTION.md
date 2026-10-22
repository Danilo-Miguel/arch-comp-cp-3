<h2 align="center">Seções e tabela de importação do PE</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo ausente ou fora do
> formato não conta como tentativa, mas resposta errada conta. Confira tudo
> antes de rodar o `check`.

Um PE é dividido em **seções**: código (`.text`), dados só leitura (`.rdata`),
dados graváveis (`.data`) etc. Como o programa usa funções do Windows, ele
também tem uma **tabela de importação**, que diz ao *loader* quais DLLs
carregar e quais funções de cada DLL o programa chama.

## 1. Investigue

```bash
objdump -h /challenge/programa.exe
objdump -x /challenge/programa.exe | less
```

- `objdump -h` lista as seções. Repare nas flags: a seção com `CODE` é a que
  contém instruções executáveis.
- Em `objdump -x`, procure o bloco **The Import Tables**: ele mostra o nome da
  DLL (`DLL Name`) e as funções importadas dela.

## 2. Responda

Crie o arquivo `/home/hacker/exercicio2.txt` com **4 linhas**:

```
quantidade de seções (em decimal)
nome da seção que contém o código executável (com o ponto)
nome da DLL importada (com .dll)
nome da função importada que encerra o processo
```

## 3. Confira

```bash
/challenge/check
```
