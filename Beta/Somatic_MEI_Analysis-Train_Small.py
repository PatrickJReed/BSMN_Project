#!/usr/bin/python2.7
import glob, os, gc
import os.path
import csv
import numpy as np
from time import time
from subprocess import (call, Popen, PIPE)
from itertools import product
from IPython.display import display
from PIL import Image
from IPython.display import Image as IPImage
import shutil
import re
import xml.etree.ElementTree as ET
import time
import tensorflow as tf
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
from keras import backend as K
from keras.utils import multi_gpu_model
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import matplotlib.pyplot as plt
from keras.utils import plot_model
from keras.models import load_model

# dimensions of our images.
img_width, img_height = 28, 28

train_data_dir = os.path.join(basepath, 'training')
validation_data_dir = os.path.join(basepath, 'testing')
nb_train_samples = 60000
nb_validation_samples = 10000
epochs = 10
batch_size = 16


if K.image_data_format() == 'channels_first':
    input_shape = (1, img_width, img_height)
else:
    input_shape = (img_width, img_height, 1)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(10))
model.add(Activation('sigmoid'))

parallel_model = multi_gpu_model(model, gpus=8)

parallel_model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

parallel_model.summary()
# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(rescale=1./255)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(28, 28),
    color_mode = 'grayscale',
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(28, 28),
    color_mode = 'grayscale',
    batch_size=batch_size,
    class_mode='categorical')

parallel_model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size, verbose=1)

parallel_model.save_weights('first_try_mnist.h5')

scoreSeg = parallel_model.evaluate_generator(validation_generator,10000, workers=8, use_multiprocessing=True)
print("Accuracy = ",scoreSeg[1])

model.save('MNIST_model.h5')

model = load_model('MNIST_model.h5')
plot_model(model, to_file='model.png')
