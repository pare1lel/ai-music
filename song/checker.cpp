#include <iostream>
#include <cstdlib>
#include <cmath>
#include <windows.h>
#include <fstream>
#include <string>
#include <cassert>

using namespace std;

int main(int argc, char** argv) {
    float A4 = 440.0f;
    float ratio = pow(2, 1.0 / 12);
    float C4 = A4 / pow(ratio, 9);
    float totalTime = 0;
    ifstream in;
    in.open(string(argv[1]), ios::in);
    assert(in.is_open());
    while(!in.eof()) {
        int pitch;
        float time;
        in >> pitch >> time;
        cerr << pitch << " " << time << endl;
        totalTime += time;
        if(pitch == 99)
            Beep(1, time * 600);
        else
            Beep(C4 * pow(ratio, pitch), time * 600);
    } 
    assert(totalTime == 16.0f);
    return 0;
}