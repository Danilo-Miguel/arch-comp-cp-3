# Estrutura de Binários e Assembly x86 (32 e 64 bits)

Dojo do pwn.college com 10 exercícios, definido em [dojo.yml](./dojo.yml):
3 de estrutura de binários (PE e ELF) e 7 de Assembly com NASM.

| Módulo | Desafio | Tema |
|---|---|---|
| exercicio-1 | `pe-cabecalho` | Formato PE: cabeçalho DOS, `e_lfanew`, PE32 |
| exercicio-2 | `pe-secoes-entry-point` | Seções, importações, ImageBase, RVA e VA |
| exercicio-3 | `elf-cabecalho-segmentos` | Cabeçalho ELF, seções e segmentos |
| exercicio-4 | `asm-escrita` | `write` e `exit` (32 bits) |
| exercicio-5 | `asm-leitura-escrita` | Ciclo escrita → `read` → escrita (32 bits) |
| exercicio-6 | `asm-leitura-escrita-64` | Ciclo de leitura e escrita com `syscall` (64 bits) |
| exercicio-7 | `asm-funcoes` | Funções `print_nome`, `print_idade`, `print_curso` (32 bits) |
| exercicio-8 | `asm-funcoes-64` | As mesmas funções em 64 bits |
| exercicio-9 | `asm-ficha` | Funções `ler_*` e `print_*` com dados do teclado (32 bits) |
| exercicio-10 | `asm-ficha-64` | Ficha completa (nome, idade, curso) em 64 bits |

Assembly de 32 bits: `nasm -f elf32`, `ld -m elf_i386`, `int 0x80` com `read`
(3), `write` (4) e `exit` (1). Assembly de 64 bits: `nasm -f elf64`, `ld`,
`syscall` com `read` (0), `write` (1) e `exit` (60).

## Regra das tentativas

Cada `check` permite **um erro**. No segundo erro o exercício fica
**invalidado** para aquele aluno e o `check` não libera mais a flag.

- O registro fica em `/home/hacker/.tentativas`, uma pasta do **root** criada
  pelo `check`. O aluno não consegue apagar nem alterar o conteúdo. Se ele
  renomear a pasta ou criar outra no lugar, o `check` encontra a original.
- O dojo usa `allow_privileged: false`. Sem isso, o aluno poderia entrar no
  modo *practice* (com `sudo`) e apagar o registro.
- Arquivo ausente, resposta fora do formato, `.asm` alterado depois de montar,
  objeto/executável com o número de bits errado, `int 0x80` num exercício de
  64 bits (ou `syscall` num de 32) e função exigida sem rótulo/`call`/`ret`
  **não** contam como tentativa.
- Exercícios 1 a 3: o `check` guarda só o SHA-256 da resposta, sem o gabarito
  em texto puro.
- Exercícios 4 a 10: o programa do aluno roda com o usuário `hacker` (não como
  root), com limite de 5 segundos. O `check` digita as entradas sorteadas uma
  linha por vez (com uma pausa entre elas, como no teclado), compara a saída
  **caractere por caractere** e exige `exit(0)`.
