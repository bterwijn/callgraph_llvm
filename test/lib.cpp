#include "lib.h"

void X::my_method()
{ a(66); }

void a(int i)
{
}

void b(X x)
{
    x.my_method();
}
