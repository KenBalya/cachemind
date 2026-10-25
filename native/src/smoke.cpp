#include <array>
#include <iostream>
#include <span>

using namespace std;

int checksum(span<const int> values) {
    int total = 0;

    for (int value : values) {
        total += value;
    }

    return total;
}

int main() {
    constexpr array<int, 5> values{1, 2, 3, 4, 5};

    constexpr int expected = 15;

    const int actual = checksum(values);

    if (actual != expected) {
        cerr << "CacheMind C++20 smoke test failed" << '\n';
        return 1;
    }

    cout << "CacheMind native C++20 smoke: PASS" << '\n';
    cout << "Checksum: " << actual << '\n';

    return 0;
}