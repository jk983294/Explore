```sh
$ ar -t staticlib.a               # display object files contained
$ ar -x staticlib.a               # extract object files contained
```

### notes
in x64, when static lib linked to dynamic lib, the static lib required to be compiled with -fPIC or -mcmodel-large

### link
gcc -o hello hello.c -I /home/hello/include -L /home/hello/lib -lworld

-I /home/hello/include表示将/home/hello/include目录作为第一个寻找头文件的目录，
寻找的顺序是：/home/hello/include-->/usr/include-->/usr/local/include

-L /home/hello/lib表示将/home/hello/lib目录作为第一个寻找库文件的目录，
寻找的顺序是：/home/hello/lib-->/lib-->/usr/lib-->/usr/local/lib

-lworld表示在上面的lib的路径中寻找libworld.so动态库文件，
如果gcc编译选项中加入了“-static”表示寻找libworld.a静态库文件


### add shared lib path with current path

LIBRARY_PATH used for time compile time shared object dependencies finding (.so compile time)

LD_LIBRARY_PATH used for run time shared object dependencies finding (.so execution time)

LIBRARY_PATH="./${LIBRARY_PATH:+:${LIBRARY_PATH}}"; export LIBRARY_PATH;

LD_LIBRARY_PATH="./${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"; export LD_LIBRARY_PATH;
