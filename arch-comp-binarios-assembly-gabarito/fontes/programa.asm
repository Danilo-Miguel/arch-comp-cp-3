; programa.exe: PE32 (Windows, console, i386) montado à mão com NASM.
; Monte com: nasm -f bin programa.asm -o programa.exe
; Importa GetStdHandle, WriteFile e ExitProcess da KERNEL32.dll.

BITS 32

IMAGEBASE   equ 0x00400000
SECT_ALIGN  equ 0x1000
FILE_ALIGN  equ 0x200

%define RVA(x) ((x) - IMAGEBASE)

section cabecalho start=0          vstart=IMAGEBASE
section codigo    start=0x200      vstart=IMAGEBASE+0x1000
section rdados    start=0x400      vstart=IMAGEBASE+0x2000
section dados     start=0x600      vstart=IMAGEBASE+0x3000

; ---------------------------------------------------------------- cabeçalhos
section cabecalho

dos_header:
    dw "MZ"                     ; e_magic
    dw 0x90, 3, 0, 4, 0, 0xFFFF, 0, 0xB8, 0, 0, 0, 0x40, 0
    times 4 dw 0                ; e_res
    dw 0, 0                     ; e_oemid, e_oeminfo
    times 10 dw 0               ; e_res2
    dd pe_header - dos_header   ; e_lfanew

dos_stub:                       ; stub clássico: imprime a mensagem e sai no DOS
    db 0x0E, 0x1F, 0xBA, 0x0E, 0x00, 0xB4, 0x09, 0xCD, 0x21, 0xB8, 0x01, 0x4C, 0xCD, 0x21
    db "This program cannot be run in DOS mode.", 13, 13, 10, "$"
    align 0x80, db 0

pe_header:
    db "PE", 0, 0
    ; COFF File Header
    dw 0x014C                   ; Machine: i386
    dw 3                        ; NumberOfSections
    dd 0x6716C900               ; TimeDateStamp
    dd 0, 0                     ; PointerToSymbolTable, NumberOfSymbols
    dw opt_fim - opt_header     ; SizeOfOptionalHeader
    dw 0x0103                   ; RELOCS_STRIPPED | EXECUTABLE_IMAGE | 32BIT_MACHINE

opt_header:
    dw 0x010B                   ; Magic: PE32
    db 14, 0                    ; Linker version
    dd FILE_ALIGN               ; SizeOfCode
    dd 2 * FILE_ALIGN           ; SizeOfInitializedData
    dd 0                        ; SizeOfUninitializedData
    dd RVA(entrada)             ; AddressOfEntryPoint
    dd 0x1000                   ; BaseOfCode
    dd 0x2000                   ; BaseOfData
    dd IMAGEBASE                ; ImageBase
    dd SECT_ALIGN               ; SectionAlignment
    dd FILE_ALIGN               ; FileAlignment
    dw 6, 0                     ; OS version
    dw 0, 0                     ; Image version
    dw 6, 0                     ; Subsystem version
    dd 0                        ; Win32VersionValue
    dd 0x4000                   ; SizeOfImage
    dd 0x200                    ; SizeOfHeaders
    dd 0                        ; CheckSum
    dw 3                        ; Subsystem: WINDOWS_CUI (console)
    dw 0x0100                   ; DllCharacteristics: NX_COMPAT
    dd 0x100000, 0x1000         ; Stack reserve/commit
    dd 0x100000, 0x1000         ; Heap reserve/commit
    dd 0                        ; LoaderFlags
    dd 16                       ; NumberOfRvaAndSizes
    ; Data Directories
    dd 0, 0                                     ; 0 Export
    dd RVA(import_desc), import_desc_fim - import_desc ; 1 Import
    times 10 dd 0, 0                            ; 2..11
    dd RVA(iat), iat_fim - iat                  ; 12 IAT
    times 3 dd 0, 0                             ; 13..15
opt_fim:

    ; Section Table
    db ".text", 0, 0, 0
    dd codigo_fim - codigo_ini, 0x1000, FILE_ALIGN, 0x200
    dd 0, 0
    dw 0, 0
    dd 0x60000020               ; CODE | EXECUTE | READ

    db ".rdata", 0, 0
    dd rdados_fim - rdados_ini, 0x2000, FILE_ALIGN, 0x400
    dd 0, 0
    dw 0, 0
    dd 0x40000040               ; INITIALIZED_DATA | READ

    db ".data", 0, 0, 0
    dd dados_fim - dados_ini, 0x3000, FILE_ALIGN, 0x600
    dd 0, 0
    dw 0, 0
    dd 0xC0000040               ; INITIALIZED_DATA | READ | WRITE

    times FILE_ALIGN - ($ - $$) db 0

; ---------------------------------------------------------------- .text
section codigo
codigo_ini:

imprime:                        ; WriteFile(GetStdHandle(-11), mensagem, tam, &escritos, 0)
    push ebp
    mov ebp, esp
    push -11                    ; STD_OUTPUT_HANDLE
    call [iat_GetStdHandle]
    push 0
    push escritos
    push TAM_MENSAGEM
    push mensagem
    push eax
    call [iat_WriteFile]
    mov esp, ebp
    pop ebp
    ret

    align 0x20, db 0xCC

entrada:                        ; entry point
    call imprime
    push 0
    call [iat_ExitProcess]

codigo_fim:
    times FILE_ALIGN - ($ - $$) db 0

; ---------------------------------------------------------------- .rdata
section rdados
rdados_ini:

import_desc:
    dd RVA(ilt), 0, 0, RVA(nome_dll), RVA(iat)
    times 5 dd 0                ; descritor nulo (fim da lista)
import_desc_fim:

ilt:
    dd RVA(hn_GetStdHandle), RVA(hn_WriteFile), RVA(hn_ExitProcess), 0

iat:
iat_GetStdHandle: dd RVA(hn_GetStdHandle)
iat_WriteFile:    dd RVA(hn_WriteFile)
iat_ExitProcess:  dd RVA(hn_ExitProcess)
    dd 0
iat_fim:

hn_GetStdHandle: dw 0
    db "GetStdHandle", 0
    align 2, db 0
hn_WriteFile: dw 0
    db "WriteFile", 0
    align 2, db 0
hn_ExitProcess: dw 0
    db "ExitProcess", 0
    align 2, db 0

nome_dll: db "KERNEL32.dll", 0

rdados_fim:
    times FILE_ALIGN - ($ - $$) db 0

; ---------------------------------------------------------------- .data
section dados
dados_ini:

mensagem: db "Ola do Windows! Este e um PE32.", 13, 10
TAM_MENSAGEM equ $ - mensagem
escritos: dd 0

dados_fim:
    times FILE_ALIGN - ($ - $$) db 0
