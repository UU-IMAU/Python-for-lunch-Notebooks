%module knn_swig_py

// Add necessary symbols to generated header
%{
#define SWIG_FILE_WITH_INIT
#include <Python.h>
#include <knn_swig.hpp>
%}

%include "stdint.i"
%include "std_string.i"
%include "typemap.i"
%include "numpy.i"

%ignore ""; // ignore all
%define %unignore %rename("%s") %enddef

%unignore kNN_particles_ctypes(float* particles, int rows, int columns, int* kNN_indices, double* kNN_distances, float r, int k);

// Process symbols in header
%include "knn_swig.hpp"

%unignore ""; // unignore all
