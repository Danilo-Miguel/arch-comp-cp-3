<h2 align="center">Seções, importações e entry point do PE</h2>

> **Atenção: você só pode errar UMA vez.** No segundo erro o exercício fica
> **invalidado** e a flag não é mais liberada. Arquivo ausente ou fora do
> formato não conta como tentativa, mas resposta errada conta. Confira tudo
> antes de rodar o `check`.

Um PE é dividido em **seções**: código (`.text`), dados só leitura (`.rdata`),
dados graváveis (`.data`) etc. Como o programa usa funções do Windows, ele
também tem uma **tabela de importação**, que diz ao *loader* quais DLLs
carregar e quais funções de cada DLL o programa chama.

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
objdump -h /challenge/programa.exe
objdump -x /challenge/programa.exe | less
```

- `objdump -h` lista as seções.
- Em `objdump -x`, procure o bloco **The Import Tables**: ele mostra o nome da
  DLL (`DLL Name`) e as funções importadas dela.
- Ainda no `objdump -x`, procure `ImageBase` e `AddressOfEntryPoint` no
  cabeçalho opcional.

Para somar em hexadecimal no terminal:

```bash
printf '0x%x\n' $((0x400 + 0x20))
```

## 2. Responda

Crie o arquivo `/home/hacker/exercicio2.txt` com **5 linhas**:

```
quantidade de seções (em decimal)
nome da DLL importada (com .dll)
ImageBase (hexadecimal com 0x)
AddressOfEntryPoint, a RVA do entry point (hexadecimal com 0x)
endereço virtual (VA) do entry point na memória (hexadecimal com 0x)
```

## 3. Confira

```bash
/challenge/check
```
