def fun_fast():
    cdef float result, i
    cdef int a, amax, imax

    a = 0
    amax = 500
    imax = 10000
    while a < amax:
        a = a + 1
        result = 0.0
        i = 0
        while i < imax:
            i = i + 1
            result = result + 1/(i**2)
