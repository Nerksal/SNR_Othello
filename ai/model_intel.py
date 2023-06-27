import tensorflow as tf
from tensorflow.keras import datasets, layers, models, Input


import intel_extension_for_tensorflow as ipex

ipex.set_backend("GPU")


import numpy as np

root_path = './'

path = root_path + 'dataset.npz'
with np.load(path) as data:
    print(data.files)
    x_train = data['x_train']
    y_train = data['y_train']

    x_test = data['x_test']
    y_test = data['y_test']

print("x_train: ", x_train.shape)
print("x_test: ", x_test.shape)
print("y_train: ", y_train.shape)
print("y_test: ", y_test.shape)

train_dataset = tf.data.Dataset.from_tensor_slices((
    x_train,
    y_train,
))

val_dataset = tf.data.Dataset.from_tensor_slices((
    x_test,
    y_test,
))

BATCH_SIZE = 64
SHUFFLE_BUFFER_SIZE = 100

train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
val_dataset = val_dataset.batch(BATCH_SIZE)

inputs = Input(shape=(8,8,2), name="input")

hidden = layers.Conv2D( 32, (3, 3), activation='relu', strides=1, padding="same", name="conv2d_1")(inputs)
hidden = layers.Conv2D( 64, (3, 3), activation='relu', strides=1, padding="same", name="conv2d_2")(hidden)
hidden = layers.Conv2D(128, (3, 3), activation='relu', strides=1, padding="same", name="conv2d_3")(hidden)
hidden = layers.Conv2D(256, (3, 3), activation='relu', strides=1, padding="same", name="conv2d_5")(hidden)
hidden = layers.Conv2D(128, (3, 3), activation='relu', strides=1, padding="same", name="conv2d_6")(hidden)
hidden = layers.Conv2D( 64, (3, 3), activation='relu', strides=1, padding="same", name="conv2d_7")(hidden)

flat    = layers.Flatten(name="flatten")(hidden)
flat    = layers.Dense(1024, activation='relu', name="fc_1")(flat)
#flat    = layers.Dense( 512, activation='relu', name="fc_2")(flat)
output  = layers.Dense(  64, activation='softmax', name="output")(flat)

'''
checkpoint_filepath = root_path + 'checkpoint'
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
    monitor='val_loss',
    mode='max',
    save_best_only=True)
'''

opt = tf.keras.optimizers.experimental.RMSprop(learning_rate=0.001)
#opt = tf.keras.optimizers.Adam(learning_rate=0.001)
#metric = tf.keras.metrics.TopKCategoricalAccuracy(k=2, name='top_2')
metric = tf.keras.metrics.CategoricalAccuracy()
#metric = tf.keras.metrics.BinaryAccuracy()
cross = tf.keras.losses.CategoricalCrossentropy(from_logits=False)
#cross = tf.keras.losses.CategoricalCrossentropy()
#cross = tf.keras.losses.BinaryCrossentropy()

model = tf.keras.Model(inputs=inputs, outputs=output)
model.compile(optimizer = opt,
              loss = cross,
              metrics = metric)

model.summary()
with tf.device("/XPU:0"):
    history = model.fit(train_dataset,
                    epochs=10,
                    validation_data=val_dataset)

model.save(root_path + 'model_softmax/')
