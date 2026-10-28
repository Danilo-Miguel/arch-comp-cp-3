# Estrutura de Binários e Assembly x86 (32 e 64 bits)

Dojo do pwn.college com 10 exercícios, definido em [dojo.yml](./dojo.yml):
3 de reconhecimento de binários (PE e ELF), em nível introdutório, e 7 de
Assembly com NASM. Todos os enunciados sugerem o `nano` para criar os arquivos.

| Módulo | Desafio | Tema |
|---|---|---|
| exercicio-1 | `pe-cabecalho` | Reconhecer um PE: assinatura `MZ` e `file` |
| exercicio-2 | `pe-entry-point` | Achar o entry point de um PE com `objdump -f` |
| exercicio-3 | `elf-cabecalho` | Classe e entry point de um ELF com `readelf -h` |
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

- O registro fica em `/home/hacker/.tentativas`, um arquivo por exercício.
  Cada registro é **assinado** com um segredo derivado do `/flag` (que só o
  root lê): registro editado ou forjado conta como um erro já gasto.
- Quando o home permite, a pasta fica com dono diferente do aluno e ele não
  consegue nem apagá-la; se ele renomear a pasta e criar outra, o `check`
  encontra a original. Se o home deixa tudo com dono `hacker`, a assinatura
  continua valendo, mas apagar a pasta inteira zera as tentativas.
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
