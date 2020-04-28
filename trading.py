# -*- coding: utf-8 -*-
"""

@author: 1987h
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib as ta
from copy import copy


class act:
    
    def __init__(self, cash, signal, df):
        from copy import copy
        self.cash = cash
        self.signal = signal
        self.df = copy(df)
        
    def act(self):
        
        """
        Function to trade in the market. We will observe the market condition till the candle for the period closes,
        then after observing the closing price we will take the position assuming we will get the fill at the closing price.
        -----------------------------------------------------------
        cash: Initial cash positions (all amount will be reinvested, cash will be only withdrawn at the end of the session)
        signal: Column of the dataframe(df) from which to take trading signals
        df: dataframe containing prices and signals
        """
    
        position = "flat"
        ret = 0
        rets = []
        count = 0
        pnl = []
        tm = self.cash

        for i in range(self.df.shape[0]):
            if (self.df[self.signal][i]==1 and position=="flat"):
                position = "long"
                ret += self.df["future returns"][i]
                count += 1
                tm = tm*(1+self.df["future returns"][i])
                pnl.append(tm)
            
            elif (self.df[self.signal][i]==1 and position=="short"):
                position = "flat"
                count += 1
                pnl.append(tm)
                
            elif (self.df[self.signal][i]==1 and position=="long"):
                ret += self.df["future returns"][i]
                count += 1
                tm = tm*(1+self.df["future returns"][i])
                pnl.append(tm)
                
            elif (self.df[self.signal][i]==-1 and position=="flat"):
                position = "short" 
                ret -= self.df["future returns"][i] 
                count += 1
                tm = tm*(1-self.df["future returns"][i])
                pnl.append(tm)

            elif (self.df[self.signal][i]==-1 and position=="long"):
                position = "flat"
                count+=1
                pnl.append(tm)
                
            elif (self.df[self.signal][i]==-1 and position=="short"):
                ret -= self.df["future returns"][i]
                count += 1
                tm = tm*(1-self.df["future returns"][i])
                pnl.append(tm)
                
            elif (self.df[self.signal][i]==0 and position=="short"):
                ret -= self.df["future returns"][i]
                count += 1
                tm = tm*(1-self.df["future returns"][i])
                pnl.append(tm)  
                
            elif (self.df[self.signal][i]==0 and position=="long"):
                ret += self.df["future returns"][i]
                count += 1
                tm = tm*(1+self.df["future returns"][i])
                pnl.append(tm)   
                
                
            elif (self.df[self.signal][i]==0 and position=="flat"): 
                count+=1
                pnl.append(tm)
 
        return ((1+ret)*self.cash, ret, pnl)    


def pnl_profile(X_test, y_pred):
    X = copy(X_test)
    X = X.reset_index(drop=True)
    X["future returns"] = X["returns"].shift(-1)
    X["signal"] = y_pred
    action = act(1000, "signal", X)
    final_cash, ret, pnl = action.act()
    print(final_cash)
    print(ret)
    plt.plot(pnl)
    plt.ylabel("PnL")
    plt.legend()
    plt.show()
    return X[["returns","future returns","signal"]], pnl
