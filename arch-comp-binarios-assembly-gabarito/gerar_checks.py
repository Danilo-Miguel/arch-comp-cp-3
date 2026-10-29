#!/usr/bin/env python3
"""Gera os arquivos `check` do dojo arch-comp-binarios-assembly.

As respostas dos exercícios 1 a 3 ficam só aqui (no gabarito); os checks
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
#
# O registro fica em /home/hacker/.tentativas, um arquivo por exercício, e cada
# linha é assinada com um segredo tirado do /flag (que só o root lê): registro
# editado ou forjado não passa na assinatura e conta como um erro já gasto.
# Se o home deixar a pasta ficar com outro dono que não o aluno (root ou
# root_squash), ela também fica protegida contra remoção.

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/run/dojo/bin
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

# Pasta de verdade (não link) cujo dono não é o aluno.
protegida() {
    [ -d "$1" ] && [ ! -L "$1" ] && [ "$(stat -c %u -- "$1")" != "$UID_ALUNO" ]
}

assinar() {
    printf '%s|%s\n' "$1" "$(printf '%s\n%s\n%s' "$SEGREDO" "$DESAFIO" "$1" | sha256sum | cut -d' ' -f1)"
}

# Numa pasta do aluno, quem lê e grava é o aluno (sem risco de link para
# arquivo do root); na pasta protegida, quem grava é o root.
ler_registro() {
    if [ "$PROTEGIDO" = 1 ]; then cat -- "./$DESAFIO"; else como_aluno cat -- "./$DESAFIO"; fi
}

gravar() {
    if [ "$PROTEGIDO" = 1 ]; then
        assinar "$1" > "./$DESAFIO"
    else
        assinar "$1" | como_aluno tee -- "./$DESAFIO" > /dev/null
    fi || falha_interna "gravar"
}

abrir_registro() {
    command -v setpriv >/dev/null || falha_interna "setpriv ausente"
    UID_ALUNO=$(id -u "$ALUNO") || falha_interna "usuario"
    GID_ALUNO=$(id -g "$ALUNO") || falha_interna "grupo"
    SEGREDO=$(sha256sum /flag | cut -d' ' -f1)
    [ -n "$SEGREDO" ] || falha_interna "segredo"

    # Link ou arquivo com o nome da pasta: foi o aluno, tira do caminho.
    if [ -L "$ESTADO_DIR" ] || { [ -e "$ESTADO_DIR" ] && [ ! -d "$ESTADO_DIR" ]; }; then
        mv -- "$ESTADO_DIR" "$ESTADO_DIR.descartado.$$" || falha_interna "mv"
    fi

    # Se uma pasta protegida foi renomeada e trocada por outra, volta a original.
    if ! protegida "$ESTADO_DIR"; then
        local d
        while IFS= read -r -d '' d; do
            if protegida "$d" && [ -f "$d/$ESTADO_MARCA" ]; then
                [ -e "$ESTADO_DIR" ] && { mv -- "$ESTADO_DIR" "$ESTADO_DIR.descartado.$$" || falha_interna "mv"; }
                mv -- "$d" "$ESTADO_DIR" || falha_interna "mv"
                break
            fi
        done < <(find "$HOME_ALUNO" -mindepth 1 -maxdepth 1 -type d ! -user "$UID_ALUNO" -print0)
    fi

    if [ ! -e "$ESTADO_DIR" ]; then
        mkdir -m 700 -- "$ESTADO_DIR" || falha_interna "mkdir"
        chown 0:0 -- "$ESTADO_DIR" 2>/dev/null
        : > "$ESTADO_DIR/$ESTADO_MARCA" 2>/dev/null
    fi

    cd -P -- "$ESTADO_DIR" || falha_interna "cd"
    if protegida .; then PROTEGIDO=1; else PROTEGIDO=0; fi

    local linha situacao
    linha=$(ler_registro 2>/dev/null | head -n 1)
    situacao=${linha%%|*}
    if [ -z "$linha" ]; then
        situacao=""
    elif [ "$(assinar "$situacao")" != "$linha" ]; then
        situacao="erros=1"    # registro mexido: conta como um erro já gasto
    fi
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
    gravar aprovado
    echo "Correto! Flag:"
    cat /flag
    exit 0
}

# $@ = linhas de detalhe, mostradas só depois que o erro já foi gravado.
reprovar() {
    local erros=$((ERROS + 1))
    if [ "$erros" -ge "$MAX_ERROS" ]; then
        gravar invalido
    else
        gravar "erros=$erros"
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
# Avaliação por arquivo de respostas (exercícios 1 a 3)
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
# Avaliação de programa NASM de 32 ou 64 bits (exercícios 4 a 10)
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

# Código-fonte do aluno sem os comentários.
codigo() {
    como_aluno sed 's/;.*//' -- "$ASM" 2>/dev/null
}

como_aluno test -f "$ASM" || pre_requisito "Arquivo $NOME.asm não encontrado no seu diretório home."
como_aluno test -f "$OBJ" || pre_requisito "Objeto $NOME.o não encontrado. Monte com: @@MONTAR@@"
como_aluno test -f "$EXE" || pre_requisito "Executável $NOME não encontrado. Ligue com: @@LIGAR@@"
como_aluno test -x "$EXE" || pre_requisito "$NOME existe mas não é executável. Rode: chmod +x $NOME"
[ "$ASM" -nt "$OBJ" ] && pre_requisito "Você alterou $NOME.asm depois de montar. Monte e ligue de novo antes do check."
[ "$OBJ" -nt "$EXE" ] && pre_requisito "Você montou $NOME.o depois de ligar. Ligue de novo: @@LIGAR@@"
# Lê o cabeçalho ELF direto (sem o comando file, que pode não estar no PATH):
# bytes 0-3 = 7f 'E' 'L' 'F', byte 4 = classe (1 = 32 bits, 2 = 64 bits),
# bytes 16-17 = tipo (1 = objeto relocável, 2 = executável).
elf_tipo() {  # $1 = arquivo, $2 = tipo esperado
    local b
    b=($(como_aluno od -An -tu1 -N18 -- "$1" 2>/dev/null))
    [ "${b[0]}/${b[1]}/${b[2]}/${b[3]}" = "127/69/76/70" ] && [ "${b[4]}" = @@CLASSE@@ ] &&
        [ "${b[16]}" = "$2" ] && [ "${b[17]}" = 0 ]
}
elf_tipo "$OBJ" 1 || pre_requisito "$NOME.o não é um objeto ELF de @@BITS@@ bits. Use: @@MONTAR@@"
elf_tipo "$EXE" 2 || pre_requisito "$NOME não é um executável ELF de @@BITS@@ bits. Use: @@LIGAR@@"
codigo | grep -Eiq '^[[:space:]]*@@SYSCALL@@[[:space:]]*$' ||
    pre_requisito "Em @@BITS@@ bits as syscalls são feitas com '@@SYSCALL_TXT@@', que não aparece no $NOME.asm."
codigo | grep -Eiq '^[[:space:]]*@@SYSCALL_ERRADA@@[[:space:]]*$' &&
    pre_requisito "O $NOME.asm usa '@@ERRADA_TXT@@', mas este exercício é de @@BITS@@ bits: use '@@SYSCALL_TXT@@'."

# $@ = nomes das funções: cada uma precisa do rótulo, de um call e de um ret.
exigir_funcoes() {
    local f
    for f in "$@"; do
        codigo | grep -Eq "^[[:space:]]*$f:" ||
            pre_requisito "Não encontrei o rótulo da função $f no $NOME.asm."
        codigo | grep -Eiq "^[[:space:]]*call[[:space:]]+$f[[:space:]]*$" ||
            pre_requisito "A função $f precisa ser chamada com call (call $f)."
    done
    [ "$(codigo | grep -Eic '^[[:space:]]*ret[[:space:]]*$')" -ge $# ] ||
        pre_requisito "Cada uma das $# funções ($*) precisa terminar com ret."
}
@@PRE@@
# Roda o programa do aluno (como aluno). Cada argumento é uma linha digitada,
# enviada com uma pausa, como alguém no teclado. Define SAIDA e CODIGO.
executar() {
    local bruto
    bruto=$(
        { for linha in "$@"; do printf '%s\n' "$linha"; sleep 0.3; done; } 2>/dev/null |
            timeout 5 setpriv --reuid="$UID_ALUNO" --regid="$GID_ALUNO" --clear-groups -- "$EXE" 2>/dev/null |
            head -c 4096 | cat -v
        echo "#${PIPESTATUS[1]}"
    )
    CODIGO=${bruto##*#}
    SAIDA=${bruto%#*}
}

descrever_codigo() {
    case "$1" in
        124) echo "o programa travou (não encerrou em 5 s; faltou a syscall exit?)" ;;
        139) echo "o programa caiu com segmentation fault (faltou o exit ou um ret?)" ;;
        *) echo "o programa saiu com código $1" ;;
    esac
}

# $1 = descrição da entrada. Exige exit(0).
conferir_codigo() {
    [ "$CODIGO" = 0 ] ||
        reprovar "Entrada $1: era esperado exit(0), mas $(descrever_codigo "$CODIGO")."
}

# $1 = descrição da entrada, $2 = saída esperada, exatamente.
conferir() {
    conferir_codigo "$1"
    [ "$SAIDA" = "$2" ] ||
        reprovar "Entrada $1: a saída do programa está diferente." \
            "----- esperado -----" "$2" "----- obtido -------" "$SAIDA" "--------------------"
}

NOMES=(Ana Bruno Carla Diego Eduarda Felipe Gabriela Henrique Isabela Joao
       Larissa Mateus Natalia Otavio Paula Rafael Sofia Thiago Vitoria
       "Maria Clara" "Pedro Henrique" "Ana Beatriz" "Lucas Oliveira")
CURSOS=(ADS "Ciencia da Computacao" "Engenharia de Software" "Sistemas de Informacao"
        "Defesa Cibernetica" "Engenharia de Computacao" "Inteligencia Artificial")

@@CASOS@@

aprovar
'''


def sha(desafio, respostas):
    return hashlib.sha256((desafio + "\n" + "\n".join(respostas)).encode()).hexdigest()


# (pasta, desafio, título, arquivo, [(descrição, regex, resposta normalizada)])
QUESTIONARIOS = [
    ("exercicio-1/pe-cabecalho", "pe-cabecalho",
     "Exercício 1: Reconhecendo um executável do Windows (PE)", "exercicio1.txt", [
         ("os 2 primeiros caracteres do arquivo (2 letras)", r"^[a-z]{2}$", "mz"),
         ("formato, como o comando file mostra: PE32 ou PE32+", r"^pe32\+?$", "pe32"),
     ]),
    ("exercicio-2/pe-entry-point", "pe-entry-point",
     "Exercício 2: Entry point de um executável do Windows (PE)", "exercicio2.txt", [
         ("endereço do entry point (start address), em hexadecimal com 0x", r"^0x[0-9a-f]+$", "0x401040"),
     ]),
    ("exercicio-3/elf-cabecalho", "elf-cabecalho",
     "Exercício 3: Reconhecendo um executável do Linux (ELF)", "exercicio3.txt", [
         ("classe: ELF32 ou ELF64", r"^elf(32|64)$", "elf32"),
         ("endereço do entry point, em hexadecimal com 0x", r"^0x[0-9a-f]+$", "0x8049000"),
     ]),
]

CASOS_OLA = r'''
executar
conferir "(nenhuma)" $'Ola, FIAP!\nEstou aprendendo Assembly x86.\n'
'''

CASOS_NOME32 = r'''
for nome in Ana "${NOMES[RANDOM % ${#NOMES[@]}]}" "${NOMES[RANDOM % ${#NOMES[@]}]}"; do
    executar "$nome"
    conferir "'$nome'" "Qual o seu nome? Ola, $nome"$'\n'
done
'''

CASOS_NOME64 = r'''
for i in 1 2 3; do
    nome=${NOMES[RANDOM % ${#NOMES[@]}]}
    curso=${CURSOS[RANDOM % ${#CURSOS[@]}]}
    [ "$i" = 1 ] && nome=Ana curso=ADS
    executar "$nome" "$curso"
    conferir "'$nome' e '$curso'" \
        "Digite seu nome: Digite seu curso: Ola, $nome"$'\n'"Voce estuda $curso"$'\n'
done
'''

CASOS_FUNCOES = r'''
executar
conferir_codigo "(nenhuma)"
FORMATO=$'^Nome: [^\n]+\nIdade: [0-9]{1,3}\nCurso: [^\n]+\n$'
[[ $SAIDA =~ $FORMATO ]] ||
    reprovar "A saída precisa ter exatamente 3 linhas, nesta ordem:" \
        "Nome: <seu nome>" "Idade: <sua idade>" "Curso: <seu curso>" \
        "----- obtido -------" "$SAIDA" "--------------------"
'''

CASOS_FICHA32 = r'''
for i in 1 2 3; do
    nome=${NOMES[RANDOM % ${#NOMES[@]}]}
    curso=${CURSOS[RANDOM % ${#CURSOS[@]}]}
    [ "$i" = 1 ] && nome=Ana curso=ADS
    executar "$nome" "$curso"
    conferir "'$nome' e '$curso'" \
        "Digite seu nome: Digite seu curso: Nome: $nome"$'\n'"Curso: $curso"$'\n'
done
'''

CASOS_FICHA64 = r'''
for i in 1 2 3; do
    nome=${NOMES[RANDOM % ${#NOMES[@]}]}
    idade=$((17 + RANDOM % 43))
    curso=${CURSOS[RANDOM % ${#CURSOS[@]}]}
    [ "$i" = 1 ] && nome=Ana idade=20 curso=ADS
    executar "$nome" "$idade" "$curso"
    conferir "'$nome', '$idade' e '$curso'" \
        "Digite seu nome: Digite sua idade: Digite seu curso: Nome: $nome"$'\n'"Idade: $idade"$'\n'"Curso: $curso"$'\n'
done
'''

PRINTS = "\nexigir_funcoes print_nome print_idade print_curso\n"

# (pasta, desafio, título, nome, bits, pré-requisitos extras, casos de teste)
PROGRAMAS = [
    ("exercicio-4/asm-escrita", "asm-escrita",
     "Exercício 4: Escrita na tela com write (32 bits)", "ola32", 32, "", CASOS_OLA),
    ("exercicio-5/asm-leitura-escrita", "asm-leitura-escrita",
     "Exercício 5: Ciclo de leitura e escrita (32 bits)", "nome32", 32, "", CASOS_NOME32),
    ("exercicio-6/asm-leitura-escrita-64", "asm-leitura-escrita-64",
     "Exercício 6: Ciclo de leitura e escrita (64 bits)", "nome64", 64, "", CASOS_NOME64),
    ("exercicio-7/asm-funcoes", "asm-funcoes",
     "Exercício 7: Funções print_nome, print_idade e print_curso (32 bits)", "funcoes32", 32,
     PRINTS, CASOS_FUNCOES),
    ("exercicio-8/asm-funcoes-64", "asm-funcoes-64",
     "Exercício 8: Funções print_nome, print_idade e print_curso (64 bits)", "funcoes64", 64,
     PRINTS, CASOS_FUNCOES),
    ("exercicio-9/asm-ficha", "asm-ficha",
     "Exercício 9: Ficha do aluno com funções de leitura e escrita (32 bits)", "ficha32", 32,
     "\nexigir_funcoes ler_nome ler_curso print_nome print_curso\n", CASOS_FICHA32),
    ("exercicio-10/asm-ficha-64", "asm-ficha-64",
     "Exercício 10: Ficha do aluno com funções de leitura e escrita (64 bits)", "ficha64", 64,
     "\nexigir_funcoes ler_nome ler_idade ler_curso print_nome print_idade print_curso\n",
     CASOS_FICHA64),
]

FERRAMENTAS = {
    32: ("nasm -f elf32 {n}.asm -o {n}.o", "ld -m elf_i386 {n}.o -o {n}", "int 0x80", "syscall"),
    64: ("nasm -f elf64 {n}.asm -o {n}.o", "ld {n}.o -o {n}", "syscall", "int 0x80"),
}


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

for pasta, desafio, titulo, nome, bits, pre, casos in PROGRAMAS:
    montar, ligar, instrucao, errada = FERRAMENTAS[bits]
    corpo = (ASSEMBLY.replace("@@NOME@@", nome)
             .replace("@@MONTAR@@", montar.format(n=nome))
             .replace("@@LIGAR@@", ligar.format(n=nome))
             .replace("@@BITS@@", str(bits))
             .replace("@@CLASSE@@", "1" if bits == 32 else "2")
             .replace("@@SYSCALL_TXT@@", instrucao)
             .replace("@@ERRADA_TXT@@", errada)
             .replace("@@SYSCALL@@", instrucao.replace(" ", "[[:space:]]+"))
             .replace("@@SYSCALL_ERRADA@@", errada.replace(" ", "[[:space:]]+"))
             .replace("@@PRE@@", pre)
             .replace("@@CASOS@@", casos.strip("\n")))
    escrever(pasta, motor(desafio, titulo) + corpo)
