section .bss
    caractere resb 1

section .text
    global _start

_start:
    ; LEITURA: read(0, caractere, 1)
    mov eax, 3
    mov ebx, 0
    mov ecx, caractere
    mov edx, 1
    int 0x80

    ; SAIR: exit(codigo ASCII do caractere)
    mov ebx, 0
    mov bl, [caractere]
    mov eax, 1
    int 0x80
