<h2 align="center">Formato ELF: cabeçalho, seções e segmentos</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo ausente ou fora do
> formato não conta como tentativa, mas resposta errada conta. Confira tudo
> antes de rodar o `check`.

No Linux, os executáveis usam o formato **ELF (Executable and Linkable
Format)**. Um ELF tem:

- um **cabeçalho ELF** (classe 32/64 bits, tipo, entry point...);
- **seções** (`.text`, `.data`, `.bss`, `.symtab`...), usadas pelo *linker*;
- **segmentos** (*program headers*), usados pelo *loader*. Os do tipo `LOAD`
  são os pedaços copiados para a memória.

O arquivo `/challenge/alvo` é um ELF montado com NASM e ligado com `ld`, do
mesmo jeito que você faz em aula.

## 1. Investigue

```bash
file /challenge/alvo
readelf -h /challenge/alvo
readelf -S /challenge/alvo
readelf -l /challenge/alvo
```

## 2. Responda

Crie o arquivo `/home/hacker/exercicio4.txt` com **5 linhas**:

```
classe: ELF32 ou ELF64
tipo do arquivo (só a sigla do campo Type: EXEC, DYN ou REL)
endereço do entry point (hexadecimal com 0x)
quantidade de section headers (decimal)
quantidade de segmentos do tipo LOAD (decimal)
```

## 3. Confira

```bash
/challenge/check
```
