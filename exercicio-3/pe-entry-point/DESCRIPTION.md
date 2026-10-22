<h2 align="center">Entry point e carregamento do PE em memória</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo ausente ou fora do
> formato não conta como tentativa, mas resposta errada conta. Confira tudo
> antes de rodar o `check`.

Quando o Windows carrega um PE, ele copia o arquivo para a memória a partir de
um endereço base, o **ImageBase**. Os endereços dentro do PE são guardados como
**RVA (Relative Virtual Address)**, ou seja, a distância até o ImageBase. Para
saber o endereço real na memória (**VA**), basta somar:

```
VA = ImageBase + RVA
```

O **entry point** é a primeira instrução executada. O campo
`AddressOfEntryPoint` guarda a RVA dele.

## 1. Investigue

```bash
objdump -x /challenge/programa.exe | less
```

Procure `ImageBase` e `AddressOfEntryPoint` no cabeçalho opcional. Na lista de
seções (`Sections:`), a coluna `VMA` já mostra o endereço virtual de cada
seção. Use isso para conferir sua conta.

Para somar em hexadecimal no terminal:

```bash
printf '0x%x\n' $((0x400 + 0x20))
```

## 2. Responda

Crie o arquivo `/home/hacker/exercicio3.txt` com **4 linhas**, todos os valores
em hexadecimal com `0x`:

```
ImageBase
AddressOfEntryPoint (RVA do entry point)
endereço virtual (VA) do entry point na memória
endereço virtual (VA) onde a seção .data é carregada
```

## 3. Confira

```bash
/challenge/check
```
