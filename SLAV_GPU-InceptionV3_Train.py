from __future__ import print_function
import glob, os, gc, sys
import os.path
import csv
import numpy as np
np.random.seed(1337)  # for reproducibility
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
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers.normalization import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras import optimizers
from keras.applications.inception_v3 import InceptionV3
from keras.utils import np_utils
from keras import backend as K
from keras.utils import multi_gpu_model
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from keras.layers import Lambda, concatenate
from keras import Model
import tensorflow as tf

##Path to Data
basepath = "/home/ubuntu/efs/SLAV_Data/"


#config = tf.ConfigProto(log_device_placement=True)
#config.gpu_options.allocator_type = 'BFC'
#config.gpu_options.allow_growth = True
#sess = tf.Session(config = config)
#K.set_session(sess)
# dimensions of our images.
img_width, img_height = 512,512

train_data_dir = os.path.join(basepath, 'Train')
validation_data_dir = os.path.join(basepath, 'Validate')
#test_data_dir = os.path.join(basepath, '_Test')
nb_train_samples = 12500
nb_validation_samples = 2500
batch_size = 32

# this is the augmentation configuration we will use for testing:
# only rescaling
train_datagen = ImageDataGenerator(rescale = 1./255, horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale = 1./255, horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(512,512),
    color_mode = 'rgb',
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(512,512),
    color_mode = 'rgb',
    batch_size=batch_size,
    class_mode='categorical')


if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

base_model = InceptionV3(weights='imagenet', include_top=False)


# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(512, activation="relu")(x)
x = Dropout(.2)(x)
# and a logistic layer -- let's say we have 4 classes
predictions = Dense(5, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

for i, layer in enumerate(model.layers):
    print(i, layer.name)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers

for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)

# Save the model according to the conditions  
checkpoint = ModelCheckpoint("slav_incv3.h5", monitor='loss', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='loss', patience=10, verbose=1, mode='auto')


#model.summary()
#model = multi_gpu_model(model,4)
model.compile(optimizer='rmsprop',    
                loss='categorical_crossentropy', 
                metrics=['accuracy'])
# train the model on the new data for a few epochs
history1 = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=20,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size, verbose=1,
    callbacks = [early,checkpoint], shuffle=True)
model.save('inceptionV3_SLAV_4_1.h5')
# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
    print(i, layer.name)


for layer in model.layers[:249]:
      layer.trainable = False
for layer in model.layers[249:]:
      layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
#model = multi_gpu_model(model,4)
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy',metrics=['accuracy'])

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers

history2 = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=20,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size, verbose=1,
    callbacks = [early,checkpoint], shuffle=True)

model.save('inceptionV3_SLAV_4_2.h5')
