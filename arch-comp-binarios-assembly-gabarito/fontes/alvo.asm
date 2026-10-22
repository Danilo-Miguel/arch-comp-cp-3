; alvo: ELF 32 bits usado nos exercícios 4 e 5.
; nasm -f elf32 alvo.asm -o alvo.o && ld -m elf_i386 alvo.o -o alvo

section .data
    mensagem db "Simbolos e relocacao!", 10
    tamanho equ $ - mensagem
    global contador
    contador dd 0

section .bss
    buffer resb 16

section .text
    global _start

_start:
    mov eax, 4
    mov ebx, 1
    mov ecx, mensagem
    mov edx, tamanho
    int 0x80

    inc dword [contador]

    mov eax, 3
    mov ebx, 0
    mov ecx, buffer
    mov edx, 16
    int 0x80

    mov eax, 1
    mov ebx, 0
    int 0x80
