import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.double
ctypedef np.double_t DTYPE_t

@cython.boundscheck(False)
def jkmean(np.ndarray[DTYPE_t, ndim=1] x):
  cdef unsigned int N = x.size
  cdef double nn = 1.0/(N-1.0)
  cdef double allsum
  cdef unsigned int i
  cdef np.ndarray[DTYPE_t, ndim=1] samples = np.zeros(N, dtype=DTYPE)
  cdef DTYPE_t mu, sigma
  
  allsum = np.sum(x)
  samples = samples + allsum
  samples = (samples - x)*nn
  
  mu = np.mean(samples)
  sigma = np.sqrt(N-1)*np.std(samples)
  return (mu, sigma)

@cython.boundscheck(False)
def xcov4(np.ndarray[DTYPE_t, ndim=1] a, np.ndarray[DTYPE_t, ndim=1] b, unsigned int L=200):
  cdef unsigned int N = a.size
  cdef unsigned int LL = 2*L + 1
  cdef int i
  
  cdef np.ndarray[DTYPE_t, ndim=1] am = a - a.mean()
  cdef np.ndarray[DTYPE_t, ndim=1] bm = b - b.mean()
  cdef np.ndarray[DTYPE_t, ndim=1] c = np.zeros(LL, dtype=DTYPE)
  cdef np.ndarray[DTYPE_t, ndim=1] s = np.zeros(LL, dtype=DTYPE)
  
  for i in range(-L, 0):
    c[<unsigned int>(i+L)], s[<unsigned int>(i+L)] = jkmean(am[0:N+i]*bm[<unsigned int>(-i):N])
  
  c[L], s[L] = jkmean(am*bm)
  
  for i in range(1, L+1):
    c[i+L], s[i+L] = jkmean(am[i:N]*bm[0:<unsigned int>(N-i)])
  
  return (c, s)

@cython.boundscheck(False)
def xcov3(np.ndarray[DTYPE_t, ndim=1] a, np.ndarray[DTYPE_t, ndim=1] b, unsigned int L=200):
  cdef unsigned int N = a.size
  cdef unsigned int LL = 2*L + 1
  cdef int i
  
  cdef np.ndarray[DTYPE_t, ndim=1] am = a - a.mean()
  cdef np.ndarray[DTYPE_t, ndim=1] bm = b - b.mean()
  cdef np.ndarray[DTYPE_t, ndim=1] c = np.zeros(LL, dtype=DTYPE)
  
  for i in range(-L, 0):
    c[<unsigned int>(i+L)] = np.dot(am[0:<unsigned int>(N+i)], bm[<unsigned int>(-i):N])/(N+i)
  
  c[L] = np.dot(am, bm)/N
  
  for i in range(1, L+1):
    c[<unsigned int>(i+L)] = np.dot(am[<unsigned int>(i):N], bm[0:<unsigned int>(N-i)])/(N-i)
  
  return c
