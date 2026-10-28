section .data
    nome db "Nome: Ana Souza", 10
    tam_nome equ $ - nome
    idade db "Idade: 20", 10
    tam_idade equ $ - idade
    curso db "Curso: Ciencia da Computacao", 10
    tam_curso equ $ - curso

section .text
    global _start

_start:
    call print_nome
    call print_idade
    call print_curso

    ; SAIR: exit(0)
    mov eax, 1
    mov ebx, 0
    int 0x80

print_nome:
    mov eax, 4
    mov ebx, 1
    mov ecx, nome
    mov edx, tam_nome
    int 0x80
    ret

print_idade:
    mov eax, 4
    mov ebx, 1
    mov ecx, idade
    mov edx, tam_idade
    int 0x80
    ret

print_curso:
    mov eax, 4
    mov ebx, 1
    mov ecx, curso
    mov edx, tam_curso
    int 0x80
    ret
