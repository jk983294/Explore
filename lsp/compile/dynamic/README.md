### visibility

by default, gcc will expose all dynamic link symbols

```sh
$ nm -D libdynamiclib.so               # display all exported symbols in object files
```

| means        | scope   |  option description  |
| :----:   | :----:  | :----:  |
| -fvisibility=hidden -fvisibility-inlines-hidden     | all code | |
| \__attribute__ ((visibility("hidden,default")))   |   decorate function, affect one symbol   | |
| #pragma GCC visibility [push,pop]  |    in header, affect header's symbols    | push is hidden |
| -W1,--version-script,[script]    |    all    | later |


### locate dynamic lib

dynamic library filename = lib + &lt;library name&gt; + .so + &lt;library version information&gt;

library version information = &lt;major&gt;.&lt;minor&gt;.&lt;patch&gt;

library soname = lib + &lt;library name&gt; + .so + &lt;major version&gt;

like libz.so.1.2.3.4, its soname is libz.so.1

#### preload

/etc/ld.so.preload

export LD_PRELOAD=/home/kun/lib/liba.so:$LD_PRELOAD

export LD_RUN_PATH=/home/kun/libs/:$LD_RUN_PATH

#### runpath

gcc -Wl,-R/home/kun/libs/ -Wl,--enable-new-dtags -lworld

write into binary file DT_RUNPATH field in elf header

#### ldconfig cache

cat /etc/ld.so.conf

ls -alg /etc/ld.so.conf.d/

cat /etc/ld.so.cache

### link

one shot compile and link

gcc -fPIC main.cpp -Wl,-L../sharedLib -Wl,-lworld -o demo

gcc -o hello hello.c -I/home/hello/include -L/home/hello/lib -lworld

-I /home/hello/include表示将/home/hello/include目录作为第一个寻找头文件的目录，
寻找的顺序是：/home/hello/include-->/usr/include-->/usr/local/include

-L /home/hello/lib表示将/home/hello/lib目录作为第一个寻找库文件的目录，
寻找的顺序是：/home/hello/lib-->/lib-->/usr/lib-->/usr/local/lib

-lworld表示在上面的lib的路径中寻找libworld.so动态库文件，
如果gcc编译选项中加入了“-static”表示寻找libworld.a静态库文件

### duplicate symbol

if several dynamic libs have duplicate symbol, then pick one lib's symbol to link.

actually when dynamic loading, symbol won't get duplicated because dlopen() will translate symbol to unique symbol name.

weak symbols in object file, this means that when the linker produces the final executable program, it can throw away all but one of these duplicate definitions

#### priority to link:

1) client code symbol

2) dynamic lib exported symbol

3) invisible symbol, removed symbol

### version control

```sh
$ gcc -shared <inputs> -l:libxyz.so.1 -o <clientBinary>         # compile with main version
$ gcc -shared <inputs> -Wl,-soname,<soname> -o <clientBinary>   # compile embed with soname info
```

soname will be record in lib binary and client binary, so it can check if they match to some extent
