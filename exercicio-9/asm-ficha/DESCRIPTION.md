<h2 align="center">Ficha do aluno com funções de leitura e escrita (x86, 32 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com saída errada
> conta. **Teste o seu programa antes de rodar o `check`.**

Agora os dados vêm do teclado. Crie o arquivo `ficha32.asm` no seu diretório
home, em **Assembly x86 (32 bits)** com NASM, com **quatro funções**:

| função | o que faz |
|---|---|
| `ler_nome` | escreve `Digite seu nome: ` e lê o nome |
| `ler_curso` | escreve `Digite seu curso: ` e lê o curso |
| `print_nome` | escreve `Nome: ` seguido do nome lido |
| `print_curso` | escreve `Curso: ` seguido do curso lido |

O `_start` chama, nessa ordem, `ler_nome`, `ler_curso`, `print_nome` e
`print_curso`, e encerra com `exit(0)`.

No terminal fica assim (`Ana` e `ADS` foram digitados):

```
Digite seu nome: Ana
Digite seu curso: ADS
Nome: Ana
Curso: ADS
```

## Guardando o tamanho para outra função

O `read` devolve em `eax` quantos bytes leu, mas quem precisa desse valor é
**outra** função (`print_nome`), chamada depois. Como cada syscall estraga o
`eax`, `ebx`, `ecx` e `edx`, guarde o tamanho numa **variável** na `.bss`:

```nasm
section .bss
    nome resb 32
    tam_nome resd 1        ; 4 bytes para guardar o tamanho

ler_nome:
    ; write(1, pede_nome, tam_pede_nome)
    ; read(0, nome, 32)
    mov [tam_nome], eax    ; guarda quantos bytes foram lidos
    ret

print_nome:
    ; write(1, rotulo_nome, tam_rotulo_nome)
    ; write(1, nome, [tam_nome])   ->  mov edx, [tam_nome]
    ret
```

| syscall | `eax` | `ebx` | `ecx` | `edx` |
|---|---|---|---|---|
| `read` | `3` | `0` (teclado) | endereço do buffer | tamanho máximo |
| `write` | `4` | `1` (tela) | endereço do texto | quantidade de bytes |
| `exit` | `1` | código de saída | | |

**Sem acentos.**

## Monte, ligue e teste

```bash
nasm -f elf32 ficha32.asm -o ficha32.o
ld -m elf_i386 ficha32.o -o ficha32
./ficha32
echo $?
```

## Confira

```bash
/challenge/check
```

O `check` confere no seu `.asm` se as quatro funções existem, são chamadas com
`call` e terminam com `ret`. Depois roda o programa com nomes e cursos
**sorteados** e compara a saída caractere por caractere.
