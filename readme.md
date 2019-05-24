# Introduction
The purpose of this course is to build a full-scale computer, from the very bottom of computing to the a high-level OOP language, the name of the course is [nand2tetris](https://nand2tetris.org) and was solved using the [book](https://www.nand2tetris.org/book), [forum](http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/) and [videos](https://www.youtube.com/watch?v=KBTg0ju4rxM&list=PLrDd_kMiAuNmllp9vuPqCuttC1XL9VyVh&index=1). Below is an depicting each step in the process, notice that each step is merely an abstracting, each time becoming more readable. 
I choose not to implement the last chapter about Operation System (12). Project 9 also do not have a mention as it's simply learning the jack langauge.

![alt text](https://github.com/mklindtner/computerScratch/blob/master/pictures/overview_simple.png)

Each asbtraction goes through a chapter, however a chapter might present the next abstraction before asking to build it. Here is an overview w. appropriate chapter.

![overview-chapters](https://github.com/mklindtner/computerScratch/blob/master/pictures/overview_detailed.png).


## Tools, Emulators and OS
- all Tools used for testing can be found under [here](https://www.nand2tetris.org/software). Which also provides a guide on how to dl it. Personally I used Linux while going through the course. Indescrepencies might occur if trying to use test my software on other OS like Windows. It should compile fine but Windows might add unexpected spaces when using things like textcomparer. 

## Testing
- each chapter comes with premade tests, once all tests are passed within a chapter it's considered finished.
- an input file is delivered into a given emulator or tool, then a test file is added and the given emulator will run a comparision alerting of any unexpected behvaior.

## project 01-05: computer architecture
 - emulators
     - uses the hardwaresimulator and the CPU emulator
     
 - hdl language
    - a language for running chips on software, is used to simulate proper connection of chips
 
 - uses the tool "Digital"
    - pictures displaying the wiring logic of some chips.
    - all chips are made in the hdl language, but Digital allows for a better mental image.
    - drawins for the respective chapter can be found under "digital-drawings" in said chapter

## project 06: Assembler-Hack
 - emulators
    - uses the assembler (simulator), takes an input (assembler code) and compares it with a test
    - uses the textcomparer
 - Overview
    - The folder "Assembler" consists of the solution for the chapter (my code)
    - The other 4 folders are program-examples that can be given as input to the Parser(inside the Assembler folder)
    


## project 07-08: VM-Assembler
 - emulators
   - uses the VMemulator
 - Overview
   - the folder "VMTranslator" consists of the solution for the chapter (my code)
       
 - note
    - a directory must containt a Sys.vm file otherwise it'll fail
    - if you wish to test files that does not have this, add the OS folders to the folder for translator to work.
    
 
## project 10-11: Jack Compiler
 - emulators
    - uses the JackCompiler
    - uses the textcomparer when going through chapter 10 (XML)
  - overview
    - the folder "JackCompiler" consists of the solution for the chapter (my code)
    - using the terminal line call ``` "python3.5 dest/to/jackcompiler/jackcompiler.py input/input.jack" ```


book: *link to book here / *www.nand2tetris.org

TODO:

create gitignore and remove wierd pycharm stuff
chap 6-7-8-10-11
make "OS" folder

***make .gitignore file) make readme --> each proj, what it's about, what i did) fix compiler 10/11 to work on remote dirs




    

