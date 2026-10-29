<h2 align="center">Ficha do aluno com funções de leitura e escrita (x86-64, 64 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com saída errada
> conta. **Teste o seu programa antes de rodar o `check`.**

A ficha completa, em **64 bits**. Crie o arquivo `ficha64.asm` no seu diretório
home, em **Assembly x86-64** com NASM, com **seis funções**:

| função | o que faz |
|---|---|
| `ler_nome` | escreve `Digite seu nome: ` e lê o nome |
| `ler_idade` | escreve `Digite sua idade: ` e lê a idade |
| `ler_curso` | escreve `Digite seu curso: ` e lê o curso |
| `print_nome` | escreve `Nome: ` seguido do nome lido |
| `print_idade` | escreve `Idade: ` seguida da idade lida |
| `print_curso` | escreve `Curso: ` seguido do curso lido |

O `_start` chama as três `ler_...` e depois as três `print_...`, nessa ordem,
e encerra com `exit(0)`.

No terminal fica assim (`Ana`, `20` e `ADS` foram digitados):

```
Digite seu nome: Ana
Digite sua idade: 20
Digite seu curso: ADS
Nome: Ana
Idade: 20
Curso: ADS
```

A idade é lida e escrita **como texto**, igual ao nome: não precisa converter
para número.

Como no exercício anterior, guarde cada tamanho lido numa variável da `.bss`.
Em 64 bits o `rax` tem 8 bytes, então reserve com `resq 1`.

Coloque também **`default rel` na primeira linha** do arquivo. Em 64 bits, o
acesso a variáveis com colchetes (`[tam_nome]`) deve ser relativo ao `rip`; sem
essa linha o NASM mostra o aviso `implicit DEFAULT ABS is deprecated`.

```nasm
default rel

section .bss
    nome resb 32
    tam_nome resq 1

    ; dentro de ler_nome, depois do read:
    mov [tam_nome], rax

    ; dentro de print_nome:
    mov rdx, [tam_nome]
```

| syscall | `rax` | `rdi` | `rsi` | `rdx` |
|---|---|---|---|---|
| `read` | `0` | `0` (teclado) | endereço do buffer | tamanho máximo |
| `write` | `1` | `1` (tela) | endereço do texto | quantidade de bytes |
| `exit` | `60` | código de saída | | |

Instrução: **`syscall`** (não `int 0x80`). **Sem acentos.**

## Crie o arquivo

Escreva o código com um editor de texto. Sugestão: o **nano**.

```bash
cd ~
nano ficha64.asm
```

Para salvar: `Ctrl+O` e depois `Enter`. Para sair: `Ctrl+X`. Para continuar
editando depois, é só rodar `nano ficha64.asm` de novo.

## Monte, ligue e teste

```bash
nasm -f elf64 ficha64.asm -o ficha64.o
ld ficha64.o -o ficha64
./ficha64
echo $?
```

## Confira

```bash
/challenge/check
```

O `check` confere se o objeto e o executável são ELF **64 bits**, se o código
usa `syscall`, se as seis funções existem, são chamadas com `call` e terminam
com `ret`. Depois roda o programa com nomes, idades e cursos **sorteados** e
compara a saída caractere por caractere.
