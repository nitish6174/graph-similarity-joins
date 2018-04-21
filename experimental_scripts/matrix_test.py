"""
To test and compare convergence of 2 ways in which pagerank iterations
can be executed:
Method 1 : Ab, A((A^1)b), A((A^2)b), A((A^3)b), A((A^4)b), A((A^5)b), ....
Method 2 : Ab, (A^1)(A^1)b, (A^2)(A^2)b, (A^4)(A^4)b, (A^8)(A^8)b, ....
"""
import numpy as np


def main():
    n = 100
    b = np.full((n, 1), 1.0/n)
    A = np.random.rand(n, n)
    s = np.sum(A, 0)
    for i in range(n):
        for j in range(n):
            A[i][j] /= s[j]
    print(converge1(A, b))
    print("-" * 10)
    print(converge2(A, b))


def converge1(A, b):
    C1 = np.matmul(A, b)
    C2 = np.matmul(A, C1)
    i = 1
    while not np.allclose(C1, C2):
        C1 = np.matmul(A, C2)
        C2 = np.matmul(A, C1)
        print(i)
        i += 1
    return C2


def converge2(A, b):
    A_p = np.matmul(A, A)
    C1 = np.matmul(A, b)
    C2 = np.matmul(A_p, b)
    i = 1
    while not np.allclose(C1, C2):
        C1 = C2
        A_p = np.matmul(A_p, A_p)
        C2 = np.matmul(A_p, b)
        print(i)
        i += 1
    return C2


if __name__ == '__main__':
    main()
