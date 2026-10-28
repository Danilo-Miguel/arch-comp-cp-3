<h2 align="center">Ciclo de leitura e escrita (x86-64, 64 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com saída errada
> conta. **Teste o seu programa antes de rodar o `check`.**

Agora em **64 bits**. A ideia é a mesma do exercício anterior, mas mudam os
registradores, os números das syscalls e a instrução: sai o `int 0x80`, entra
o **`syscall`**.

| syscall | `rax` | `rdi` | `rsi` | `rdx` |
|---|---|---|---|---|
| `read` | `0` | `0` (teclado) | endereço do buffer | tamanho máximo |
| `write` | `1` | `1` (tela) | endereço do texto | quantidade de bytes |
| `exit` | `60` | código de saída | | |

Crie o arquivo `nome64.asm` no seu diretório home, em **Assembly x86-64** com
NASM, que:

1. Escreva `Digite seu nome: ` e leia o nome (buffer de 32 bytes);
2. Escreva `Digite seu curso: ` e leia o curso (outro buffer de 32 bytes);
3. Escreva `Ola, ` seguido do nome;
4. Escreva `Voce estuda ` seguido do curso;
5. Encerre com `exit(0)`.

No terminal fica assim (`Ana` e `ADS` foram digitados):

```
Digite seu nome: Ana
Digite seu curso: ADS
Ola, Ana
Voce estuda ADS
```

Como no exercício anterior, o `read` devolve em **`rax`** quantos bytes leu
(com o Enter). Guarde os dois tamanhos em registradores que **não** são usados
pelas syscalls, como `r12` e `r13`. Cuidado: além de `rax`, a instrução
`syscall` também estraga `rcx` e `r11`.

**Sem acentos**: `Ola`, `Voce`.

## Monte, ligue e teste

```bash
nasm -f elf64 nome64.asm -o nome64.o
ld nome64.o -o nome64
./nome64
echo $?
```

## Confira

```bash
/challenge/check
```

O `check` confere se o objeto e o executável são ELF **64 bits**, se o código
usa `syscall` (e não `int 0x80`) e roda o programa com nomes e cursos
**sorteados**, comparando a saída caractere por caractere.
