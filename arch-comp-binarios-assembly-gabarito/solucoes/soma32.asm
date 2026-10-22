section .bss
    digitos resb 2

section .text
    global _start

_start:
    ; LEITURA: read(0, digitos, 2)
    mov eax, 3
    mov ebx, 0
    mov ecx, digitos
    mov edx, 2
    int 0x80

    ; primeiro digito: ASCII -> numero
    mov ebx, 0
    mov bl, [digitos]
    sub ebx, 48

    ; segundo digito: ASCII -> numero
    mov ecx, 0
    mov cl, [digitos + 1]
    sub ecx, 48

    add ebx, ecx

    ; SAIR: exit(soma)
    mov eax, 1
    int 0x80
