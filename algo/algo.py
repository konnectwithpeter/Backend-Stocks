import datetime
import os

import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
from core.models import Predictions, Stock


def prediction_algo(stock):
    #df=yf.download(stock, start=datetime.datetime.now(), end="2022-04-30")
    #df.to_csv(stock + ".csv")

    df=pd.read_csv("algo/"+ stock + ".csv")
    # print(df)
    #print(df.tail())
    df1=df.reset_index()['Close']
    #print(df1)
    latest_data = pd.read_csv("algo/"+stock + ".csv").iloc[-1]


    import numpy as np
    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range=(0,1))
    df1=scaler.fit_transform(np.array(df1).reshape(-1,1))
    #print(df1)


    ##splitting dataset into train and test split
    training_size=int(len(df1)*0.65)
    test_size=len(df1)-training_size
    train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]

    #print(training_size,test_size)
    #print(train_data)


    import numpy

    # convert an array of values into a dataset matrix
    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-time_step-1):
            a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return numpy.array(dataX), numpy.array(dataY)
    # reshape into X=t,t+1,t+2,t+3 and Y=t+4

    time_step = 100
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, ytest = create_dataset(test_data, time_step)
    # print(X_train.shape)
    # print(y_train.shape)

    # reshape input to be [samples, time steps, features] which is required for LSTM
    X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
    X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)


    ### Create the Stacked LSTM model
    from tensorflow.keras.layers import LSTM, Dense
    from tensorflow.keras.models import Sequential
    model=Sequential()
    model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
    model.add(LSTM(50,return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error',optimizer='adam')
    #print(model.summary())

    model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=100,batch_size=64,verbose=1)
    import tensorflow as tf

    #print(tf.__version__)
    ### Lets Do the prediction and check performance metrics
    train_predict=model.predict(X_train)
    test_predict=model.predict(X_test)

    ##Transformback to original form
    train_predict=scaler.inverse_transform(train_predict)
    test_predict=scaler.inverse_transform(test_predict)


    ### Calculate RMSE performance metrics
    import math

    from sklearn.metrics import mean_squared_error
    math.sqrt(mean_squared_error(y_train,train_predict))

    ### Test Data RMSE
    math.sqrt(mean_squared_error(ytest,test_predict))

    ### Plotting 
    # shift train predictions for plotting
    look_back=100
    trainPredictPlot = numpy.empty_like(df1)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(train_predict)+look_back, :] = train_predict

    # shift test predictions for plotting
    testPredictPlot = numpy.empty_like(df1)
    testPredictPlot[:, :] = numpy.nan
    testPredictPlot[len(train_predict)+(look_back*2)+1:len(df1)-1, :] = test_predict

    # plot baseline and predictions
    # plt.plot(scaler.inverse_transform(df1))
    # plt.plot(trainPredictPlot)
    # plt.plot(testPredictPlot)
    # plt.show()

    #print(len(test_data)-100)

    x_input=test_data[len(test_data)-100:].reshape(1,-1)

    temp_input=list(x_input)
    temp_input=temp_input[0].tolist()
    # print(len(temp_input))

    # demonstrate prediction for next 10 days
    from numpy import array

    lst_output=[]
    n_steps=100
    i=0
    while(i<30):        
        if(len(temp_input)>100):
            #print(temp_input)
            x_input=np.array(temp_input[1:])
            #print("{} day input {}".format(i,x_input))
            x_input=x_input.reshape(1,-1)
            x_input = x_input.reshape((1, n_steps, 1))
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            #print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input=temp_input[1:]
            #print(temp_input)
            lst_output.extend(yhat.tolist())
            i=i+1
        else:
            x_input = x_input.reshape((1, n_steps,1))
            yhat = model.predict(x_input, verbose=0)
            print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i=i+1
        

    reformed_pred = scaler.inverse_transform(lst_output)
    preds = []   

    for i in range(len(reformed_pred)):
        preds.append(reformed_pred[i][0])

    stk = Stock.objects.get(stock=stock)
    if Predictions.objects.filter(stock=stock).exists():
       Predictions.objects.filter(stock=stock).update(from_date=latest_data['Date'], preds=preds)
    else:
        Predictions.objects.create(stock=stk, from_date=latest_data['Date'], preds=preds)    
       
    return None
