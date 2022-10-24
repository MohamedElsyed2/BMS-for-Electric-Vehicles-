
#include<stdio.h>
#include <stdint.h>
int main()
{
    char result[50];
    uint16_t num = 1560;
    sprintf(result, "%u", num);
    printf("\n The string for the num is %s", result);
    return 0;
}