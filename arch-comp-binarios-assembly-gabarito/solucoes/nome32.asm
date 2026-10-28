section .data
    pergunta db "Qual o seu nome? "
    tam_pergunta equ $ - pergunta
    saudacao db "Ola, "
    tam_saudacao equ $ - saudacao

section .bss
    nome resb 32

section .text
    global _start

_start:
    ; ESCRITA: write(1, pergunta, tam_pergunta)
    mov eax, 4
    mov ebx, 1
    mov ecx, pergunta
    mov edx, tam_pergunta
    int 0x80

    ; LEITURA: read(0, nome, 32), devolve em eax quantos bytes leu
    mov eax, 3
    mov ebx, 0
    mov ecx, nome
    mov edx, 32
    int 0x80
    mov esi, eax           ; esi = tamanho do nome (com o Enter)

    ; ESCRITA: write(1, saudacao, tam_saudacao)
    mov eax, 4
    mov ebx, 1
    mov ecx, saudacao
    mov edx, tam_saudacao
    int 0x80

    ; ESCRITA: write(1, nome, esi)
    mov eax, 4
    mov ebx, 1
    mov ecx, nome
    mov edx, esi
    int 0x80

    ; SAIR: exit(0)
    mov eax, 1
    mov ebx, 0
    int 0x80
