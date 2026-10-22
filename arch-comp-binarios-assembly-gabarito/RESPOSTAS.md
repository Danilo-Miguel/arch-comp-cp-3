# Gabarito: Estrutura de Binários e Introdução ao Assembly x86

**Não publique esta pasta.** Ela fica fora do repositório do dojo de propósito.
O `RESPOSTAS.md` do CP-4 está público no GitHub, então os alunos conseguem lê-lo.

Conteúdo desta pasta:

- `fontes/`: código dos binários inspecionados (`programa.asm`, um PE32 montado à mão, e `alvo.asm`) e o `build.sh`, que os gera e copia para o dojo;
- `solucoes/`: soluções dos exercícios 6 a 10;
- `gerar_checks.py`: gera todos os `check` do dojo. As respostas dos exercícios 1 a 5 estão nele; os `check` levam só o hash.

Se mudar uma resposta ou o motor de tentativas, rode `python3 gerar_checks.py`
de novo. Se mudar `programa.asm` ou `alvo.asm`, rode `bash fontes/build.sh` e
**atualize as respostas** no `gerar_checks.py`.

---

## Exercício 1: `pe-cabecalho` (`exercicio1.txt`)

```
MZ
0x80
PE32
i386
```

`od` mostra `80 00 00 00` no offset `0x3C` (e_lfanew = 0x80); `file` diz
`PE32 executable (console) Intel 80386`; `objdump -f` diz `architecture: i386`.

## Exercício 2: `pe-secoes-importacao` (`exercicio2.txt`)

```
3
.text
KERNEL32.dll
ExitProcess
```

Seções `.text`, `.rdata`, `.data`. Importa `GetStdHandle`, `WriteFile` e
`ExitProcess` da `KERNEL32.dll`.

## Exercício 3: `pe-entry-point` (`exercicio3.txt`)

```
0x400000
0x1040
0x401040
0x403000
```

O entry point **não** é o início da `.text` (`0x401000`): antes dele há a
função `imprime`. Quem chuta `0x1000` erra.

## Exercício 4: `elf-cabecalho-segmentos` (`exercicio4.txt`)

```
ELF32
EXEC
0x8049000
7
3
```

## Exercício 5: `elf-simbolos-relocacao` (`exercicio5.txt`)

```
REL
3
R_386_32
contador
```

As 3 relocações são `mov ecx, mensagem`, `inc dword [contador]` e
`mov ecx, buffer`.

Os checks aceitam maiúsculas/minúsculas, espaços extras, CRLF e hexadecimal com
zeros à esquerda (`0x00401040`). Hexadecimal sem `0x` é recusado como erro de
formato (não conta tentativa).

---

## Exercícios 6 a 10

Soluções completas em `solucoes/`. Montagem de todas:

```bash
nasm -f elf32 X.asm -o X.o
ld -m elf_i386 X.o -o X
```

| Ex. | Arquivo | Comportamento | Exemplo |
|---|---|---|---|
| 6 | `ascii32.asm` | sai com o ASCII do caractere lido | `A` → 65 |
| 7 | `soma32.asm` | sai com a soma de 2 dígitos | `37` → 10 |
| 8 | `maior32.asm` | sai com o maior de 2 dígitos | `27` → 7 |
| 9 | `traducao32.asm` | tradução do código AT&T: `2*d + 10` | `3` → 16 |
| 10 | `funcao32.asm` | `ler_digito` chamada 3×, sai com a soma | `123` → 6 |

Pré-requisitos extras que não gastam tentativa:

- Ex. 9: o `.asm` não pode ter `%` fora de comentário, e o `.o` precisa ter sido
  gerado pelo NASM a partir de `traducao32.asm` (símbolo `FILE`), para impedir
  que o aluno monte o código AT&T com `as`.
- Ex. 10: o executável precisa ter o rótulo `ler_digito`, pelo menos 3
  `call ler_digito` e um `ret`.

---

## Como resetar um aluno

Não há reset pela plataforma: com `allow_privileged: false`, ninguém tem root no
container. Para liberar um aluno, mude temporariamente para
`allow_privileged: true`, peça para ele entrar no modo *practice* do exercício e
rodar `sudo rm -rf ~/.tentativas` (isso zera **todos** os exercícios dele).
Depois volte para `false`.
