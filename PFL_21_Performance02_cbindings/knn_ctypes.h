#ifndef __KNN_CTYPES
#define __KNN_CTYPES

#ifdef __cplusplus
extern "C" {
#endif

#include <math.h>
#include <malloc.h>
#include <stdio.h>
#include <string.h>

unsigned long get_index_columnorder(int row, int rows, int column, int columns);
unsigned long get_index_roworder(int row, int rows, int column, int columns);
void kNN_particles_ctypes(float* particles, int rows, int columns, int* kNN_indices, double* kNN_distances, float r, int k);

#ifdef __cplusplus
}
#endif
#endif // __KNN_CTYPES