<h2 align="center">cmp e saltos condicionais (x86, 32 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com resultado errado
> conta. **Teste o seu programa antes de rodar o `check`.**

Crie o arquivo `maior32.asm` no seu diretório home, em **Assembly x86 (32 bits)**
com NASM, que:

1. Leia **2 dígitos** do teclado com `read` (como no exercício anterior);
2. Compare os dois com `cmp`;
3. Encerre com `exit`, usando como código de saída o **maior** dos dois dígitos.

Exemplos: `27` sai com `7`; `72` sai com `7`; `55` sai com `5`.

Como funcionam os saltos:

- `cmp a, b` compara `a` com `b` (faz `a - b` sem guardar o resultado);
- `jge rotulo` salta se `a >= b`; `jl rotulo` salta se `a < b`;
- `jmp rotulo` salta sempre.

Um jeito de pensar: coloque o primeiro dígito em `ebx` e o segundo em `ecx`. Se
`ebx >= ecx`, o `ebx` já é o maior e você pula direto para o `exit`. Se não,
copie o `ecx` para o `ebx` antes de sair.

## Monte, ligue e teste

```bash
nasm -f elf32 maior32.asm -o maior32.o
ld -m elf_i386 maior32.o -o maior32
printf '27' | ./maior32 ; echo $?
printf '72' | ./maior32 ; echo $?
printf '55' | ./maior32 ; echo $?
```

## Confira

```bash
/challenge/check
```

O `check` testa os casos acima e mais pares **sorteados**.
