# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 02:02:00 2020

@author: 1987h
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta

class ta_signals:
    
    def __init__(self, df):
        import copy
        self.df = copy.copy(df)
        
    def ss_dbb(self, returns_window=1):
        
        
        price = self.df["Open"]
        m = self.df["MiddleBand"]
        u2 = self.df["UpperBand_2"]
        l2 = self.df["LowerBand_2"]
        u1 = self.df["UpperBand_1"]
        l1 = self.df["LowerBand_1"]
        k = self.df["Slowk"]
        d = self.df["Slowd"]
        length = self.df.shape[0]
        signal = [0]
        for i in range(1,length):
            if(k[i]<d[i] and k[i]<85 and k[i-1]>=85):
                signal.append(-1)
            elif(k[i]>d[i] and k[i]>15 and k[i-1]<=15):
                signal.append(1)
            else:
                signal.append(0)

        self.df["ss signal"] = signal 
        
        
        ####double bollinger band####
        bb_signal = [0]
        for i in range(1,length):
            if(price[i]>u1[i] and price[i-1]<u1[i-1]):
                bb_signal.append(1)
            elif(price[i]<u1[i] and price[i-1]>u1[i-1]):
                bb_signal.append(-1)
            else:
                bb_signal.append(0)
        
        self.df["dbb signal"] = bb_signal
        
        final = []
        for i in range(length):
            if(self.df["dbb signal"][i]==1 and self.df["ss signal"][i]==0):
                final.append(1)
            elif(self.df["dbb signal"][i]==-1 and self.df["ss signal"][i]==0):
                final.append(-1)    
            elif(self.df["dbb signal"][i]==0 and self.df["ss signal"][i]==1):
                final.append(1)
            elif(self.df["dbb signal"][i]==0 and self.df["ss signal"][i]==-1):
                final.append(-1) 
            else:
                final.append(self.df["dbb signal"][i])
        self.df["signal"] = final   
        return self.df 
    
    
    def rsi_bb(self, returns_window=1):
        
        """
        if rsi > 70 we consider it overbought and enter short. Similarly if rsi < 30 its oversold and we enter short
        """
  
        length = self.df.shape[0]
        
        price = self.df["Open"]
        m = self.df["MiddleBand"]
        u2 = self.df["UpperBand_2"]
        l2 = self.df["LowerBand_2"]
        u1 = self.df["UpperBand_1"]
        l1 = self.df["LowerBand_1"]
        
        rsi_signal = []
        
        for i in range(length):
            if(self.df["RSI"][i]>65):
                rsi_signal.append(-1)
            elif(self.df["RSI"][i]<35):
                rsi_signal.append(1)
            else:
                rsi_signal.append(0)  
                
        self.df["rsi signal"] = rsi_signal   
        
        ####double bollinger band####
        bb_signal = [0]
        for i in range(1,length):
            if(price[i]>u1[i] and price[i-1]<u1[i-1]):
                bb_signal.append(1)
            elif(price[i]<u1[i] and price[i-1]>u1[i-1]):
                bb_signal.append(-1)
            else:
                bb_signal.append(0)
        
        self.df["dbb signal"] = bb_signal
        
        final = []
        for i in range(length):
            if(self.df["dbb signal"][i]==1 and self.df["rsi signal"][i]==0):
                final.append(1)
            elif(self.df["dbb signal"][i]==-1 and self.df["rsi signal"][i]==0):
                final.append(-1)    
            elif(self.df["dbb signal"][i]==0 and self.df["rsi signal"][i]==1):
                final.append(1)
            elif(self.df["dbb signal"][i]==0 and self.df["rsi signal"][i]==-1):
                final.append(-1) 
            else:
                final.append(self.df["dbb signal"][i])
        self.df["signal"] = final   
        return self.df
        
          