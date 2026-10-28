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

    ; exit(0)
    mov rax, 60
    mov rdi, 0
    syscall

print_nome:
    mov rax, 1
    mov rdi, 1
    mov rsi, nome
    mov rdx, tam_nome
    syscall
    ret

print_idade:
    mov rax, 1
    mov rdi, 1
    mov rsi, idade
    mov rdx, tam_idade
    syscall
    ret

print_curso:
    mov rax, 1
    mov rdi, 1
    mov rsi, curso
    mov rdx, tam_curso
    syscall
    ret
