#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        printf("Usage: openmp_worker.exe <matrix_size> <threads>\n");
        return 1;
    }

    int n = atoi(argv[1]);
    int threads = atoi(argv[2]);

    omp_set_num_threads(threads);

    double *A = malloc((size_t)n * n * sizeof(double));
    double *B = malloc((size_t)n * n * sizeof(double));
    double *C = calloc((size_t)n * n, sizeof(double));

    if (A == NULL || B == NULL || C == NULL)
    {
        printf("Memory allocation failed\n");

        free(A);
        free(B);
        free(C);

        return 1;
    }

    /* Initialize matrices */
    for (int i = 0; i < n * n; i++)
    {
        A[i] = 1.0;
        B[i] = 2.0;
    }

    /* Parallel matrix multiplication */
    double start = omp_get_wtime();

    #pragma omp parallel for
    for (int i = 0; i < n; i++)
    {
        for (int k = 0; k < n; k++)
        {
            double value = A[i * n + k];

            for (int j = 0; j < n; j++)
            {
                C[i * n + j] += value * B[k * n + j];
            }
        }
    }

    double end = omp_get_wtime();

    double execution_time = end - start;

    printf("WORKLOAD=Matrix Multiplication\n");
    printf("SIZE=%d\n", n);
    printf("THREADS=%d\n", threads);
    printf("EXECUTION_TIME=%.6f\n", execution_time);
    printf("RESULT_SAMPLE=%.2f\n", C[0]);

    free(A);
    free(B);
    free(C);

    return 0;
}