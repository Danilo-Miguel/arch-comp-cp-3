<h2 align="center">add e sub com dígitos lidos do teclado (x86, 32 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com resultado errado
> conta. **Teste o seu programa antes de rodar o `check`.**

Crie o arquivo `soma32.asm` no seu diretório home, em **Assembly x86 (32 bits)**
com NASM, que:

1. Leia **2 caracteres** do teclado com `read`, cada um sendo um dígito de `0` a `9`;
2. Some os dois **dígitos** (não os códigos ASCII!);
3. Encerre com `exit`, usando a soma como código de saída.

Exemplo: digitando `37`, o programa deve sair com código `10`.

O caractere `'3'` vale `51` na tabela ASCII, e `'0'` vale `48`. Para
transformar o caractere no número, **subtraia 48** (`sub`). Depois some os
dois com `add`.

| syscall | `eax` | `ebx` | `ecx` | `edx` |
|---|---|---|---|---|
| `read` | `3` | `0` (teclado) | endereço do buffer | quantidade de bytes |
| `exit` | `1` | código de saída | | |

Dica: com `resb 2` você guarda os dois caracteres; o segundo fica em
`[buffer + 1]`.

## Monte, ligue e teste

```bash
nasm -f elf32 soma32.asm -o soma32.o
ld -m elf_i386 soma32.o -o soma32
printf '37' | ./soma32
echo $?
```

Teste também `00` e `99`.

## Confira

```bash
/challenge/check
```

O `check` roda o seu programa com pares de dígitos **sorteados** e compara o
código de saída.
