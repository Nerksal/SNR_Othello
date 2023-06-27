import numpy as np

root_path = './'

path = root_path + 'dataset/dataset.npz'
with np.load(path) as data:
    print(data.files)
    x_train = data['arr_0']
    y_train = data['arr_1']

    x_test = data['arr_2']
    y_test = data['arr_3']

np.savez('./dataset.npz', x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)

