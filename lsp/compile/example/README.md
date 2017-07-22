# Compile

---

## 1. compile steps

### 1.1 preprocess
1. #include
2. #define
3. macro substitution
4. conditional handle #if #elif #endif
```sh
$ g++ -E -P function.c -o function.i
```

### 1.2 parse
1. lexical analysis
2. syntax analysis
3. meaning analysis

### 1.3 assembly
it support two assembly format: (1) AT&T (2) Intel
```sh
$ g++ -S -masm=att function.c -o function.s
$ g++ -S -masm=intel function.c -o function.s
```

### 1.4 optimization
remove unnecessary code

### 1.5 object file generation

generate binary object file, follow ELF format

basic components in object file: 1) symbol 2) section

symbol contains memory address and memory data

section contains .text .data .bss etc

```sh
$ g++ -c function.c -o function.o
$ g++ -c main.c -o main.o
```

### 1.6 link

static compiling means that executable doesn't contains any dynamic link dependency

```sh
$ g++ function.o main.o -o main
$ g++ -static function.o main.o -o main_static
```

disassembly
```sh
$ objdump -D function.o
$ objdump -D -M intel function.o
$ objdump -D -M intel main.o
$ objdump -D -M intel main
$ objdump -x -j .bss main               # disassembly bss section to find global variable address
```

### 1.7 load

load sections into segments based on access attribute (R, W, RW, RO)

locate PT_INTERP segment for dynamic loading

then locate segment header information, reserve enough space for each segment

then load corresponding page when needed (page fault signal)

run sequence: 1) _start 2) __libc_start_main 3) main()

```sh
$ readelf --segments main               # show segments of an elf
```

## 2. Topics

### 2.1 function call convention

calling convention is an implementation-level scheme for how subroutines receive parameters from their caller
and how they return a result

| call convention        | stack sequence   |  who clear stack  | registers | function call encode |
| :----:   | :----:  | :----:  | :----:  | :----:  |
| __cdecl     | from right to left |   caller     |  | '_' prefix |
| __stdcall   |   from right to left   |   callee   |   | '_' prefix, @ suffix + parameters byte number |
| __fastcall  |    from right to left    |  callee  |  ECX, EDX (MS), EAX, ECX, EDX (Borland)  | '@' prefix, '@' suffix + parameters byte number |
| thiscall    |    from right to left    |  callee  |  ECX (this)  | C++ compiler related encoding algorithm |


### 2.2 static vs dynamic

#### static library:

package several object files into one binary file, binary level reuse

when compiled, we need static library and its header files for compiling

when linking, it won't drag all library in, it will only drag necessary object files in

#### dynamic library:

runtime level reuse, no need to recompile and link object files

share .text but not data sections, so basically share read-only sections but not write sections

PIC (position independent code), the dynamic library only need to be loaded once,
then other application can use it as well

build dynamic library is basically the same with building executable (compile and link),
the only missing part is startup routines which can let library run itself

when link to dynamic library, linker only check if all unresolved symbols can get found in dynamic library
only when loading phase, the dynamic library will be integrated with executable

when link, it will drag whole library in
