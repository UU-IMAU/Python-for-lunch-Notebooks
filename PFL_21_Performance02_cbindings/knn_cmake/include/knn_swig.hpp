#ifndef __KNN_SWIG_H
#define __KNN_SWIG_H

#include <math.h>
#include <malloc.h>
#include <stdio.h>
#include <string.h>

unsigned long get_index_columnorder(int row, int rows, int column, int columns);
unsigned long get_index_roworder(int row, int rows, int column, int columns);
void kNN_particles_swig(float* particles, int rows, int columns, int* kNN_indices, double* kNN_distances, float r, int k);

#endif
#endif // __KNN_SWIG_H
