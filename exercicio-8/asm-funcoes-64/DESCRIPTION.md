<h2 align="center">Funções print_nome, print_idade e print_curso (x86-64, 64 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com saída errada
> conta. **Teste o seu programa antes de rodar o `check`.**

Mesmo programa do exercício anterior, agora em **64 bits**: crie o arquivo
`funcoes64.asm` no seu diretório home, em **Assembly x86-64** com NASM, com as
funções `print_nome`, `print_idade` e `print_curso`, chamadas no `_start` com
`call`, nessa ordem, e encerrando com `exit(0)`.

A saída, com os **seus** dados:

```
Nome: Ana Souza
Idade: 20
Curso: Ciencia da Computacao
```

O `call` e o `ret` funcionam igual em 64 bits (o endereço de retorno guardado
na pilha só passa a ter 8 bytes). O que muda são as syscalls:

| syscall | `rax` | `rdi` | `rsi` | `rdx` |
|---|---|---|---|---|
| `write` | `1` | `1` (tela) | endereço do texto | quantidade de bytes |
| `exit` | `60` | código de saída | | |

e no lugar de `int 0x80` se usa **`syscall`**.

**Sem acentos.**

## Crie o arquivo

Escreva o código com um editor de texto. Sugestão: o **nano**.

```bash
cd ~
nano funcoes64.asm
```

Para salvar: `Ctrl+O` e depois `Enter`. Para sair: `Ctrl+X`. Para continuar
editando depois, é só rodar `nano funcoes64.asm` de novo.

## Monte, ligue e teste

```bash
nasm -f elf64 funcoes64.asm -o funcoes64.o
ld funcoes64.o -o funcoes64
./funcoes64
echo $?
```

## Confira

```bash
/challenge/check
```

O `check` confere se o objeto e o executável são ELF **64 bits**, se o código
usa `syscall`, se as três funções existem, são chamadas com `call` e terminam
com `ret`, e exige exatamente 3 linhas na saída: `Nome: ...`,
`Idade: <número>`, `Curso: ...`.
