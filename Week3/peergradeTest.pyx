cdef int i, j
cdef double s, k

for i in range(500):
	s = 0
	for j in range(1,10001):
		k = 1/(j**2)
		s += k

print(s)
print("done")