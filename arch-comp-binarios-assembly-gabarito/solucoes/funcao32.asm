section .bss
    digito resb 1

section .text
    global _start

_start:
    mov esi, 0             ; esi guarda a soma (ler_digito nao mexe nele)

    call ler_digito
    add esi, eax
    call ler_digito
    add esi, eax
    call ler_digito
    add esi, eax

    ; SAIR: exit(soma)
    mov ebx, esi
    mov eax, 1
    int 0x80

; ler_digito: le 1 caractere do teclado e devolve o digito (0 a 9) em EAX.
; Altera EBX, ECX e EDX.
ler_digito:
    mov eax, 3
    mov ebx, 0
    mov ecx, digito
    mov edx, 1
    int 0x80

    mov eax, 0
    mov al, [digito]
    sub eax, 48
    ret
