# Gabarito: Estrutura de Binários e Assembly x86 (32 e 64 bits)

**Não publique esta pasta.** Ela fica fora do repositório do dojo de propósito.
O `RESPOSTAS.md` do CP-4 está público no GitHub, então os alunos conseguem lê-lo.

Conteúdo desta pasta:

- `fontes/`: código dos binários inspecionados (`programa.asm`, um PE32 montado à mão, e `alvo.asm`) e o `build.sh`, que os gera e copia para o dojo;
- `solucoes/`: soluções dos exercícios 4 a 10;
- `gerar_checks.py`: gera todos os `check` do dojo. As respostas dos exercícios 1 a 3 estão nele; os `check` levam só o hash.

Se mudar uma resposta, um caso de teste ou o motor de tentativas, rode
`python3 gerar_checks.py` de novo. Se mudar `programa.asm` ou `alvo.asm`, rode
`bash fontes/build.sh` e **atualize as respostas** no `gerar_checks.py`.

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

## Exercício 2: `pe-secoes-entry-point` (`exercicio2.txt`)

```
3
KERNEL32.dll
0x400000
0x1040
0x401040
```

Seções `.text`, `.rdata`, `.data`. Importa `GetStdHandle`, `WriteFile` e
`ExitProcess` da `KERNEL32.dll`. O entry point **não** é o início da `.text`
(`0x401000`): antes dele há a função `imprime`. Quem chuta `0x1000` erra.

## Exercício 3: `elf-cabecalho-segmentos` (`exercicio3.txt`)

```
ELF32
EXEC
0x8049000
7
3
```

Os checks aceitam maiúsculas/minúsculas, espaços extras, CRLF e hexadecimal com
zeros à esquerda (`0x00401040`). Hexadecimal sem `0x` é recusado como erro de
formato (não conta tentativa).

---

## Exercícios 4 a 10

Soluções completas em `solucoes/`. Montagem:

```bash
nasm -f elf32 X.asm -o X.o && ld -m elf_i386 X.o -o X   # 32 bits
nasm -f elf64 X.asm -o X.o && ld X.o -o X               # 64 bits
```

| Ex. | Arquivo | Bits | Saída esperada (entradas `Ana`, `20`, `ADS`) |
|---|---|---|---|
| 4 | `ola32.asm` | 32 | `Ola, FIAP!` / `Estou aprendendo Assembly x86.` |
| 5 | `nome32.asm` | 32 | `Qual o seu nome? Ola, Ana` |
| 6 | `nome64.asm` | 64 | `Digite seu nome: Digite seu curso: Ola, Ana` / `Voce estuda ADS` |
| 7 | `funcoes32.asm` | 32 | `Nome: ...` / `Idade: <número>` / `Curso: ...` (dados do aluno) |
| 8 | `funcoes64.asm` | 64 | igual ao 7 |
| 9 | `ficha32.asm` | 32 | `Digite seu nome: Digite seu curso: Nome: Ana` / `Curso: ADS` |
| 10 | `ficha64.asm` | 64 | `Digite seu nome: Digite sua idade: Digite seu curso: Nome: Ana` / `Idade: 20` / `Curso: ADS` |

(`/` = quebra de linha; toda saída termina com `\n`. Os prompts aparecem
"colados" porque, com a entrada vinda de um pipe, o que o aluno digita não é
ecoado na tela.)

Como o `check` testa:

- Envia cada linha de entrada separada por 0,3 s, para que cada `read` receba
  uma linha só, como no teclado. Nomes (com espaço às vezes) e cursos são
  sorteados de listas no próprio `check`; a idade, de 17 a 59. O maior valor
  tem 24 caracteres, então buffers de 32 bytes bastam.
- A saída passa por `cat -v`: quem escreve o buffer inteiro (32 bytes) em vez
  de usar o retorno do `read` vê os `^@` no erro.
- Ex. 7 e 8 não têm entrada: a saída é conferida por regex
  (`Nome: .+`, `Idade: [0-9]{1,3}`, `Curso: .+`).
- O código de saída precisa ser 0. Segfault (faltou `exit`) conta tentativa.

Pré-requisitos que não gastam tentativa:

- ELF de 32 ou 64 bits conforme o exercício (`file` no `.o` e no executável);
- em 32 bits o `.asm` precisa ter `int 0x80` e não pode ter `syscall`; em 64
  bits, o contrário;
- Ex. 7 e 8: rótulos `print_nome`, `print_idade`, `print_curso`, um
  `call` para cada e pelo menos 3 `ret`;
- Ex. 9: `ler_nome`, `ler_curso`, `print_nome`, `print_curso` (idem);
- Ex. 10: `ler_nome`, `ler_idade`, `ler_curso`, `print_nome`, `print_idade`,
  `print_curso` (idem).

---

## Como resetar um aluno

Não há reset pela plataforma: com `allow_privileged: false`, ninguém tem root no
container. Para liberar um aluno, mude temporariamente para
`allow_privileged: true`, peça para ele entrar no modo *practice* do exercício e
rodar `sudo rm -rf ~/.tentativas` (isso zera **todos** os exercícios dele).
Depois volte para `false`.
