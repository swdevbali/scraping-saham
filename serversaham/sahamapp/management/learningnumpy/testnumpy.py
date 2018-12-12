import numpy as np

a = np.array(['A', 'B', 'B', 'A'])
print(a)
print(a.shape)

a = np.zeros((2, 2))
print(a)
print('-'*4)

a = np.ones((2, 2))
print(a)
print('-'*4)

a = np.full ((2, 2), 101)
print(a)
print('-'*4)

a = np.random.random((2, 2))
print(a)
print('-'*4)

#ARITHMETIC
a = np.ones((2, 2))
b = np.ones((2, 2))
c = a + b
print(c)

#PENGURANGAN
d = np.full((2, 2), 4)
e = c - d
print(e)

#PERKALIAN
a = np.full((2, 2), 2)
b = np.full((2, 2), 3)
c = a * b
print(c)

#SLICING
a = np.full((3, 3), 2)
print(a)
print('-'*4)
b = a[:1]
print(b)
print('-'*4)