## Dump internal trees when compiling with g++

C++ type system is very complicated, and together with operators
oeverloading, templating, type definitions and other mechanism it can
make it very difficult to understand what is exactly happening inside
a certain C++ code line. This can make debugging or compilation errors
fixing rather difficult.

Fortunately with `g++` it is possible to dump a lot of useful
information about what the compiler think of each line by dumping the
internal trees used during compilation. Such information is mainly
meant for debugging `g++` itself, so there probably is no guarantee of
uniformity and things can change between different versions of the
compiler. Sill, they can be useful and instructive.

Enable tree dumping by compiling with

    g++ -fdump-tree-all -fdump-tree-all-lineno ...

A lot of files will be generated. To me the most useful are "class",
"original" and "gimple". The "class" tree shows all classes and their
hierarchy. The "gimple" tree is probably the one that makes it easiest
to decode the C++ source line per line. The "original" tree is a bit
more obscure than "gimple", but it contains the template expansions of
return types, which "gimple" does not.

References:

 * https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html

 * https://gcc.gnu.org/onlinedocs/gccint/GIMPLE.html#GIMPLE
