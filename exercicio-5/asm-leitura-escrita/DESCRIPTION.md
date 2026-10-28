<h2 align="center">Ciclo de leitura e escrita (x86, 32 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com saída errada
> conta. **Teste o seu programa antes de rodar o `check`.**

Crie o arquivo `nome32.asm` no seu diretório home, em **Assembly x86 (32 bits)**
com NASM, que faça o ciclo **escrita → leitura → escrita**:

1. Escreva `Qual o seu nome? ` (com um espaço no final e **sem** quebra de linha);
2. Leia o nome do usuário com `read`, num buffer de **32 bytes**;
3. Escreva `Ola, ` seguido do nome que foi digitado;
4. Encerre com `exit(0)`.

No terminal fica assim (o `Ana` foi digitado pelo usuário):

```
Qual o seu nome? Ana
Ola, Ana
```

| syscall | `eax` | `ebx` | `ecx` | `edx` |
|---|---|---|---|---|
| `read` | `3` | `0` (teclado) | endereço do buffer | tamanho máximo |
| `write` | `4` | `1` (tela) | endereço do texto | quantidade de bytes |
| `exit` | `1` | código de saída | | |

## O pulo do gato: quantos bytes foram lidos?

Depois do `int 0x80`, o `read` devolve em **`eax` a quantidade de bytes que
leu**, já contando o Enter (`\n`). Digitando `Ana`, o `eax` volta com `4`.

Use esse valor como tamanho no `write` do nome. Se escrever os 32 bytes do
buffer, vão junto bytes zerados e a saída fica errada. Como o `eax` será
usado nas próximas syscalls, **guarde o tamanho** antes em outro registrador
(por exemplo `esi`):

```nasm
section .bss
    nome resb 32

    ; ... depois do read:
    int 0x80
    mov esi, eax        ; esi = quantidade de bytes lidos
```

**Sem acentos**: escreva `Ola`, não `Olá`.

## Crie o arquivo

Escreva o código com um editor de texto. Sugestão: o **nano**.

```bash
cd ~
nano nome32.asm
```

Para salvar: `Ctrl+O` e depois `Enter`. Para sair: `Ctrl+X`. Para continuar
editando depois, é só rodar `nano nome32.asm` de novo.

## Monte, ligue e teste

```bash
nasm -f elf32 nome32.asm -o nome32.o
ld -m elf_i386 nome32.o -o nome32
./nome32
echo $?
```

## Confira

```bash
/challenge/check
```

O `check` roda o programa com nomes **sorteados** (até 24 letras, podendo ter
espaço, como `Maria Clara`) e compara a saída caractere por caractere. O
programa precisa terminar com `exit(0)`.
