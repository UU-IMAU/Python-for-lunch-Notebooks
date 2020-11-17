#include "knn_swig.hpp"

unsigned long get_index_columnorder(int row, int rows, int column, int columns) {
    return (row*columns)+column;
}

unsigned long get_index_roworder(int row, int rows, int column, int columns) {
    return (column*rows)+row;
}

void kNN_particles_swig(float* particles, int rows, int columns, int* kNN_indices, double* kNN_distances, float r, int k) {
    int N = rows;
    double dx, dy, dv_len_sqr, m, l;
    double* distance_matrix = (double*)malloc(sizeof(double)*rows*rows);
    memset(distance_matrix, (double)r, sizeof(double)*rows*rows);
    for(int i=0; i<N; i++) {
        for(int j=i; j<N; j++) {
            if(i==j) {
                distance_matrix[get_index_columnorder(i,N,j,N)] = 0.0;
                continue;
            }
            dx = particles[get_index_columnorder(i, N, 0, 3)]-particles[get_index_columnorder(j, N, 0, 3)];
            dy = particles[get_index_columnorder(i, N, 1, 3)]-particles[get_index_columnorder(j, N, 1, 3)];
            dv_len_sqr = dx*dx+dy*dy;
            distance_matrix[get_index_columnorder(i,N,j,N)] = dv_len_sqr;
            distance_matrix[get_index_columnorder(j,N,i,N)] = dv_len_sqr;
        }
    }

    for(int i=0; i<N; i++) {
        for(int j=i; j<N; j++) {
            if(i==j) {
                continue;
            }
            m = 0;
            while((m<k) && ((kNN_indices[get_index_columnorder(i, N, m, k)] < 0) || (kNN_distances[get_index_columnorder(i, N, m, k)] <= distance_matrix[get_index_columnorder(i, N, j, N)]))) {
                m++;
            }
            if(m >= k) {
                continue;
            }
            l = k-1;
            while(l>m) {
                kNN_indices[get_index_columnorder(i, N, l, k)] = kNN_indices[get_index_columnorder(i, N, l-1, k)];
                kNN_distances[get_index_columnorder(i, N, l, k)] = kNN_distances[get_index_columnorder(i, N, l-1, k)];
            }
            kNN_indices[get_index_columnorder(i, N, m, k)] = j;
            kNN_distances[get_index_columnorder(i, N, m, k)] = distance_matrix[get_index_columnorder(i, N, j, N)];
        }
    }


    free(distance_matrix);
    return;
}
