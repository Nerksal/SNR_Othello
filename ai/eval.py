import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter Matplotlib Demo')
        self.protocol("WM_DELETE_WINDOW", self.__quit)

        self.model = keras.models.load_model('./models/model_softmax3')


        path = './dataset.npz'
        with np.load(path) as data:
            self.examples = data['x_test']
            self.labels = data['y_test']

        self.idx = 0
        self.cnt = 6


        fg, self.ax = plt.subplots(3, self.cnt)
        self.canvas = FigureCanvasTkAgg(fg, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
 

        self.__update_charts()

        button = tk.Button(master=self, text="Quit", command=self.__quit)
        button.pack(side=tk.BOTTOM)

        btn = tk.Button(master=self, text="Next", command=self.__next)
        btn.pack(side=tk.BOTTOM)


    def __quit(self):
        self.quit()
        self.destroy()

    def __next(self):
        self.idx += 1
        self.__update_charts()

    def __update_charts(self):
        start = self.idx * self.cnt
        stop = start + self.cnt
        boards = self.examples[start:stop]
        t_move = self.labels[start:stop]
        predict = self.model.predict(boards)

        for i in range(0, self.cnt):
            black = boards[i,:,:,0]*64
            white = boards[i,:,:,1]*16
            
            #black[t_move[i, 0], t_move[i, 1]] = 255
            true_matrix = np.add(black, white)
            self.ax[0, i].clear()
            self.ax[0, i].imshow(true_matrix, cmap=plt.cm.Greys)
            #self.ax[0, i].matshow(true_matrix, cmap=plt.cm.Spectral)

            predict_matrix = np.reshape(predict[i], (8,8))
            self.ax[1, i].clear()
            self.ax[1, i].imshow(predict_matrix, cmap=plt.cm.Blues)

            #posible = np.reshape(np.ceil(t_move[i]), (8,8))
            #posible = np.multiply(predict_matrix, posible)
            posible = np.reshape(t_move[i], (8,8))
            self.ax[2, i].clear()
            self.ax[2, i].imshow(posible, cmap=plt.cm.Greens)

        self.canvas.draw()

if __name__ == '__main__':
    app = App()
    app.mainloop()
