import numpy as np



with open('data.npy', 'rb') as f:
    a = np.load(f, allow_pickle=True)

print(a[1][1])
print(a.shape)
