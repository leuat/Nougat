#include <QString>
#include <QVector>
#include <QVector3D>
#include <QPointF>
#include <iostream>
#include "GeometryLibrary/distancetoatom.h"
#include "GeometryLibrary/particle.h"
#include "GeometryLibrary/dtalikelihood.h"
#include "GeometryLibrary/likelihood/lgraph.h"

using namespace std;


void Instructions() {
    cout << "Welcome to Nougat 0.1" << endl << endl;
    cout << "Usage: nougat [ command ] { params }" << endl;
    cout << "Exhaustive list of parameters: " << endl<<endl;
    cout << "   dta [ xyz file ] [ output file ]" << endl;

    cout << endl << endl;

}

void quit(QString s) {
    cout << s.toStdString() << endl;
    cout << endl;
    exit(1);
}

void assertParams(int N, int required) {
    if (N!=required) {
        Instructions();
        quit("Incorrect number of parameters");

    }
}



int main(int argc, char *argv[])
{
    if (argc==1) {
        Instructions();
        exit(1);
    }

    bool ok = false;

    if (QString(argv[1]) == QString("dta")) {
        assertParams(4,argc);
        cout << "Ready to DTA baby" << endl;
        Particles p;
        p.open(argv[2]);
        // First, copy particles to single list
        if (p.size()==0)
            quit(QString("Error loading file " + QString(argv[2])));

        QVector<QVector3D> points;
        p.getVector3DList(points);
        DistanceToAtom da(20);

        da.compute(points, 30.0);
        QVector<QPointF> hist = da.histogram(100);
        LGraph g(hist);
        g.SaveText(argv[3]);


        ok = true;
    }

    return 0;
}
