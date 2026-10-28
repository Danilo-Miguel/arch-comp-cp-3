<h2 align="center">Funções print_nome, print_idade e print_curso (x86, 32 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com saída errada
> conta. **Teste o seu programa antes de rodar o `check`.**

Uma **função** em Assembly é só um rótulo que termina com `ret`:

- `call rotulo` guarda o endereço de retorno na pilha e salta para a função;
- `ret` tira esse endereço da pilha e volta para a instrução depois do `call`.

Crie o arquivo `funcoes32.asm` no seu diretório home, em **Assembly x86
(32 bits)** com NASM, com **três funções**, cada uma escrevendo uma linha com
os **seus** dados:

| função | escreve |
|---|---|
| `print_nome` | `Nome: <seu nome>` |
| `print_idade` | `Idade: <sua idade>` (só números) |
| `print_curso` | `Curso: <seu curso>` |

O `_start` só chama as três funções, nessa ordem, e encerra com `exit(0)`:

```nasm
section .data
    nome db "Nome: Ana Souza", 10
    tam_nome equ $ - nome
    ; ... idade e curso do mesmo jeito ...

section .text
    global _start

_start:
    call print_nome
    call print_idade
    call print_curso
    ; exit(0)

print_nome:
    ; write(1, nome, tam_nome)
    ret

; ... print_idade e print_curso ...
```

O `exit` precisa vir **antes** das funções: sem ele, o processador continua
executando para baixo, entra no `print_nome` de novo e o `ret` final derruba
o programa (*segmentation fault*).

| syscall | `eax` | `ebx` | `ecx` | `edx` |
|---|---|---|---|---|
| `write` | `4` | `1` (tela) | endereço do texto | quantidade de bytes |
| `exit` | `1` | código de saída | | |

**Sem acentos** (`Ciencia da Computacao`).

## Monte, ligue e teste

```bash
nasm -f elf32 funcoes32.asm -o funcoes32.o
ld -m elf_i386 funcoes32.o -o funcoes32
./funcoes32
echo $?
```

## Confira

```bash
/challenge/check
```

O `check` confere no seu `.asm` se existem os rótulos `print_nome`,
`print_idade` e `print_curso`, se cada um é chamado com `call` e se há um
`ret` por função. Depois roda o programa e exige exatamente 3 linhas, nesta
ordem: `Nome: ...`, `Idade: <número>`, `Curso: ...`.
