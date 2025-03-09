// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.
    
    @i
    M=0         // i = 0

    @SCREEN
    D=A
    @address
    M=D

(LOOP)
    @i
    M=0         // reset i pointer
    @SCREEN
    D=A
    @address
    M=D         // reset address pointer
    
    @KBD
    D=M         // check memory for an input
    @FILL
    D;JGT       // goto FILL if input
    @CLEAR
    D;JEQ       // goto CLEAR if no input
    
(FILL)
    @i
    M=M+1       
    @address
    A=M
    M=-1
    @address
    M=M+1
    @i
    D=M
    @8192
    D=D-A
    @LOOP
    D;JEQ
    @FILL
    0;JMP

(CLEAR)

    @i
    M=M+1
    @address
    A=M
    M=0
    @address
    M=M+1
    @i
    D=M
    @8192
    D=D-A
    @LOOP
    D;JEQ
    @CLEAR
    0;JMP






