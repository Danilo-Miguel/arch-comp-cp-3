# Estrutura de Binários e Introdução ao Assembly x86

Dojo do pwn.college com 10 exercícios, definido em [dojo.yml](./dojo.yml).

| Módulo | Desafio | Tema |
|---|---|---|
| exercicio-1 | `pe-cabecalho` | Formato PE: cabeçalho DOS, `e_lfanew`, PE32 |
| exercicio-2 | `pe-secoes-importacao` | Seções e tabela de importação |
| exercicio-3 | `pe-entry-point` | Entry point, ImageBase, RVA e VA |
| exercicio-4 | `elf-cabecalho-segmentos` | Cabeçalho ELF, seções e segmentos |
| exercicio-5 | `elf-simbolos-relocacao` | Símbolos e tabela de relocação |
| exercicio-6 | `asm-ascii` | `mov`, `read` e `exit` |
| exercicio-7 | `asm-soma` | `add` e `sub` |
| exercicio-8 | `asm-maior` | `cmp` e saltos condicionais |
| exercicio-9 | `asm-traducao` | Sintaxe Intel vs AT&T |
| exercicio-10 | `asm-funcao` | `call`/`ret` e retorno em `eax` |

Todos os exercícios de Assembly são **x86 de 32 bits** com NASM, `int 0x80` e
as syscalls `read` (3), `write` (4) e `exit` (1).

## Regra das tentativas

Cada `check` permite **um erro**. No segundo erro o exercício fica
**invalidado** para aquele aluno e o `check` não libera mais a flag.

- O registro fica em `/home/hacker/.tentativas`, uma pasta do **root** criada
  pelo `check`. O aluno não consegue apagar nem alterar o conteúdo. Se ele
  renomear a pasta ou criar outra no lugar, o `check` encontra a original.
- O dojo usa `allow_privileged: false`. Sem isso, o aluno poderia entrar no
  modo *practice* (com `sudo`) e apagar o registro.
- Arquivo ausente, resposta fora do formato, `.asm` alterado depois de montar e
  objeto/executável que não é ELF 32 bits **não** contam como tentativa.
- Exercícios 1 a 5: o `check` guarda só o SHA-256 da resposta, sem o gabarito
  em texto puro.
- Exercícios 6 a 10: o programa do aluno roda com o usuário `hacker` (não como
  root), com entradas sorteadas e limite de 5 segundos.
