#include <iostream>

int main() {
    int w0 = 0;
    int w1 = 0;
    int w4 = 1;
    int w2 = 0;
    int w3 = 0;
    goto ad864;
    ad854:
    w0 = w0 + w3;
    std::cout << w0 << std::endl;
    w1 = w1 + 1;
    ad85c:
    w4 = w2;
    w2 = w3;
    ad864:
    w3 = w2 + w4;
    if (w1 % 2 == 0) {
        goto ad854;
    }
    w1 = w1 + 1;
    if (w1 != 0x28) {
        goto ad85c;
    } 
    std::cout << w0 << std::endl;
    return 0;
}
