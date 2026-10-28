<h2 align="center">Reconhecendo um executável do Windows (PE)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo ausente ou fora do
> formato não conta como tentativa, mas resposta errada conta. Confira tudo
> antes de rodar o `check`.

O arquivo `/challenge/programa.exe` é um executável de **Windows**, no formato
**PE (Portable Executable)**. Dá para reconhecer um PE mesmo no Linux, sem
executá-lo:

- todo PE começa com as letras **`MZ`** (a "assinatura" do arquivo);
- o comando `file` identifica o formato sozinho.

## 1. Investigue

```bash
head -c 2 /challenge/programa.exe; echo
file /challenge/programa.exe
```

O `head -c 2` mostra os 2 primeiros caracteres do arquivo. O `file` diz se ele
é `PE32` (32 bits) ou `PE32+` (64 bits).

## 2. Responda

Crie o arquivo de resposta com um editor de texto. Sugestão: o **nano**.

```bash
nano ~/exercicio1.txt
```

Escreva **2 linhas**:

```
os 2 primeiros caracteres do arquivo
formato: PE32 ou PE32+
```

Para salvar no nano: `Ctrl+O` e depois `Enter`. Para sair: `Ctrl+X`.
Confira o que ficou salvo com `cat ~/exercicio1.txt`.

## 3. Confira

```bash
/challenge/check
```
