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

import sklearn_json as skljson
from sklearn.ensemble import GradientBoostingClassifier

class model():
    def __init__(self, input_list=[], output_list=[], model_flg=False):
        self.x_np = np.array(input_list)
        self.y_np = np.array(output_list)
        self.model_mode = 1 # 0:MLP, 1:勾配ブースティング木
        if len(self.x_np) > 0 and len(self.y_np) > 0:
            self.set_parameters()
            if model_flg:
                self.set_model(model_dict)

    def set_parameters(self):
        if self.model_mode == 0:
            out_sum = self.y_np.sum(axis=0)
            pos = out_sum[0]
            neg = out_sum[1]
            self.output_bias = keras.initializers.Constant(np.log([pos/neg]))
            self.class_weight = {1: (1/neg)*(pos+neg)/2.0, 0: (1/pos)*(pos+neg)/2.0}

    def set_model(self, model_dict):
        if self.model_mode == 0:
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
        elif self.model_mode == 1:
            m_dict = {}
            m_dict["random_state"] = model_dict["random_state"] if "random_state" in model_dict else 1
            m_dict["learning_rate"] = model_dict["learning_late"] if "learning_late" in model_dict else 0.1
            m_dict["min_samples_split"] = model_dict["min_samples_split"] if "min_samples_split" in model_dict else 10
            m_dict["max_depth"] = model_dict["max_depth"] if "max_depth" in model_dict else 8
            m_dict["max_features"] = model_dict["max_features"] if "max_features" in model_dict else 'sqrt'
            m_dict["subsample"] = model_dict["subsample"] if "subsample" in model_dict else 1.0
            self.model = GradientBoostingClassifier(random_state=m_dict["random_state"], learning_rate=m_dict["learning_rate"], min_samples_split=m_dict["min_samples_split"], max_depth=m_dict["max_depth"], max_features=m_dict["max_features"], subsample=m_dict["subsample"])

    def gradientboost_train(self):
        for max_features in ["sqrt"]: #["sqrt","log2"]:
            for random_state in [1]:
                for learning_rate in [0.1]:
                    for min_samples_split in [3]:
                        for max_depth in [12]: #[3,5,7,8,9,10]:
                            for subsample in [0.7]: #[0.3, 0.5, 0.7, 0.9, 1.0]:
                                model_dict = {"max_features":max_features, "random_state":random_state, "learning_rate":learning_rate, "min_samples_split":min_samples_split, "max_depth":max_depth, "subsample":subsample}
                                print(model_dict)
                                self.set_model(model_dict)
                                self.train()

    def train(self):
        # jvのcsvファイル読み込み元のディレクトリがマウントされていない場合にはここでエラー
        if self.model_mode == 0:
            self.model.fit(self.x_np, self.y_np, epochs=30, batch_size=256, validation_split=0.1, class_weight=self.class_weight)
        elif self.model_mode == 1:
            self.model.fit(self.x_np, self.y_np)
            print("Training score: {:.3f}".format(self.model.score(self.x_np, self.y_np)))

    def save(self, name):
        json_name = "machine_learning/" + name + ".json"
        h5_name = "machine_learning/" + name + ".h5"
        if self.model_mode == 0:
            json_file = open(json_name,"w")
            json_file.write(self.model.to_json())
            self.model.save_weights(h5_name)
        elif self.model_mode == 1:
            skljson.to_json(self.model, json_name)

    def load(self, name):
        json_name = "machine_learning/" + name + ".json"
        h5_name = "machine_learning/" + name + ".h5"
        if self.model_mode == 0:
            model = model_from_json(open(json_name,"r").read())
            model.load_weights(h5_name)
            self.model = model
        elif self.model_mode == 1:
            self.model = skljson.from_json(json_name)

    def predict(self, x):
        xnp = np.array(x)
        return self.model.predict(xnp)
