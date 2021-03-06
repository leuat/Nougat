TEMPLATE = app
LIBS += -L/usr/local/lib -lgsl
INCLUDEPATH += /usr/local/include

CONFIG += console c++11
CONFIG -= app_bundle
#DEFINES += USE_SIMVIZ
SOURCES += \
    GeometryLibrary/likelihood/graphstatistics.cpp \
    GeometryLibrary/likelihood/lgraph.cpp \
    GeometryLibrary/likelihood/likelihood.cpp \
    GeometryLibrary/logger.cpp \
    GeometryLibrary/misc/cutil.cpp \
    GeometryLibrary/misc/util.cpp \
    GeometryLibrary/models/cylindermodel.cpp \
    GeometryLibrary/models/model.cpp \
    GeometryLibrary/models/multifractalmodel.cpp \
    GeometryLibrary/models/octree.cpp \
    GeometryLibrary/models/regularnoisemodel.cpp \
    GeometryLibrary/models/voidmodel.cpp \
    GeometryLibrary/models/xyzmodel.cpp \
    GeometryLibrary/noise.cpp \
    GeometryLibrary/parameters.cpp \
    GeometryLibrary/perlin.cpp \
    GeometryLibrary/simplex.cpp \
    GeometryLibrary/simplexnoise.cpp \
    GeometryLibrary/likelihood/dtalikelihood.cpp \
    GeometryLibrary/particle.cpp \
    nougat.cpp \
    commandparser.cpp \
    GeometryLibrary/misc/distancetoatommap.cpp \
    GeometryLibrary/misc/grid.cpp \
    GeometryLibrary/misc/points.cpp \
    GeometryLibrary/measures/distancetoatom.cpp \
    GeometryLibrary/measures/measure.cpp \
    GeometryLibrary/measures/gofr.cpp \
    GeometryLibrary/measures/neighborlist.cpp \
    GeometryLibrary/measures/poresizedistribution.cpp \
    GeometryLibrary/likelihood/gofrlikelihood.cpp \
    GeometryLibrary/likelihood/particlelikelihood.cpp

HEADERS += \
    GeometryLibrary/likelihood/graphstatistics.h \
    GeometryLibrary/likelihood/lgraph.h \
    GeometryLibrary/likelihood/likelihood.h \
    GeometryLibrary/likelihood/spline.h \
    GeometryLibrary/logger.h \
    GeometryLibrary/misc/cinifile.h \
    GeometryLibrary/misc/cutil.h \
    GeometryLibrary/misc/random.h \
    GeometryLibrary/misc/util.h \
    GeometryLibrary/models/cylindermodel.h \
    GeometryLibrary/models/model.h \
    GeometryLibrary/models/models.h \
    GeometryLibrary/models/multifractalmodel.h \
    GeometryLibrary/models/octree.h \
    GeometryLibrary/models/regularnoisemodel.h \
    GeometryLibrary/models/voidmodel.h \
    GeometryLibrary/models/xyzmodel.h \
    GeometryLibrary/noise.h \
    GeometryLibrary/parameters.h \
    GeometryLibrary/perlin.h \
    GeometryLibrary/simplex.h \
    GeometryLibrary/simplexnoise.h \
    GeometryLibrary/likelihood/dtalikelihood.h \
    GeometryLibrary/particle.h \
    commandparser.h \
    GeometryLibrary/misc/distancetoatommap.h \
    GeometryLibrary/misc/grid.h \
    GeometryLibrary/misc/points.h \
    GeometryLibrary/measures/distancetoatom.h \
    GeometryLibrary/measures/measure.h \
    GeometryLibrary/measures/gofr.h \
    GeometryLibrary/measures/neighborlist.h \
    GeometryLibrary/measures/poresizedistribution.h \
    GeometryLibrary/likelihood/gofrlikelihood.h \
    GeometryLibrary/likelihood/particlelikelihood.h
