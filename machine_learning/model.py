# coding: utf-8 
import os
import csv
import keras
import numpy as np
from .utility import Utility
from keras.metrics import Precision, Recall
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout
from keras.optimizers import Adamax
from keras.layers.normalization import BatchNormalization

import sklearn_json as skljson
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

class model():
    def __init__(self, input_list=[], output_list=[], model_flg=False):
        self.utility = Utility()
        self.x_np = np.array(input_list)
        self.y_np = np.array(output_list)
        self.y_np_2dim = np.array(self.utility.divide_to_2dim_list(output_list))
        self.model_mode = 0 # 0:MLP, 1:勾配ブースティング木, 2:ランダムフォレスト 3:k近傍法 4:SVM

    def set_parameters(self):
        if self.model_mode == 0:
            out_sum = self.y_np_2dim.sum(axis=0)
            pos = out_sum[0]
            neg = out_sum[1]
            self.output_bias = keras.initializers.Constant(np.log([pos/neg]))
            self.class_weight = {1: (1/neg)*(pos+neg)/2.0, 0: (1/pos)*(pos+neg)/2.0}
            print(self.class_weight)

    def set_model_mode(self, mode):
        if mode == "mlp":
            self.model_mode = 0
        if mode == "gradientboost":
            self.model_mode = 1
        elif mode == "randomforest":
            self.model_mode = 2
        elif mode == "knn":
            self.model_mode = 3
        elif mode == "svm":
            self.model_mode = 4
        else:
            self.model_mode = 0

    def set_model(self, model_dict):
        if self.model_mode == 0:
            input_dim = len(self.x_np[0])
            output_dim = len(self.y_np_2dim[0])
            print([input_dim, output_dim])
            model = Sequential()
            optimizer = Adamax(lr=0.001)

            model.add(Dense(input_dim*80, activation='relu', input_dim=input_dim))
            model.add(Dropout(0.2))
            model.add(BatchNormalization())
            model.add(Dense(input_dim*80, activation='relu'))
            model.add(Dropout(0.2))
            model.add(BatchNormalization())
            model.add(Dense(input_dim*5, activation='relu', input_dim=input_dim))
            model.add(Dropout(0.2))
            model.add(BatchNormalization())
            model.add(Dense(input_dim*1, activation='relu', input_dim=input_dim))
            model.add(Dropout(0.2))
            model.add(BatchNormalization())

 
            model.add(Dense(output_dim, activation='softmax', bias_initializer=self.output_bias))
            #model.add(Dense(output_dim, activation='sigmoid')) # うまくいかないとき用
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
        elif self.model_mode == 2:
            m_dict = {}
            m_dict["n_estimators"] = model_dict["n_estimators"] if "n_estimators" in model_dict else 100
            m_dict["criterion"] = model_dict["criterion"] if "criterion" in model_dict else "gini"
            m_dict["max_depth"] = model_dict["max_depth"] if "max_depth" in model_dict else 2
            m_dict["bootstrap"] = model_dict["bootstrap"] if "bootstrap" in model_dict else True
            m_dict["oob_score"] = model_dict["oob_score"] if "oob_score" in model_dict else False
            m_dict["warm_start"] = model_dict["warm_start"] if "warm_start" in model_dict else False
            m_dict["class_weight"] = model_dict["class_weight"] if "class_weight" in model_dict else 'balanced'
            self.model = RandomForestClassifier(n_estimators=m_dict["n_estimators"], criterion=m_dict["criterion"], max_depth=m_dict["max_depth"], bootstrap=m_dict["bootstrap"], oob_score=m_dict["oob_score"], warm_start=m_dict["warm_start"], class_weight=m_dict["class_weight"])
        elif self.model_mode == 3:
            m_dict = {}
            m_dict["n_neighbors"] = model_dict["n_neighbors"] if "n_neighbors" in model_dict else 5
            m_dict["weights"] = model_dict["weights"] if "weights" in model_dict else 'uniform'
            m_dict["leaf_size"] = model_dict["leaf_size"] if "leaf_size" in model_dict else 30
            m_dict["p"] = model_dict["p"] if "p" in model_dict else 2
            self.model = KNeighborsClassifier(n_neighbors=m_dict["n_neighbors"], weights=m_dict["weights"], leaf_size=m_dict["leaf_size"], p=m_dict["p"])
        elif self.model_mode == 4:
            m_dict = {}
            m_dict["kernel"] = model_dict["kernel"] if "kernel" in model_dict else "rbf"
            m_dict["shrinking"] = model_dict["shrinking"] if "shrinking" in model_dict else True
            m_dict["class_weight"] = model_dict["class_weight"] if "class_weight" in model_dict else None
            self.model = SVC(kernel=m_dict["kernel"], shrinking=m_dict["shrinking"], class_weight=m_dict["class_weight"])

    def train(self, import_list=[], mode="gradientboost"):
        self.set_model_mode(mode)
        model_dict = {}
        if mode == "mlp":
            self.set_parameters()
        if mode == "gradientboost":
            model_dict = {"max_features":"sqrt", "random_state":1, "learning_rate":0.1, "min_samples_split":3, "max_depth":15, "subsample":0.7}
        elif mode == "randomforest":
            model_dict = {"n_estimators":1000,"criterion":"gini","max_depth":12,"bootstrap":True,"oob_score":True,"warm_start":False}
        elif mode == "knn":
            model_dict = {"weights":"distance"}
        elif mode == "svm":
            model_dict = {"kernel":"poly", "class_weight":{0:1,1:3}}
        print(model_dict)
        self.set_model(model_dict)
        # 注:jvのcsvファイル読み込み元のディレクトリがマウントされていない場合にはここでエラー出るので確認する
        if self.model_mode == 0:
            self.model.fit(self.x_np, self.y_np_2dim, epochs=20, batch_size=256, validation_split=0.1, class_weight=self.class_weight)
        elif self.model_mode >= 1:
            self.model.fit(self.x_np, self.y_np)
            if self.model_mode == 2 or self.model_mode == 3:
                for i in range(len(self.model.feature_importances_)):
                    print(str(i+1).zfill(3)+" : "+str(round(self.model.feature_importances_[i],5)))
                print("Training score: {:.3f}".format(self.model.score(self.x_np, self.y_np)))
        self.check_accuracy(import_list)

    # 学習完了時の学習データ自体に対する予測精度を一応確認する用
    def check_accuracy(self, import_list):
        if len(import_list) > 0:
            predicted = self.model.predict(self.x_np).tolist()
            count = [0, 0]
            for i in range(len(predicted)):
                if predicted[i] == 1:
                    if len(import_list["goal_order"]) > 0:
                        if import_list["goal_order"][i] <= 3:
                            count[0] = count[0] + 1
                        else:
                            count[1] = count[1] + 1
            print(count)

    def save(self, name):
        json_name = "machine_learning/" + name + ".json"
        h5_name = "machine_learning/" + name + ".h5"
        joblib_name = "machine_learning/" + name + ".joblib"
        if self.model_mode == 0:
            json_file = open(json_name,"w")
            json_file.write(self.model.to_json())
            self.model.save_weights(h5_name)
        elif self.model_mode in [3,4]:
            joblib.dump(self.model, joblib_name)
        elif self.model_mode >= 1:
            skljson.to_json(self.model, json_name)

    def load(self, name):
        json_name = "machine_learning/" + name + ".json"
        h5_name = "machine_learning/" + name + ".h5"
        joblib_name = "machine_learning/" + name + ".joblib"
        if self.model_mode == 0:
            model = model_from_json(open(json_name,"r").read())
            model.load_weights(h5_name)
            self.model = model
        elif self.model_mode in [3,4]:
            self.model = joblib.load(joblib_name)
        elif self.model_mode >= 1:
            self.model = skljson.from_json(json_name)

    def predict(self, x):
        xnp = np.array(x)
        return self.model.predict(xnp)
