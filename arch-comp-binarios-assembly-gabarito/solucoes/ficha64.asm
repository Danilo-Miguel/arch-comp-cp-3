section .data
    pede_nome db "Digite seu nome: "
    tam_pede_nome equ $ - pede_nome
    pede_idade db "Digite sua idade: "
    tam_pede_idade equ $ - pede_idade
    pede_curso db "Digite seu curso: "
    tam_pede_curso equ $ - pede_curso
    rotulo_nome db "Nome: "
    tam_rotulo_nome equ $ - rotulo_nome
    rotulo_idade db "Idade: "
    tam_rotulo_idade equ $ - rotulo_idade
    rotulo_curso db "Curso: "
    tam_rotulo_curso equ $ - rotulo_curso

section .bss
    nome resb 32
    tam_nome resq 1
    idade resb 32
    tam_idade resq 1
    curso resb 32
    tam_curso resq 1

section .text
    global _start

_start:
    call ler_nome
    call ler_idade
    call ler_curso
    call print_nome
    call print_idade
    call print_curso

    ; exit(0)
    mov rax, 60
    mov rdi, 0
    syscall

ler_nome:
    mov rax, 1
    mov rdi, 1
    mov rsi, pede_nome
    mov rdx, tam_pede_nome
    syscall

    mov rax, 0
    mov rdi, 0
    mov rsi, nome
    mov rdx, 32
    syscall
    mov [tam_nome], rax
    ret

ler_idade:
    mov rax, 1
    mov rdi, 1
    mov rsi, pede_idade
    mov rdx, tam_pede_idade
    syscall

    mov rax, 0
    mov rdi, 0
    mov rsi, idade
    mov rdx, 32
    syscall
    mov [tam_idade], rax
    ret

ler_curso:
    mov rax, 1
    mov rdi, 1
    mov rsi, pede_curso
    mov rdx, tam_pede_curso
    syscall

    mov rax, 0
    mov rdi, 0
    mov rsi, curso
    mov rdx, 32
    syscall
    mov [tam_curso], rax
    ret

print_nome:
    mov rax, 1
    mov rdi, 1
    mov rsi, rotulo_nome
    mov rdx, tam_rotulo_nome
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, nome
    mov rdx, [tam_nome]
    syscall
    ret

print_idade:
    mov rax, 1
    mov rdi, 1
    mov rsi, rotulo_idade
    mov rdx, tam_rotulo_idade
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, idade
    mov rdx, [tam_idade]
    syscall
    ret

print_curso:
    mov rax, 1
    mov rdi, 1
    mov rsi, rotulo_curso
    mov rdx, tam_rotulo_curso
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, curso
    mov rdx, [tam_curso]
    syscall
    ret
