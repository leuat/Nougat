#ifndef COMMANDPARSER_H
#define COMMANDPARSER_H
#include <QString>
#include <QVector>
#include <QVector3D>
#include <QPointF>
#include <QDebug>
#include <iostream>
#include "GeometryLibrary/distancetoatom.h"
#include "GeometryLibrary/particle.h"
#include "GeometryLibrary/dtalikelihood.h"
#include "GeometryLibrary/likelihood/lgraph.h"
#include "GeometryLibrary/models/regularnoisemodel.h"
using namespace std;




class CommandParser
{
private:
    int m_argc;
    char** m_argv;
public:
    CommandParser(int argc, char *argv[]);

    void instructions();
    void quit(QString s);
    void assertParams(int N, int required);

    // All methods

    bool CalculateDTA();
    bool CalculateDTAModel();
    bool DTAMapXYZ();
    bool FullLikelihood();
    bool Likelihood1D();


};

#endif // COMMANDPARSER_H
