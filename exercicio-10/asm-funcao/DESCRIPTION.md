<h2 align="center">Chamada de função com call/ret (x86, 32 bits)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo faltando ou programa não
> montado/ligado não conta como tentativa, mas programa com resultado errado
> conta. **Teste o seu programa antes de rodar o `check`.**

Uma **função** em Assembly é só um rótulo que termina com `ret`:

- `call rotulo` guarda o endereço de retorno na pilha e salta para a função;
- `ret` tira esse endereço da pilha e volta para a instrução depois do `call`;
- **convenção**: a função devolve o resultado em `eax`.

Crie o arquivo `funcao32.asm` no seu diretório home, em **Assembly x86
(32 bits)** com NASM, com:

1. Uma função chamada **`ler_digito`**, que lê **1 caractere** com `read`,
   converte de ASCII para número (subtrai 48) e devolve o dígito em `eax`, terminando com `ret`;
2. Um `_start` que chama `ler_digito` **três vezes** com `call`, soma os três
   dígitos e encerra com `exit`, usando a soma como código de saída.

Exemplo: digitando `123`, o programa deve sair com código `6`.

Cuidado: dentro de `ler_digito` a syscall `read` usa `eax`, `ebx`, `ecx` e
`edx`, então o valor que estiver neles **se perde**. Guarde a soma num
registrador que a função não usa, como o `esi`.

```nasm
_start:
    mov esi, 0
    call ler_digito
    add esi, eax
    ; ... mais duas vezes ...
    ; exit com o valor de esi

ler_digito:
    ; read de 1 byte, converte, resultado em eax
    ret
```

## Monte, ligue e teste

```bash
nasm -f elf32 funcao32.asm -o funcao32.o
ld -m elf_i386 funcao32.o -o funcao32
printf '123' | ./funcao32
echo $?
```

## Confira

```bash
/challenge/check
```

O `check` confere se existe o rótulo `ler_digito`, se ele é chamado com `call`
três vezes e se há `ret`, e então roda o programa com dígitos **sorteados**.
