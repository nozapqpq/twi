# coding: utf-8 
import os
import csv
import keras
import numpy as np
from keras.metrics import Precision, Recall
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout
from keras.optimizers import Adamax
from keras.layers.normalization import BatchNormalization

class model():
    def __init__(self, input_list=[], output_list=[]):
        self.x_np = np.array(input_list)
        self.y_np = np.array(output_list)
        if len(self.x_np) > 0 and len(self.y_np) > 0:
            self.set_parameters()
            self.set_model()

    def set_parameters(self):
        out_sum = self.y_np.sum(axis=0)
        pos = out_sum[0]
        neg = out_sum[1]
        self.output_bias = keras.initializers.Constant(np.log([pos/neg]))
        self.class_weight = {1: (1/neg)*(pos+neg)/2.0, 0: (1/pos)*(pos+neg)/2.0}

    def set_model(self):
        input_dim = len(self.x_np[0])
        output_dim = len(self.y_np[0])
        print([input_dim, output_dim])
        model = Sequential()
        optimizer = Adamax(lr=0.001)

        model.add(Dense(input_dim, activation='relu', input_dim=input_dim))
        model.add(Dropout(0.25))
        model.add(BatchNormalization())
        model.add(Dense(input_dim*100, activation='relu'))
        model.add(Dropout(0.25))
        model.add(BatchNormalization())
        model.add(Dense(input_dim*50, activation='relu'))
        model.add(Dropout(0.25))
        model.add(BatchNormalization())
        model.add(Dense(input_dim*25, activation='relu'))
        model.add(Dropout(0.25))
        model.add(BatchNormalization())
        model.add(Dense(input_dim*3, activation='relu'))
        model.add(Dropout(0.25))
        model.add(BatchNormalization())
        model.add(Dense(input_dim*2, activation='relu'))
        model.add(Dropout(0.25))
        model.add(BatchNormalization())
 
        model.add(Dense(output_dim, activation='softmax', bias_initializer=self.output_bias))
        # model.add(output_dim, activation='softmax')) # うまくいかないとき用
        model.summary()
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=["accuracy"])
        self.model = model

    def train(self):
        self.model.fit(self.x_np, self.y_np, epochs=30, batch_size=256, validation_split=0.1, class_weight=self.class_weight)

    def save(self, name):
        json_name = "machine_learning/" + name + ".json"
        h5_name = "machine_learning/" + name + ".h5"
        json_file = open(json_name,"w")
        json_file.write(self.model.to_json())
        self.model.save_weights(h5_name)

    def load(self, name):
        json_name = "machine_learning/" + name + ".json"
        h5_name = "machine_learning/" + name + ".h5"
        model = model_from_json(open(json_name,"r").read())
        model.load_weights(h5_name)
        self.model = model

    def predict(self, x):
        xnp = np.array(x)
        return self.model.predict(xnp)
