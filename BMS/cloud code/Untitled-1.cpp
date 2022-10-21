#include <iostream>
#include <string>
 
int main()
{
    char c  = 'fan';
 
    // using string class fill constructor
 
    std::string s(1, c);
    std::cout << s << std::endl;
 
    return 0;
}