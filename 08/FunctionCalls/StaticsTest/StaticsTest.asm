(Sys.init)
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@Class1.set$RETURN
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Class1.set$RETURN)
@SP
AM=M-1
D=M
@5
M=D
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
@Class2.set$RETURN
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Class2.set$RETURN)
@SP
AM=M-1
D=M
@5
M=D
@Class1.get$RETURN
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(Class1.get$RETURN)
@Class2.get$RETURN
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(Class2.get$RETURN)
(Sys$WHILE)
@Sys$WHILE
0;JMP
(Class1.set)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@Class1.0
M=D
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@Class1.1
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
AD=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@R15
M=D
@R15
AM=M-1
D=M
@THAT
M=D
@R15
AM=M-1
D=M
@THIS
M=D
@R15
AM=M-1
D=M
@ARG
M=D
@R15
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Class1.get)
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class1.1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
M=0
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
AD=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@R15
M=D
@R15
AM=M-1
D=M
@THAT
M=D
@R15
AM=M-1
D=M
@THIS
M=D
@R15
AM=M-1
D=M
@ARG
M=D
@R15
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Class2.set)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@Class2.0
M=D
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@Class2.1
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
AD=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@R15
M=D
@R15
AM=M-1
D=M
@THAT
M=D
@R15
AM=M-1
D=M
@THIS
M=D
@R15
AM=M-1
D=M
@ARG
M=D
@R15
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Class2.get)
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class2.1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
M=0
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
AD=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@R15
M=D
@R15
AM=M-1
D=M
@THAT
M=D
@R15
AM=M-1
D=M
@THIS
M=D
@R15
AM=M-1
D=M
@ARG
M=D
@R15
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP