import numpy as np

root_path = '/content/drive/MyDrive/othello/'

path = root_path + 'outfile.npz'
with np.load(path) as data:
  examples = data['examples']
  labels = data['labels']

idx = np.random.permutation(len(examples))

examples = examples[idx]
labels = labels[idx]

np.savez(root_path + 'permuted.npz', examples=examples, labels=labels)

