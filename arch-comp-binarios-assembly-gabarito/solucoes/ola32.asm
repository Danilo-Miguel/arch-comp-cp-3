section .data
    mensagem db "Ola, FIAP!", 10, "Estou aprendendo Assembly x86.", 10
    tam_mensagem equ $ - mensagem

section .text
    global _start

_start:
    ; ESCRITA: write(1, mensagem, tam_mensagem)
    mov eax, 4
    mov ebx, 1
    mov ecx, mensagem
    mov edx, tam_mensagem
    int 0x80

    ; SAIR: exit(0)
    mov eax, 1
    mov ebx, 0
    int 0x80
