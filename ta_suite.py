# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 01:59:38 2020

@author: 1987h
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

class ta_suite:
    
    def __init__(self, df):
        """
        return of the past 1-candle on an open to open basis.
        Shift close , high, low to access the past data
        """
        self.df = df
        self.high = df["High"].shift(1).values
        self.low = df["Low"].shift(1).values
        self.close = df["Close"].shift(1).values
        self.open = df["Open"].values
        self.dates = df["Date"].values
        self.time = df["Time1"].values
        
    def stoch(self,fastk_period=5,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0):
        self.slowk, self.slowd = ta.STOCH(self.high,self.low,self.close,fastk_period,slowk_period,slowk_matype,slowd_period,slowd_matype)
        return self.slowk,self.slowd
    
    def bbands(self, timeperiod=14,nbdevup=2,nbdevdn=2,matype=0):
        self.upperband, self.middleband, self.lowerband = ta.BBANDS(self.close,nbdevup=nbdevup,nbdevdn=nbdevdn)
        return self.upperband, self.middleband, self.lowerband
    
    def ema(self, timeperiod=30):
        return ta.EMA(self.close, timeperiod=timeperiod)
    
    def rsi(self, timeperiod=14):
        return ta.RSI(self.close, timeperiod=timeperiod)
    
    def cci(self, timeperiod=14): #commodity channel(momentum)
        return ta.CCI(self.high,self.low,self.close, timeperiod=timeperiod)

    def atr(self, timeperiod=14): #Average true indicator(volatility)
        return ta.ATR(self.high,self.low,self.close, timeperiod=timeperiod)
    
    def adx(self, timeperiod=14): #Average directional index(trend)
        return ta.ADX(self.high,self.low,self.close, timeperiod=timeperiod)
    
    def corr(self, timeperiod=14):
        sma = self.df.Close.rolling(window=timeperiod).mean()
        return sma.rolling(window=timeperiod).corr(self.df.Close)
    
    def sar(self):
        return ta.SAR(self.high, self.low, 0.2,0.2)
    
    
    def combine(self, returns_window = 1):
        """
        Combining different indicators
        """
        
        op = self.df.Open
        hi = self.df.High.shift(1)
        lo = self.df.Low.shift(1)
        cl = self.df.Close.shift(1)
        
        
        slowk, slowd = self.stoch()
        u2,m,l2 = self.bbands()
        u1,m,l1 = self.bbands(nbdevup=1,nbdevdn=1)
        rsi = self.rsi()
        cci = self.cci()
        ema_21 = self.ema(timeperiod=21)
        ema_50 = self.ema(timeperiod=50)
        ema_100 = self.ema(timeperiod=100)
        ema_200 = self.ema(timeperiod=200)
        atr = self.atr()
        sar = self.sar()
        corr = self.corr()
        
        
        temp = pd.DataFrame({"Date":self.dates,"Time":self.time,"Open":op,"Close":cl,"High":hi,"Low":lo,"Slowk":slowk,"Slowd":slowd, \
                           "MiddleBand":m,"UpperBand_2":u2,"LowerBand_2":l2,"BandSplit_2":u2-l2,"UpperBand_1":u1, \
                            "LowerBand_1":l1,"BRatio_2":(self.close-m)/(u2-l2),"RSI":rsi, \
                             "ema_50_21":ema_50-ema_21,"ema_100_50":ema_100-ema_50,"ema_200_100":ema_200-ema_100, \
                             "CCI":cci, "ATR":atr, "SAR":sar, "CORR":corr
                            })
        temp["returns"] = np.log(self.df.Open/self.df.Open.shift(1))
        temp["future returns"] = np.log(self.df.Open/self.df.Open.shift(returns_window)).shift(-returns_window)
        
        def get_boolean(row):
            ret = 0
            if row["future returns"]>0:
                ret = 1
            else:
                ret = -1
            return ret
        
        temp["future returns(classifier)"] = temp.apply(get_boolean, axis=1)
        
        
        temp = temp.dropna().reset_index(drop=True)
        return temp
        