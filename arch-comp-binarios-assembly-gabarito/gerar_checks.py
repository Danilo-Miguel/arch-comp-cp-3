#!/usr/bin/env python3
"""Gera os arquivos `check` do dojo arch-comp-binarios-assembly.

As respostas dos exercícios 1 a 5 ficam só aqui (no gabarito); os checks
publicados guardam apenas o SHA-256 da resposta normalizada.

Uso: python3 gerar_checks.py
"""
import hashlib
from pathlib import Path

DOJO = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Motor comum: controle de tentativas (1 erro permitido, 2º erro invalida)
# --------------------------------------------------------------------------
MOTOR = r'''#!/usr/bin/exec-suid -- /bin/bash -p
# @@TITULO@@
#
# Regra de tentativas: o aluno pode errar UMA vez. No segundo erro o exercício
# fica INVALIDADO e este check nunca mais libera a flag. Arquivo ausente,
# programa não montado/ligado ou resposta fora do formato NÃO contam como erro.
# O registro fica em /home/hacker/.tentativas, uma pasta do root: o aluno não
# consegue apagá-la nem alterar seu conteúdo (o dojo usa allow_privileged: false).

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
trap '' INT QUIT TSTP HUP

DESAFIO="@@DESAFIO@@"
ALUNO="hacker"
HOME_ALUNO="/home/hacker"
ESTADO_DIR="$HOME_ALUNO/.tentativas"
ESTADO_MARCA=".registro-tentativas"
MAX_ERROS=2

falha_interna() {
    echo "Erro interno do check ($1). Avise o professor."
    exit 2
}

# Tudo que mexe em arquivos do aluno roda com o usuário dele, nunca como root.
como_aluno() {
    setpriv --reuid="$UID_ALUNO" --regid="$GID_ALUNO" --clear-groups -- "$@"
}

dono_root() {
    [ -d "$1" ] && [ ! -L "$1" ] && [ "$(stat -c %u -- "$1")" = 0 ]
}

abrir_registro() {
    command -v setpriv >/dev/null || falha_interna "setpriv ausente"
    UID_ALUNO=$(id -u "$ALUNO") || falha_interna "usuario"
    GID_ALUNO=$(id -g "$ALUNO") || falha_interna "grupo"

    # Algo que não seja a pasta do root com esse nome foi criado pelo aluno.
    if [ -e "$ESTADO_DIR" ] || [ -L "$ESTADO_DIR" ]; then
        dono_root "$ESTADO_DIR" || mv -- "$ESTADO_DIR" "$ESTADO_DIR.descartado.$$" || falha_interna "mv"
    fi

    # O aluno não apaga a pasta do root, mas pode renomeá-la dentro do home.
    if [ ! -e "$ESTADO_DIR" ]; then
        local d
        while IFS= read -r -d '' d; do
            if [ -f "$d/$ESTADO_MARCA" ]; then
                mv -- "$d" "$ESTADO_DIR" || falha_interna "mv"
                break
            fi
        done < <(find "$HOME_ALUNO" -mindepth 1 -maxdepth 1 -type d -user root -print0)
    fi

    if [ ! -e "$ESTADO_DIR" ]; then
        mkdir -m 700 -- "$ESTADO_DIR" || falha_interna "mkdir"
        chown 0:0 -- "$ESTADO_DIR"
        : > "$ESTADO_DIR/$ESTADO_MARCA"
    fi

    cd -P -- "$ESTADO_DIR" || falha_interna "cd"
    [ "$(stat -c %u .)" = 0 ] && [ -f "$ESTADO_MARCA" ] || falha_interna "registro"

    local situacao
    situacao=$(cat -- "./$DESAFIO" 2>/dev/null)
    case "$situacao" in
        aprovado)
            echo "Você já concluiu este exercício. Flag:"
            cat /flag
            exit 0
            ;;
        invalido)
            echo "EXERCÍCIO INVALIDADO: você já errou $MAX_ERROS vezes."
            echo "A flag deste exercício não será mais liberada."
            exit 1
            ;;
        erros=[0-9]*) ERROS=${situacao#erros=} ;;
        *) ERROS=0 ;;
    esac
}

aprovar() {
    echo aprovado > "./$DESAFIO" || falha_interna "gravar"
    echo "Correto! Flag:"
    cat /flag
    exit 0
}

# $@ = linhas de detalhe, mostradas só depois que o erro já foi gravado.
reprovar() {
    local erros=$((ERROS + 1))
    if [ "$erros" -ge "$MAX_ERROS" ]; then
        echo invalido > "./$DESAFIO" || falha_interna "gravar"
    else
        echo "erros=$erros" > "./$DESAFIO" || falha_interna "gravar"
    fi
    echo "Resposta incorreta."
    printf '%s\n' "$@"
    echo
    if [ "$erros" -ge "$MAX_ERROS" ]; then
        echo "EXERCÍCIO INVALIDADO: este foi o seu erro número $erros."
        echo "A flag deste exercício não será mais liberada."
    else
        echo "ATENÇÃO: você tem só MAIS UMA tentativa."
        echo "Um novo erro invalida este exercício. Revise com calma antes de rodar o check de novo."
    fi
    exit 1
}

abrir_registro
'''

# --------------------------------------------------------------------------
# Avaliação por arquivo de respostas (exercícios 1 a 5)
# --------------------------------------------------------------------------
QUESTIONARIO = r'''
RESP="$HOME_ALUNO/@@ARQUIVO@@"
ESPERADO_SHA256="@@HASH@@"
# Uma linha por item: "descrição|regex do formato".
ITENS=(
@@ITENS@@
)

# minúsculas, sem espaços, sem linhas vazias, hexadecimal sem zeros à esquerda
normalizar() {
    tr -d '\r' | tr '[:upper:]' '[:lower:]' | tr -d ' \t' | sed '/^$/d' |
    while IFS= read -r l || [ -n "$l" ]; do
        if [[ $l =~ ^0x[0-9a-f]{1,8}$ ]]; then
            printf '0x%x\n' "$((l))"
        else
            printf '%s\n' "$l"
        fi
    done
}

mostrar_formato() {
    local i
    echo "Formato esperado em $RESP (${#ITENS[@]} linhas):"
    for i in "${!ITENS[@]}"; do
        echo "  linha $((i + 1)): ${ITENS[$i]%%|*}"
    done
}

if ! como_aluno test -f "$RESP"; then
    echo "Arquivo $RESP não encontrado (isso não conta como tentativa)."
    mostrar_formato
    exit 1
fi

CONTEUDO=$(como_aluno head -c 4096 -- "$RESP") || falha_interna "leitura"
NORMAL=$(printf '%s\n' "$CONTEUDO" | normalizar)
LINHAS=()
[ -n "$NORMAL" ] && mapfile -t LINHAS <<< "$NORMAL"

if [ "${#LINHAS[@]}" -ne "${#ITENS[@]}" ]; then
    echo "O arquivo tem ${#LINHAS[@]} linha(s) preenchida(s), mas deveria ter ${#ITENS[@]}."
    echo "(Erro de formato, não conta como tentativa.)"
    mostrar_formato
    exit 1
fi

for i in "${!ITENS[@]}"; do
    if ! [[ ${LINHAS[$i]} =~ ${ITENS[$i]#*|} ]]; then
        echo "Linha $((i + 1)) fora do formato: '${LINHAS[$i]}'"
        echo "(Erro de formato, não conta como tentativa.)"
        mostrar_formato
        exit 1
    fi
done

HASH=$(printf '%s\n%s' "$DESAFIO" "$NORMAL" | sha256sum | cut -d' ' -f1)

if [ "$HASH" = "$ESPERADO_SHA256" ]; then
    aprovar
else
    reprovar "Pelo menos uma das ${#ITENS[@]} linhas está errada."
fi
'''

# --------------------------------------------------------------------------
# Avaliação de programa NASM 32 bits (exercícios 6 a 10)
# --------------------------------------------------------------------------
ASSEMBLY = r'''
NOME="@@NOME@@"
ASM="$HOME_ALUNO/$NOME.asm"
OBJ="$HOME_ALUNO/$NOME.o"
EXE="$HOME_ALUNO/$NOME"

pre_requisito() {
    echo "$1"
    echo "(Isso não conta como tentativa.)"
    exit 1
}

como_aluno test -f "$ASM" || pre_requisito "Arquivo $NOME.asm não encontrado no seu diretório home."
como_aluno test -f "$OBJ" || pre_requisito "Objeto $NOME.o não encontrado. Monte com: nasm -f elf32 $NOME.asm -o $NOME.o"
como_aluno test -f "$EXE" || pre_requisito "Executável $NOME não encontrado. Ligue com: ld -m elf_i386 $NOME.o -o $NOME"
como_aluno test -x "$EXE" || pre_requisito "$NOME existe mas não é executável. Rode: chmod +x $NOME"
[ "$ASM" -nt "$OBJ" ] && pre_requisito "Você alterou $NOME.asm depois de montar. Monte e ligue de novo antes do check."
[ "$OBJ" -nt "$EXE" ] && pre_requisito "Você montou $NOME.o depois de ligar. Ligue de novo: ld -m elf_i386 $NOME.o -o $NOME"
como_aluno file -b -- "$OBJ" | grep -q "ELF 32-bit LSB relocatable" ||
    pre_requisito "$NOME.o não é um objeto ELF 32 bits. Use: nasm -f elf32 $NOME.asm -o $NOME.o"
como_aluno file -b -- "$EXE" | grep -q "ELF 32-bit LSB executable" ||
    pre_requisito "$NOME não é um executável ELF 32 bits. Use: ld -m elf_i386 $NOME.o -o $NOME"
@@PRE@@
# Roda o programa do aluno (como aluno) e imprime o código de saída.
executar() {
    printf '%s' "$1" | timeout 5 setpriv --reuid="$UID_ALUNO" --regid="$GID_ALUNO" --clear-groups -- "$EXE" >/dev/null 2>&1
    echo $?
}

descrever_codigo() {
    case "$1" in
        124) echo "o programa travou (não encerrou em 5 s; faltou a syscall exit?)" ;;
        139) echo "o programa caiu com segmentation fault" ;;
        *) echo "código de saída $1" ;;
    esac
}

@@CASOS@@

for i in "${!ENTRADAS[@]}"; do
    obtido=$(executar "${ENTRADAS[$i]}")
    if [ "$obtido" != "${ESPERADOS[$i]}" ]; then
        reprovar "Entrada '${ENTRADAS[$i]}': esperado código de saída ${ESPERADOS[$i]}, obtido: $(descrever_codigo "$obtido")."
    fi
done

aprovar
'''


def sha(desafio, respostas):
    return hashlib.sha256((desafio + "\n" + "\n".join(respostas)).encode()).hexdigest()


# (pasta, desafio, título, arquivo, [(descrição, regex, resposta normalizada)])
QUESTIONARIOS = [
    ("exercicio-1/pe-cabecalho", "pe-cabecalho",
     "Exercício 1: Formato PE, cabeçalho DOS e assinatura PE", "exercicio1.txt", [
         ("assinatura do cabeçalho DOS (2 letras ASCII)", r"^[a-z]{2}$", "mz"),
         ("offset do cabeçalho PE, campo e_lfanew (hexadecimal com 0x)", r"^0x[0-9a-f]+$", "0x80"),
         ("formato: PE32 ou PE32+", r"^pe32\+?$", "pe32"),
         ("arquitetura informada pelo objdump -f", r"^[a-z0-9_-]+$", "i386"),
     ]),
    ("exercicio-2/pe-secoes-importacao", "pe-secoes-importacao",
     "Exercício 2: Seções e tabela de importação do PE", "exercicio2.txt", [
         ("quantidade de seções (decimal)", r"^[0-9]+$", "3"),
         ("nome da seção que contém o código executável", r"^\.[a-z0-9_]+$", ".text"),
         ("nome da DLL importada (com .dll)", r"^[a-z0-9_]+\.dll$", "kernel32.dll"),
         ("função importada que encerra o processo", r"^[a-z0-9_]+$", "exitprocess"),
     ]),
    ("exercicio-3/pe-entry-point", "pe-entry-point",
     "Exercício 3: Entry point e carregamento do PE em memória", "exercicio3.txt", [
         ("ImageBase (hexadecimal com 0x)", r"^0x[0-9a-f]+$", "0x400000"),
         ("AddressOfEntryPoint, a RVA do entry point (hexadecimal com 0x)", r"^0x[0-9a-f]+$", "0x1040"),
         ("endereço virtual (VA) do entry point na memória (hexadecimal com 0x)", r"^0x[0-9a-f]+$", "0x401040"),
         ("endereço virtual (VA) onde a seção .data é carregada (hexadecimal com 0x)", r"^0x[0-9a-f]+$", "0x403000"),
     ]),
    ("exercicio-4/elf-cabecalho-segmentos", "elf-cabecalho-segmentos",
     "Exercício 4: Formato ELF, cabeçalho, seções e segmentos", "exercicio4.txt", [
         ("classe: ELF32 ou ELF64", r"^elf(32|64)$", "elf32"),
         ("tipo do arquivo (campo Type, só a sigla: EXEC, DYN ou REL)", r"^[a-z]+$", "exec"),
         ("endereço do entry point (hexadecimal com 0x)", r"^0x[0-9a-f]+$", "0x8049000"),
         ("quantidade de section headers (decimal)", r"^[0-9]+$", "7"),
         ("quantidade de segmentos do tipo LOAD (decimal)", r"^[0-9]+$", "3"),
     ]),
    ("exercicio-5/elf-simbolos-relocacao", "elf-simbolos-relocacao",
     "Exercício 5: Símbolos e tabela de relocação do ELF", "exercicio5.txt", [
         ("tipo do arquivo alvo.o (campo Type, só a sigla: EXEC, DYN ou REL)", r"^[a-z]+$", "rel"),
         ("quantidade de entradas de relocação em .rel.text (decimal)", r"^[0-9]+$", "3"),
         ("tipo das relocações (coluna Type do readelf -r)", r"^r_[a-z0-9_]+$", "r_386_32"),
         ("nome do símbolo GLOBAL definido na seção .data", r"^[a-z_][a-z0-9_]*$", "contador"),
     ]),
]

PRE_TRADUCAO = r'''
como_aluno sed 's/;.*//' -- "$ASM" 2>/dev/null | grep -q '%' &&
    pre_requisito "$NOME.asm ainda tem registradores com % (sintaxe AT&T). Traduza para a sintaxe Intel do NASM."
como_aluno readelf -sW -- "$OBJ" | grep -Eq 'FILE .*traducao32\.asm$' ||
    pre_requisito "$NOME.o precisa ser gerado pelo NASM a partir de $NOME.asm (nasm -f elf32 $NOME.asm -o $NOME.o)."
'''

PRE_FUNCAO = r'''
como_aluno readelf -sW -- "$EXE" | grep -Eq ' ler_digito$' ||
    pre_requisito "Não encontrei o rótulo ler_digito no executável."
[ "$(como_aluno objdump -d -- "$EXE" | grep -Ec 'call.*<ler_digito>')" -ge 3 ] ||
    pre_requisito "O programa deve chamar ler_digito com call três vezes."
como_aluno objdump -d -- "$EXE" | grep -Eq '[[:space:]]ret[[:space:]]*$' ||
    pre_requisito "A função ler_digito deve terminar com ret."
'''

# (pasta, desafio, título, nome, pré-requisitos extras, geração dos casos)
PROGRAMAS = [
    ("exercicio-6/asm-ascii", "asm-ascii",
     "Exercício 6: mov, leitura (read) e encerramento (exit)", "ascii32", "", r'''
CARACTERES=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
ENTRADAS=("A")
for _ in 1 2 3; do
    ENTRADAS+=("${CARACTERES:RANDOM % ${#CARACTERES}:1}")
done
ESPERADOS=()
for e in "${ENTRADAS[@]}"; do
    ESPERADOS+=("$(printf '%d' "'$e")")
done'''),
    ("exercicio-7/asm-soma", "asm-soma",
     "Exercício 7: add e sub com dígitos lidos do teclado", "soma32", "", r'''
ENTRADAS=("00" "99" "$((RANDOM % 10))$((RANDOM % 10))" "$((RANDOM % 10))$((RANDOM % 10))")
ESPERADOS=()
for e in "${ENTRADAS[@]}"; do
    ESPERADOS+=("$((${e:0:1} + ${e:1:1}))")
done'''),
    ("exercicio-8/asm-maior", "asm-maior",
     "Exercício 8: cmp e saltos condicionais", "maior32", "", r'''
ENTRADAS=("27" "72" "55" "$((RANDOM % 10))$((RANDOM % 10))" "$((RANDOM % 10))$((RANDOM % 10))")
ESPERADOS=()
for e in "${ENTRADAS[@]}"; do
    a=${e:0:1}; b=${e:1:1}
    ESPERADOS+=("$(( a > b ? a : b ))")
done'''),
    ("exercicio-9/asm-traducao", "asm-traducao",
     "Exercício 9: Sintaxe Intel vs AT&T", "traducao32", PRE_TRADUCAO, r'''
ENTRADAS=("0" "9" "$((RANDOM % 10))" "$((RANDOM % 10))")
ESPERADOS=()
for e in "${ENTRADAS[@]}"; do
    ESPERADOS+=("$((2 * e + 10))")
done'''),
    ("exercicio-10/asm-funcao", "asm-funcao",
     "Exercício 10: Chamada de função com call/ret", "funcao32", PRE_FUNCAO, r'''
ENTRADAS=("000" "999" "$((RANDOM % 10))$((RANDOM % 10))$((RANDOM % 10))" "$((RANDOM % 10))$((RANDOM % 10))$((RANDOM % 10))")
ESPERADOS=()
for e in "${ENTRADAS[@]}"; do
    ESPERADOS+=("$((${e:0:1} + ${e:1:1} + ${e:2:1}))")
done'''),
]


def escrever(pasta, conteudo):
    destino = DOJO / pasta / "check"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(conteudo.encode("utf-8"))
    print("gerado", destino.relative_to(DOJO))


def motor(desafio, titulo):
    return MOTOR.replace("@@DESAFIO@@", desafio).replace("@@TITULO@@", titulo)


for pasta, desafio, titulo, arquivo, itens in QUESTIONARIOS:
    linhas = "\n".join('    "%s|%s"' % (d, r) for d, r, _ in itens)
    corpo = (QUESTIONARIO.replace("@@ARQUIVO@@", arquivo)
             .replace("@@HASH@@", sha(desafio, [resp for _, _, resp in itens]))
             .replace("@@ITENS@@", linhas))
    escrever(pasta, motor(desafio, titulo) + corpo)

for pasta, desafio, titulo, nome, pre, casos in PROGRAMAS:
    corpo = (ASSEMBLY.replace("@@NOME@@", nome)
             .replace("@@PRE@@", pre)
             .replace("@@CASOS@@", casos.strip("\n")))
    escrever(pasta, motor(desafio, titulo) + corpo)
