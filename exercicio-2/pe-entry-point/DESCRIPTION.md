<h2 align="center">Entry point de um executável do Windows (PE)</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo ausente ou fora do
> formato não conta como tentativa, mas resposta errada conta. Confira tudo
> antes de rodar o `check`.

O **entry point** (ponto de entrada) é o endereço da **primeira instrução**
que o programa executa. Em análise de malware, é por ele que se começa a ler
o código.

## 1. Investigue

```bash
objdump -f /challenge/programa.exe
```

Procure a linha `start address`: esse é o endereço do entry point.

## 2. Responda

Crie o arquivo de resposta com um editor de texto. Sugestão: o **nano**.

```bash
nano ~/exercicio2.txt
```

Escreva **1 linha**: o endereço do entry point, em hexadecimal com `0x`
(do jeito que o `objdump` mostra).

Para salvar no nano: `Ctrl+O` e depois `Enter`. Para sair: `Ctrl+X`.
Confira o que ficou salvo com `cat ~/exercicio2.txt`.

## 3. Confira

```bash
/challenge/check
```
