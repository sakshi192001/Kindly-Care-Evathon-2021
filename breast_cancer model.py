
from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers, callbacks
import warnings
import pickle
warnings.filterwarnings("ignore")
from keras.models import load_model

IMAGE_SIZE = [224, 224]

train_path = '/breast_cancer/train'
valid_path = '/breast_cancer/test'

vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)


for layer in vgg.layers:
    layer.trainable = False

folders = glob('breast_cancer/train/*')
  


x = Flatten()(vgg.output)
prediction = Dense(len(folders), activation='softmax')(x)


model = Model(inputs=vgg.input, outputs=prediction)

model.summary()

model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)


from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('breast_cancer/train/',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('breast_cancer/test/',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')


# fit the model
r = model.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=17,
  #callbacks=[early_stopping],
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

model1=model.save('breast_cancer.h5')
