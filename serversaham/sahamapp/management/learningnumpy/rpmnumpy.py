import numpy as np

# Init
a = np.array(['A', 'B', 'B', 'A'])

print(a)
print(a.shape)
print('-'*4)

a = np.zeros((2,2))
print(a)
print('-'*4)

a = np.ones((2,2))
print(a)
print('-'*4)

a = np.random.random((2,2))
print(a)
print('-'*4)

a = np.full((2,2),101)
print(a)
print('-'*4)

# penjumlahan
a = np.ones((2,2))
b = np.ones((2,2))
c = a + b
print(c)
print('-'*4)

# perkalian
a = np.full((2,2),2)
b = np.full((2,2),3)
c = a * b
print(c)
print('-'*4)