#!/bin/bash
# Gera os binários usados nos exercícios 1 a 3 e copia para o dojo.
set -e
cd "$(dirname "$0")"
DOJO=../..

nasm -f bin programa.asm -o programa.exe
nasm -f elf32 alvo.asm -o alvo.o
ld -m elf_i386 alvo.o -o alvo

cp programa.exe "$DOJO"/exercicio-1/pe-cabecalho/
cp programa.exe "$DOJO"/exercicio-2/pe-entry-point/
cp alvo "$DOJO"/exercicio-3/elf-cabecalho/
