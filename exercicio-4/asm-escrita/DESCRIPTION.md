<h2 align="center">Escrita na tela com write (x86, 32 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com saída errada
> conta. **Teste o seu programa antes de rodar o `check`.**

Crie o arquivo `ola32.asm` no seu diretório home, em **Assembly x86 (32 bits)**
com NASM, que:

1. Escreva na tela, com a syscall `write`, exatamente estas duas linhas:

   ```
   Ola, FIAP!
   Estou aprendendo Assembly x86.
   ```

2. Encerre com `exit(0)`.

Syscalls de 32 bits (`int 0x80`):

| syscall | `eax` | `ebx` | `ecx` | `edx` |
|---|---|---|---|---|
| `write` | `4` | `1` (tela) | endereço do texto | quantidade de bytes |
| `exit` | `1` | código de saída | | |

Na seção `.data`, o `10` é a quebra de linha (`\n`) e o `equ $ - mensagem`
calcula sozinho o tamanho do texto:

```nasm
section .data
    mensagem db "Ola, FIAP!", 10, "Estou aprendendo Assembly x86.", 10
    tam_mensagem equ $ - mensagem
```

**Sem acentos**: escreva `Ola`, não `Olá`.

## Crie o arquivo

Escreva o código com um editor de texto. Sugestão: o **nano**.

```bash
cd ~
nano ola32.asm
```

Para salvar: `Ctrl+O` e depois `Enter`. Para sair: `Ctrl+X`. Para continuar
editando depois, é só rodar `nano ola32.asm` de novo.

## Monte, ligue e teste

```bash
nasm -f elf32 ola32.asm -o ola32.o
ld -m elf_i386 ola32.o -o ola32
./ola32
echo $?
```

O `echo $?` mostra o código de saída: tem que ser `0`.

## Confira

```bash
/challenge/check
```

O `check` não monta nada por você. Ele confere se `ola32.asm`, `ola32.o` e
`ola32` existem no seu home, se são ELF 32 bits, roda o programa e compara a
saída **caractere por caractere** (inclusive as quebras de linha).
