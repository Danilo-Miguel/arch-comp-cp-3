<h2 align="center">Formato PE: cabeçalho DOS e assinatura PE</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo ausente ou fora do
> formato não conta como tentativa, mas resposta errada conta. Confira tudo
> antes de rodar o `check`.

O arquivo `/challenge/programa.exe` é um executável de **Windows** no formato
**PE (Portable Executable)**. Mesmo sem Windows, dá para inspecioná-lo no Linux.

Todo PE começa com um **cabeçalho DOS** de 64 bytes. Os 2 primeiros bytes são
a assinatura em ASCII, e o campo `e_lfanew`, no offset `0x3C`, guarda (em 4
bytes *little-endian*) o offset onde começa o **cabeçalho PE** (`PE\0\0`).

## 1. Investigue

```bash
file /challenge/programa.exe
objdump -f /challenge/programa.exe
od -A x -t x1z -N 128 /challenge/programa.exe
```

No `od`, a coluna da esquerda é o offset em hexadecimal e cada linha mostra 16
bytes. Ache o byte do offset `0x3C` e leia os 4 bytes a partir dele (o primeiro
é o menos significativo). Confirme que nesse offset aparece `PE`.

## 2. Responda

Crie o arquivo `/home/hacker/exercicio1.txt` com **4 linhas**:

```
assinatura do cabeçalho DOS (2 letras)
offset do cabeçalho PE (e_lfanew), em hexadecimal com 0x
formato: PE32 ou PE32+
arquitetura, como o objdump -f mostra
```

## 3. Confira

```bash
/challenge/check
```
