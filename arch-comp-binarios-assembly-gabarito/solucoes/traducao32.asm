section .bss
    buffer resb 1

section .text
    global _start

_start:
    mov eax, 3
    mov ebx, 0
    mov ecx, buffer
    mov edx, 1
    int 0x80

    mov ebx, 0
    mov bl, [buffer]
    sub ebx, 48
    add ebx, ebx
    add ebx, 10

    mov eax, 1
    int 0x80
