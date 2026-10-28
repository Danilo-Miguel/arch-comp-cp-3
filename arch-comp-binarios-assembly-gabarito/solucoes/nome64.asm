section .data
    pede_nome db "Digite seu nome: "
    tam_pede_nome equ $ - pede_nome
    pede_curso db "Digite seu curso: "
    tam_pede_curso equ $ - pede_curso
    saudacao db "Ola, "
    tam_saudacao equ $ - saudacao
    estuda db "Voce estuda "
    tam_estuda equ $ - estuda

section .bss
    nome resb 32
    curso resb 32

section .text
    global _start

_start:
    ; write(1, pede_nome, tam_pede_nome)
    mov rax, 1
    mov rdi, 1
    mov rsi, pede_nome
    mov rdx, tam_pede_nome
    syscall

    ; read(0, nome, 32)
    mov rax, 0
    mov rdi, 0
    mov rsi, nome
    mov rdx, 32
    syscall
    mov r12, rax           ; r12 = tamanho do nome

    ; write(1, pede_curso, tam_pede_curso)
    mov rax, 1
    mov rdi, 1
    mov rsi, pede_curso
    mov rdx, tam_pede_curso
    syscall

    ; read(0, curso, 32)
    mov rax, 0
    mov rdi, 0
    mov rsi, curso
    mov rdx, 32
    syscall
    mov r13, rax           ; r13 = tamanho do curso

    ; "Ola, " + nome
    mov rax, 1
    mov rdi, 1
    mov rsi, saudacao
    mov rdx, tam_saudacao
    syscall
    mov rax, 1
    mov rdi, 1
    mov rsi, nome
    mov rdx, r12
    syscall

    ; "Voce estuda " + curso
    mov rax, 1
    mov rdi, 1
    mov rsi, estuda
    mov rdx, tam_estuda
    syscall
    mov rax, 1
    mov rdi, 1
    mov rsi, curso
    mov rdx, r13
    syscall

    ; exit(0)
    mov rax, 60
    mov rdi, 0
    syscall
