from model.mongo.mongodb import Mongodb
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM,Dense ,Dropout, Bidirectional
import pandas as pd
import numpy as np
import os
import tensorflow as tf
import warnings


warnings.filterwarnings("ignore", category=UserWarning, module="keras")
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

class Prediction:

    def __init__(self):
        print("init model")
        self.mongo = Mongodb(port="27019", database="meteo", collection="meteo")
        self.model = None
        self.x_train = None
        self.y_train = None
        self.filename = "model_mteo.pkl"

    def prepare_data(self):

        # Connexion à la base de données
        self.mongo.connexion()

        data = self.mongo.prepare_data()
        self.mongo.close_connection()

        data = data.sort_values(by='dh_utc', ascending=True)
        data = data.drop(['dh_utc'], axis=1)

        print(data)

        self.n_future = 4  # next 4 days temperature forecast
        self.n_past = 30  # Past 30 days 

        # Séparation des données en ensembles d'entraînement et de test
        train_data, test_data = train_test_split(data, test_size=0.2, shuffle=False)

        x_train, y_train = [], []
        x_test, y_test = [], []

        # Ensembles d'entraînement
        for i in range(0, len(train_data) - self.n_past - self.n_future + 1):
            x_train.append(train_data.iloc[i : i + self.n_past, :].values)
            y_train.append(train_data.iloc[i + self.n_past : i + self.n_past + self.n_future, :].values)

        # Ensembles de test
        for i in range(0, len(test_data) - self.n_past - self.n_future + 1):
            x_test.append(test_data.iloc[i : i + self.n_past, :].values)
            y_test.append(test_data.iloc[i + self.n_past : i + self.n_past + self.n_future, :].values)

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_test, y_test = np.array(x_test), np.array(y_test)

        # Aplatir les données avant de les passer à MinMaxScaler
        x_train_flat = x_train.reshape((x_train.shape[0], -1))
        y_train_flat = y_train.reshape((y_train.shape[0], -1))
        x_test_flat = x_test.reshape((x_test.shape[0], -1))
        y_test_flat = y_test.reshape((y_test.shape[0], -1))

        self.sc_train = MinMaxScaler(feature_range=(0, 1))
        x_train_scaled = self.sc_train.fit_transform(x_train_flat)
        y_train_scaled = self.sc_train.fit_transform(y_train_flat)

        self.sc_test = MinMaxScaler(feature_range=(0, 1))
        x_test_scaled = self.sc_test.fit_transform(x_test_flat)
        y_test_scaled = self.sc_test.fit_transform(y_test_flat)

        x_train_scaled = np.reshape(x_train_scaled, (x_train_scaled.shape[0], 30, 8))
        x_test_scaled = np.reshape(x_test_scaled, (x_test_scaled.shape[0], 30, 8))


        print("x_train shape: ", x_train_scaled.shape)
        print("y_train shape: ", y_train_scaled.shape)
        print("x_test shape: ", x_test_scaled.shape)
        print("y_test shape: ", y_test_scaled.shape)

        self.x_train = x_train_scaled
        self.y_train = y_train_scaled
        self.x_test = x_test_scaled
        self.y_test = y_test_scaled



    
    def train_model(self): 
        if not(os.path.exists(self.filename)):
            regressor = Sequential()
            regressor.add(Bidirectional(LSTM(units=30, return_sequences=True, input_shape = (self.x_train.shape[1],1) ) ))
            regressor.add(Dropout(0.2))
            regressor.add(LSTM(units= 30 , return_sequences=True))
            regressor.add(Dropout(0.2))
            regressor.add(LSTM(units= 30 , return_sequences=True))
            regressor.add(Dropout(0.2))
            regressor.add(LSTM(units= 30))
            regressor.add(Dropout(0.2))
            regressor.add(Dense(units = self.n_future * 8,activation='linear'))
            regressor.compile(optimizer='adam', loss='mean_squared_error',metrics=['acc'])
            regressor.fit(self.x_train, self.y_train, epochs=25,batch_size=32 )
            
            self.model = regressor

            with open(self.filename, 'wb') as model_file:
                pickle.dump(self.model, model_file)

            with open("scaler.pkl", 'wb') as scalerfile:
                pickle.dump(self.sc_test, scalerfile)
        else:
            with open(self.filename, 'rb') as model_file:
                self.model = pickle.load(model_file)

            with open("scaler.pkl", 'rb') as scalerfile:
                self.sc_test = pickle.load(scalerfile)


    def chargeModel(self):
        print("### chargement du modèle ###")
        with open(self.filename, 'rb') as model_file:
                self.model = pickle.load(model_file)
        with open("scaler.pkl", 'rb') as scalerfile:
                self.sc_test = pickle.load(scalerfile)



    def predict(self, data=None):
        data = data.sort_values(by='dh_utc', ascending=True)
        #print("###### data to predict ##### \n", data)
        data = data.drop(['dh_utc'], axis=1)

        data = data.values.tolist()

        data = np.array(data)

        print("data shape : ", data.shape)

        data = np.reshape(data, (1, 30, 8))

        predicted_temperature = self.model.predict(data)

        # Applique inverse_transform sans réorganiser les dimensions
        predicted_temperature = self.sc_test.inverse_transform(np.reshape(predicted_temperature, (predicted_temperature.shape[0], 32)))

        # Applique inverse_transform sans réorganiser les dimensions
        predicted_temperature = np.reshape(predicted_temperature,  (4, 8))

        print('shape predicted : ', predicted_temperature.shape)
        print(predicted_temperature)

        return predicted_temperature