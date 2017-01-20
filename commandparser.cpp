#include "commandparser.h"
#include "GeometryLibrary/misc/random.h"
#include "GeometryLibrary/likelihood/particlelikelihood.h"
#include "GeometryLibrary/likelihood/gofrlikelihood.h"

void CommandParser::instructions() {
    cout << "Welcome to Nougat 0.1" << endl << endl;
    cout << "Usage: nougat [ command ] { params }" << endl;
    cout << "Exhaustive list of parameters: " << endl<<endl;
    cout << "   dta [ xyz file ] [ output file ] [ # random vectors ]" << endl;
    cout << "   dta_model [ xyz file ] [ model parameter file] [ output file ] [ #random vectors ] [ seed ]" << endl;
    cout << "   likelihood [ xyz data file ] [ bulk data ] [ model parameter file] [ output likelihood file ] [ no steps ] [ no vectors ]" << endl;
    cout << "   brute1d [ xyz data file ] [ bulk data ]  [ model parameter file] [ output likelihood file ] [ no bins ] [ no vectors ] [ parameter ]" << endl;


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
    p.appendToQVector3DList(points);
    DistanceToAtom da;
    da.setNumberOfRandomVectors(randomDirections);
    da.setCutoff(30);
    da.compute(points);
    QVector<QPointF> hist = da.histogram(100);
    LGraph g(hist);
    g.normalizeArea();
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
    try {
        rm.parameters()->load(modelParameters);
//        rm.loadParameters(&cf);

    } catch (string s) {
        cout << "ERROR loading ini file: " << s << endl;
        exit(1);
    }

    rm.parameters()->setValue("seed", seed);
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

    DistanceToAtom da;
    da.setNumberOfRandomVectors(randomDirections);
    da.setCutoff(30);
    da.compute(points);
    QVector<QPointF> hist = da.histogram(100);
    LGraph g(hist);
    g.normalizeArea();
    g.SaveText(outFile.toStdString());

    return true;

}

bool CommandParser::DTAMapXYZ() {
/*#include "GeometryLibrary/misc/distancetoatommap.h"
#include "GeometryLibrary/misc/points.h"

QString xyz_filename = QString("/Users/anderhaf/Dropbox/uio/phd/2016/noisegeometry/states/sio2_100_systems_255katoms/system0.xyz");
QString vtk_filename = QString("/Users/anderhaf/Dropbox/uio/phd/2016/noisegeometry/states/sio2_100_systems_255katoms/system0.vtk");
Points p;
p.readXYZ(filename);

DistanceToAtomMap map(64, 64, 64);
map.build(p.points(), 15);
map.grid().toVTKFile(vtk_filename, p.systemSize());   */
    return true;
}

bool CommandParser::Likelihood1D() {
    assertParams(10,m_argc);
    QString measure = m_argv[2];

    QString dataParticleFilename = m_argv[3];
    QString bulkParticleFilename = m_argv[4];
    QString modelFile = m_argv[5];
    QString outFile = m_argv[6];
    int noSteps = (int)QString(m_argv[7]).toFloat();
    int noVectors = (int)QString(m_argv[8]).toFloat();
    QString parameter = m_argv[9];

    Random::randomSeed();

    ParticleLikelihood* likelihood;

    if (measure=="dta") {
        DTALikelihood* l = new DTALikelihood();
        likelihood = dynamic_cast<ParticleLikelihood*>(l);
        l->setNumberOfRandomVectors(noVectors);
    }
    else
    if (measure=="gofr") {
        GOfRLikelihood* l = new GOfRLikelihood();
        likelihood = dynamic_cast<ParticleLikelihood*>(l);
        //l->setNumberOfRandomVectors(noVectors);
    }
    else {
        qDebug() << "ERROR: Must supply either dta or gofr measure!";
        exit(1);
    }
//    likelihood.setDebug(true);
    likelihood->setLikelihoodFileName(outFile);

    Particles dataParticles, bulkParticles;
    qDebug() << "Loading particles..";
    dataParticles.open(dataParticleFilename.toStdString().c_str());
    bulkParticles.open(bulkParticleFilename.toStdString().c_str());

    likelihood->setDataInput(&dataParticles);
    likelihood->setOriginalInput(&bulkParticles);
    qDebug() << bulkParticles.size();
    RegularNoiseModel model;
//    CIniFile params;
    qDebug() << "Loading parameters..";
    model.parameters()->load(modelFile.toStdString().c_str());
    qDebug() << "Setting up..";
    //likelihood.monteCarlo(&model, noSteps, Likelihood::AnalysisAlgorithm::FullMonteCarlo);
    likelihood->bruteForce1D(noSteps, parameter, &model);

    qDebug() << "Starting loop!";

    while (likelihood->getDone()==false)
        likelihood->tick();

    likelihood->likelihood().SaveText(QString("chisq_" + outFile).toStdString().c_str());
    likelihood->likelihood().LikelihoodFromChisq();
    likelihood->likelihood().SaveText(outFile.toStdString().c_str());
    return true;


}


bool CommandParser::FullLikelihood()
{
    assertParams(9,m_argc);
    QString measure = m_argv[2];
    QString dataParticleFilename = m_argv[3];
    QString bulkParticleFilename = m_argv[4];
    QString modelFile = m_argv[5];
    QString outFile = m_argv[6];
    int noSteps = (int)QString(m_argv[7]).toFloat();
    int noVectors = (int)QString(m_argv[8]).toFloat();
    Random::randomSeed();

    ParticleLikelihood* likelihood;

    if (measure=="dta") {
        DTALikelihood* l = new DTALikelihood();
        likelihood = dynamic_cast<ParticleLikelihood*>(l);
        l->setNumberOfRandomVectors(noVectors);
    }
    else
    if (measure=="gofr") {
        GOfRLikelihood* l = new GOfRLikelihood();
        likelihood = dynamic_cast<ParticleLikelihood*>(l);
        //l->setNumberOfRandomVectors(noVectors);
    }
    else {
        qDebug() << "ERROR: Must supply either dta or gofr measure!";
        exit(1);
    }

    likelihood->setLikelihoodFileName(outFile);

    qDebug() << "Initialize for " << noVectors << " vectors...";

    Particles dataParticles, bulkParticles;
    qDebug() << "Loading particles..";
    dataParticles.open(dataParticleFilename.toStdString().c_str());
    bulkParticles.open(bulkParticleFilename.toStdString().c_str());

    likelihood->setDataInput(&dataParticles);
    likelihood->setOriginalInput(&bulkParticles);

    qDebug() << bulkParticles.size();
    RegularNoiseModel model;

    qDebug() << "Loading parameters..";
    model.parameters()->load(modelFile.toStdString().c_str());
    qDebug() << "Setting up..";
    likelihood->monteCarlo(&model, noSteps, Likelihood::AnalysisAlgorithm::FullMonteCarlo);
    qDebug() << "Starting loop!";
    while (likelihood->getDone()==false)
        likelihood->tick();

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

    if (command == "likelihood")
        ok = FullLikelihood();

    if (command == "brute1d")
        ok = Likelihood1D();

    if (command == "create_octree") {

    }

    if (!ok)
        instructions();
}
