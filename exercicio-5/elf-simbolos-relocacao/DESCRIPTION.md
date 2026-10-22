<h2 align="center">Símbolos e tabela de relocação do ELF</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo ausente ou fora do
> formato não conta como tentativa, mas resposta errada conta. Confira tudo
> antes de rodar o `check`.

Quando você roda `nasm -f elf32 programa.asm -o programa.o`, o resultado
**ainda não é um executável**: é um *objeto relocável*. Nele, os endereços das
variáveis ainda não são conhecidos. Por isso o objeto carrega:

- uma **tabela de símbolos** (`.symtab`), com os rótulos do programa. Os
  declarados com `global` têm *Bind* `GLOBAL`, os outros `LOCAL`;
- uma **tabela de relocação** (`.rel.text`), que lista cada lugar do código
  onde o `ld` vai ter que escrever um endereço na hora de ligar.

O arquivo `/challenge/alvo.o` é o objeto que deu origem ao `alvo` do
exercício anterior.

## 1. Investigue

```bash
file /challenge/alvo.o
readelf -h /challenge/alvo.o
readelf -s /challenge/alvo.o
readelf -r /challenge/alvo.o
objdump -d -M intel -r /challenge/alvo.o
```

No `readelf -s`, a coluna `Ndx` diz em qual seção o símbolo está (compare com
os números de `readelf -S`). No `objdump -d -r`, veja em quais instruções as
relocações aparecem.

## 2. Responda

Crie o arquivo `/home/hacker/exercicio5.txt` com **4 linhas**:

```
tipo do arquivo alvo.o (só a sigla do campo Type: EXEC, DYN ou REL)
quantidade de entradas de relocação em .rel.text (decimal)
tipo das relocações (coluna Type do readelf -r)
nome do símbolo GLOBAL definido na seção .data
```

## 3. Confira

```bash
/challenge/check
```
