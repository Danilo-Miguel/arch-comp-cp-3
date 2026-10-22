<h2 align="center">mov, leitura (read) e encerramento (exit) em x86 (32 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com resultado errado
> conta. **Teste o seu programa antes de rodar o `check`.**

Crie o arquivo `ascii32.asm` no seu diretório home, em **Assembly x86 (32 bits)**
com NASM, que:

1. Leia **1 caractere** do teclado com a syscall `read`;
2. Encerre o programa com a syscall `exit`, usando como **código de saída** o
   código ASCII do caractere lido.

Exemplo: digitando `A`, o programa deve sair com código `65`.

Lembrete das syscalls de 32 bits (`int 0x80`):

| syscall | `eax` | `ebx` | `ecx` | `edx` |
|---|---|---|---|---|
| `read` | `3` | `0` (teclado) | endereço do buffer | quantidade de bytes |
| `exit` | `1` | código de saída | | |

Dica: reserve 1 byte com `resb 1` na seção `.bss`. Para levar o byte lido para
o `ebx`, zere o `ebx` e depois use `mov bl, [buffer]`.

## Monte, ligue e teste

```bash
nasm -f elf32 ascii32.asm -o ascii32.o
ld -m elf_i386 ascii32.o -o ascii32
printf 'A' | ./ascii32
echo $?
```

O `echo $?` mostra o código de saída do último programa. Teste com outras
letras e números.

## Confira

```bash
/challenge/check
```

O `check` não monta nada por você. Ele confere se `ascii32.asm`, `ascii32.o` e
`ascii32` existem no seu home, se são ELF 32 bits e roda o programa com
caracteres **sorteados**, comparando o código de saída.
