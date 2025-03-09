// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

    @R0
    D=M
    @n
    M=D       // N = R0
    @R1
    D=M
    @i
    M=D       // i = R0
    @mult
    M=0       // mult = 0


(LOOP)
    @i
    D=M
    @STOP
    D;JEQ    // if i=0 goto STOP

    @mult
    D=M
    @R0
    D=D+M
    @mult
    M=D      // mult = mult + mult (i times)
    @i
    M=M-1    // i = i - 1
    @LOOP
    0;JMP

(STOP)
    @mult
    D=M
    @R2
    M=D      // RAM[2] = mult

(END)
    @END
    0;JMP

