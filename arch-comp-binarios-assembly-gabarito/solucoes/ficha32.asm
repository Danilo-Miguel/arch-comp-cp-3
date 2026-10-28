section .data
    pede_nome db "Digite seu nome: "
    tam_pede_nome equ $ - pede_nome
    pede_curso db "Digite seu curso: "
    tam_pede_curso equ $ - pede_curso
    rotulo_nome db "Nome: "
    tam_rotulo_nome equ $ - rotulo_nome
    rotulo_curso db "Curso: "
    tam_rotulo_curso equ $ - rotulo_curso

section .bss
    nome resb 32
    tam_nome resd 1
    curso resb 32
    tam_curso resd 1

section .text
    global _start

_start:
    call ler_nome
    call ler_curso
    call print_nome
    call print_curso

    ; SAIR: exit(0)
    mov eax, 1
    mov ebx, 0
    int 0x80

; ler_nome: pergunta o nome, le para [nome] e guarda o tamanho em [tam_nome]
ler_nome:
    mov eax, 4
    mov ebx, 1
    mov ecx, pede_nome
    mov edx, tam_pede_nome
    int 0x80

    mov eax, 3
    mov ebx, 0
    mov ecx, nome
    mov edx, 32
    int 0x80
    mov [tam_nome], eax
    ret

; ler_curso: pergunta o curso, le para [curso] e guarda o tamanho em [tam_curso]
ler_curso:
    mov eax, 4
    mov ebx, 1
    mov ecx, pede_curso
    mov edx, tam_pede_curso
    int 0x80

    mov eax, 3
    mov ebx, 0
    mov ecx, curso
    mov edx, 32
    int 0x80
    mov [tam_curso], eax
    ret

; print_nome: escreve "Nome: " e o nome lido
print_nome:
    mov eax, 4
    mov ebx, 1
    mov ecx, rotulo_nome
    mov edx, tam_rotulo_nome
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, nome
    mov edx, [tam_nome]
    int 0x80
    ret

; print_curso: escreve "Curso: " e o curso lido
print_curso:
    mov eax, 4
    mov ebx, 1
    mov ecx, rotulo_curso
    mov edx, tam_rotulo_curso
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, curso
    mov edx, [tam_curso]
    int 0x80
    ret
