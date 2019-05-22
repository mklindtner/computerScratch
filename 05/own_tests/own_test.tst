// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/05/CPU.tst

load CPU.hdl,
output-file CPU.out,
compare-to CPU.cmp,
output-list time%S0.4.0 inM%D0.6.0 instruction%B0.16.0 reset%B2.1.2 outM%D1.6.0 writeM%B3.1.3 addressM%D0.5.0 pc%D0.5.0 DRegister[]%D1.6.1;

set instruction %B0000001111101000, // @1000
tick, output, tock, output;

set instruction %B1110111010010000, // D=-1
tick, output, tock, output;

set instruction %B1110001100000001, // D;JGT
tick, output, tock, output;

set instruction %B1110001100000010, // D;JEQ
tick, output, tock, output;

set instruction %B1110001100000011, // D;JGE
tick, output, tock, output;

set instruction %B1110001100000100, // D;JLT
tick, output, tock, output;

set instruction %B1110001100000101, // D;JNE
tick, output, tock, output;

set instruction %B1110001100000110, // D;JLE
tick, output, tock, output;
