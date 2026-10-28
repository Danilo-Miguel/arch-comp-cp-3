<h2 align="center">Reconhecendo um executável do Linux (ELF)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo ausente ou fora do
> formato não conta como tentativa, mas resposta errada conta. Confira tudo
> antes de rodar o `check`.

No Linux, os executáveis usam o formato **ELF (Executable and Linkable
Format)**. O arquivo `/challenge/alvo` é um ELF montado com NASM e ligado com
`ld`, do mesmo jeito que você faz nos exercícios de Assembly.

O comando `readelf -h` mostra o **cabeçalho** do ELF, com informações como se
ele é de 32 ou 64 bits e onde fica o entry point.

## 1. Investigue

```bash
file /challenge/alvo
readelf -h /challenge/alvo
```

No `readelf -h`, procure as linhas `Class` e `Entry point address`.

## 2. Responda

Crie o arquivo de resposta com um editor de texto. Sugestão: o **nano**.

```bash
nano ~/exercicio3.txt
```

Escreva **2 linhas**:

```
classe: ELF32 ou ELF64
endereço do entry point (hexadecimal com 0x)
```

Para salvar no nano: `Ctrl+O` e depois `Enter`. Para sair: `Ctrl+X`.
Confira o que ficou salvo com `cat ~/exercicio3.txt`.

## 3. Confira

```bash
/challenge/check
```
