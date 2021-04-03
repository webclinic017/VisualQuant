from clr import AddReference

AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
import numpy as np


class TestAlgorithm(QCAlgorithm):
    '''In this example we look at the canonical 15/30 day moving average cross. This algorithm
    will go long when the 15 crosses above the 30 and will liquidate when the 15 crosses
    back below the 30.'''
    
    def __init__(self):
            self.symbol = "SPY"
            self.previous = None
            self.fast = None
            self.slow = None
    
    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        
        self.SetStartDate(2013, 10, 4)
        self.SetEndDate(2013, 10, 11)
        self.SetCash(100000)
        # Find more symbols here: http://quantconnect.com/data
        self.AddSecurity(SecurityType.Equity, self.symbol, Resolution.Minute)

        # create a 15 day exponential moving average
        self.fast = self.EMA(self.symbol, 60, Resolution.Minute)

        # create a 30 day exponential moving average
        self.slow = self.EMA(self.symbol, 180, Resolution.Minute)

        
    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        
        Arguments:
            data: TradeBars IDictionary object with your stock data
        '''
        # a couple things to notice in this method:
        #  1. We never need to 'update' our indicators with the data, the engine takes care of this for us
        #  2. We can use indicators directly in math expressions
        #  3. We can easily plot many indicators at the same time    

        # wait for our slow ema to fully initialize
        if not self.slow.IsReady:
            return    

        # define a small tolerance on our checks to avoid bouncing
        tolerance = 0.00015
        
        holdings = self.Portfolio[self.symbol].Quantity

        # we only want to go long if we're currently short or flat
        if holdings <= 0:
            # if the fast is greater than the slow, we'll go long
            if self.fast.Current.Value > self.slow.Current.Value * round(1 + tolerance):
                self.Log("BUY  >> {0}".format(self.Securities[self.symbol].Price))
                self.SetHoldings(self.symbol, 1.0)
             
        # we only want to liquidate if we're currently long
        # if the fast is less than the slow we'll liquidate our long
        if holdings > 0 and self.fast.Current.Value < self.slow.Current.Value:
            self.Log("SELL >> {0}".format(self.Securities[self.symbol].Price))
            self.Liquidate(self.symbol)  

        self.previous = self.Time
        