@256
D=A
@SP
M=D
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@Loop1
D;JEQ
@SP
A=M
M=0
@Loop1END
0;JMP
(Loop1)
@SP
A=M
M=-1
(Loop1END)
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@Loop2
D;JEQ
@SP
A=M
M=0
@Loop2END
0;JMP
(Loop2)
@SP
A=M
M=-1
(Loop2END)
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@Loop3
D;JEQ
@SP
A=M
M=0
@Loop3END
0;JMP
(Loop3)
@SP
A=M
M=-1
(Loop3END)
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@Loop4
D;JLT
@SP
A=M
M=0
@Loop4END
0;JMP
(Loop4)
@SP
A=M
M=-1
(Loop4END)
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@Loop5
D;JLT
@SP
A=M
M=0
@Loop5END
0;JMP
(Loop5)
@SP
A=M
M=-1
(Loop5END)
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@Loop6
D;JLT
@SP
A=M
M=0
@Loop6END
0;JMP
(Loop6)
@SP
A=M
M=-1
(Loop6END)
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@Loop7
D;JGT
@SP
A=M
M=0
@Loop7END
0;JMP
(Loop7)
@SP
A=M
M=-1
(Loop7END)
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@Loop8
D;JGT
@SP
A=M
M=0
@Loop8END
0;JMP
(Loop8)
@SP
A=M
M=-1
(Loop8END)
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@Loop9
D;JGT
@SP
A=M
M=0
@Loop9END
0;JMP
(Loop9)
@SP
A=M
M=-1
(Loop9END)
@SP
M=M+1
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
D=A
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
M=M+D
@SP
M=M+1
@112
D=A
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
@SP
M=M-1
A=M
D=M
M=M-D
M=M-D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D&M
@SP
M=M+1
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D|M
@SP
M=M+1
@SP
AM=M-1
M=!M
@SP
M=M+1
