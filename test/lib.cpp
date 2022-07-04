#include "lib.h"

void My_Class::my_method()
{ a(66); }

void a(int i)
{
}

void b(My_Class m)
{
    m.my_method();
}
