from tensorflow import keras
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
maxi = 7
fig, ax = plt.subplots(2,maxi)
for i in range(0,maxi,1):
    boards = examples[i]
    boards.shape = (1, 8, 8, 2)

    move = labels[i]

    model = keras.models.load_model('./model/')
    pred = model.predict(boards)

    z = np.array(pred)
    z.shape = (2,8)

    matrix = np.outer(z[0], z[1])

    a = np.argmax(z, axis=1)
    
    black = boards[0,:,:,0]*64
    white = boards[0,:,:,1]*16

    black[move[0], move[1]] = 255
    true_matrix = np.add(black, white)

    ax[0, i].matshow(true_matrix, cmap=plt.cm.Reds)
    ax[1, i].matshow(matrix, cmap=plt.cm.Blues)


plt.show()
