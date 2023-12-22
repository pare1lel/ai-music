#include <iostream>
#include <fstream>
#include <cassert>
#include <string>

using namespace std;

int a[65];

int main(int argc, char** argv) {
    ifstream in;
    ofstream out;
    in.open(argv[1], ios::in);
    out.open("converted_" + string(argv[1]), ios::out);
    assert(in.is_open());
    int tot = 0;
    
    while(!in.eof()) {
        int pitch;
        float time;
        in >> pitch >> time;
        cerr << pitch << " " << time << endl;
        int cnt = time * 4;
        if(pitch == 99) {
            for(int i = 1; i <= cnt; i++)
                a[++tot] = 0;
        } else {
            int newPitch = pitch + 60;
            assert(newPitch >= 53 && newPitch <= 79);
            for(int i = 1; i <= cnt; i++)
                a[++tot] = newPitch;
        }   
    } 
    assert(tot == 64);
    for(int i = 1; i <= tot; i++)
        out << a[i] << " ";
    return 0;
}