#include "commandparser.h"


void CommandParser::instructions() {
    cout << "Welcome to Nougat 0.1" << endl << endl;
    cout << "Usage: nougat [ command ] { params }" << endl;
    cout << "Exhaustive list of parameters: " << endl<<endl;
    cout << "   dta [ xyz file ] [ output file ] [ # random vectors ]" << endl;
    cout << "   dta_model [ xyz file ] [ model parameter file] [ output file ] [ #random vectors ] [ seed ]" << endl;

    cout << endl << endl;

}

void CommandParser::quit(QString s) {
    cout << s.toStdString() << endl;
    cout << endl;
    exit(1);
}

void CommandParser::assertParams(int N, int required) {
    if (N!=required) {
        instructions();
        quit("Incorrect number of parameters");

    }
}

bool CommandParser::CalculateDTA()
{
    assertParams(5,m_argc);
    QString particleFilename = m_argv[2];
    QString outFile = m_argv[3];
    int randomDirections = (int)QString(m_argv[4]).toFloat();

    cout << "Ready to DTA baby : " << particleFilename.toStdString() << endl;
    Particles p;
    p.open(particleFilename.toStdString().c_str());
    // First, copy particles to single list
    if (p.size()==0)
        quit(QString("Error loading file " + particleFilename));

    cout << "DTAing " << p.size() << " particles..." << endl;

    QVector<QVector3D> points;
    p.getVector3DList(points);
    DistanceToAtom da(randomDirections);
    da.compute(points, 30.0);
    QVector<QPointF> hist = da.histogram(100);
    LGraph g(hist);
    g.SaveText(outFile.toStdString());

    return true;

}

bool CommandParser::CalculateDTAModel()
{
    assertParams(7,m_argc);
    QString particleFilename = m_argv[2];
    QString modelParameters = m_argv[3];
    QString outFile = m_argv[4];
    int randomDirections = (int)QString(m_argv[5]).toFloat();
    int seed = (int)QString(m_argv[6]).toFloat();
    cout << "Ready to DTA a model baby : " << modelParameters.toStdString() << endl;
    Particles particles;
    QVector<QVector3D> points;
    RegularNoiseModel rm;
    CIniFile cf;
  /*  cout << "Loading parameter file " << modelParameters.toStdString() << endl;
    cf.load(modelParameters.toStdString().c_str());*/
    cout << "Loading model parms" << endl;
    try {
        rm.parameters()->load(modelParameters);
//        rm.loadParameters(&cf);

    } catch (string s) {
        cout << "ERROR loading ini file: " << s << endl;
        exit(1);
    }

    cout << "Setting seed .." << endl;
    rm.parameters()->setValue("seed", seed);
    cout << "Loading particle file.." << endl;
    particles.open(particleFilename.toStdString().c_str());
    // First, copy particles to single list
    if (particles.size()==0)
        quit(QString("Error loading file " + particleFilename));

    cout << "Constraining particles ..." << endl;
    rm.start();
    for (Particle* p: particles.getParticles()) {
        QVector3D pos = p->getPos();
        if (!rm.isInVoid(pos.x(), pos.y(), pos.z()))
            points.append(pos);
    }
    rm.stop();


    cout << "DTAing " << points.size() << " particles..." << endl;

    DistanceToAtom da(randomDirections);
    da.compute(points, 30.0);
    QVector<QPointF> hist = da.histogram(100);
    LGraph g(hist);
    g.SaveText(outFile.toStdString());

    return true;

}



CommandParser::CommandParser(int argc, char *argv[])
{
    // print instructions if no arguments
    if (argc==1) {
        instructions();
        exit(1);
    }
    m_argc = argc;
    m_argv = argv;

    bool ok = false;
    QString command = argv[1];

    if (command == "dta")
        ok = CalculateDTA();

    if (command == "dta_model")
        ok = CalculateDTAModel();

    if (!ok)
        instructions();
}
