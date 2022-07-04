#include "lib.h"

int a()
{
    return b();
    
}

int b()
{
    My_Class m;
    m.my_method();
    return 5;
}

void My_Class::my_method()
{
}
