#include <iostream>
#include <cstdlib>

int main() {
    const char* hexString = "0xFF";
    long hexValue = std::strtol(hexString, nullptr, 0);
    
    std::cout << "Hex value: " << std::hex << hexValue << std::endl;

    return 0;
}