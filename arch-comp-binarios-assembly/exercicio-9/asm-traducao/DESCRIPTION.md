<h2 align="center">Sintaxe Intel vs AT&T (x86, 32 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com resultado errado
> conta. **Teste o seu programa antes de rodar o `check`.**

O mesmo código de máquina pode ser escrito em duas sintaxes:

| | Intel (NASM) | AT&T (GAS) |
|---|---|---|
| ordem dos operandos | `mov destino, origem` | `movl origem, destino` |
| registradores | `eax` | `%eax` |
| valores imediatos | `3` | `$3` |
| endereço de um rótulo | `buffer` | `$buffer` |
| conteúdo da memória | `[buffer]` | `buffer` |
| tamanho | pelo registrador | sufixo: `b` = byte, `l` = 32 bits |

O programa abaixo está em **AT&T**:

```gas
.section .bss
    .lcomm buffer, 1

.section .text
.global _start
_start:
    movl $3, %eax
    movl $0, %ebx
    movl $buffer, %ecx
    movl $1, %edx
    int $0x80

    movl $0, %ebx
    movb buffer, %bl
    subl $48, %ebx
    addl %ebx, %ebx
    addl $10, %ebx

    movl $1, %eax
    int $0x80
```

Traduza-o para a **sintaxe Intel do NASM** num arquivo `traducao32.asm` no seu
diretório home. (`.lcomm buffer, 1` vira `buffer resb 1` na seção `.bss`.)

Antes de testar, tente responder: digitando `3`, qual será o código de saída?

## Monte, ligue e teste

```bash
nasm -f elf32 traducao32.asm -o traducao32.o
ld -m elf_i386 traducao32.o -o traducao32
printf '3' | ./traducao32
echo $?
```

## Confira

```bash
/challenge/check
```

O `check` exige que o objeto seja gerado pelo NASM a partir de `traducao32.asm`
(montar o código AT&T com o `as` não vale) e roda o programa com dígitos
**sorteados**.
