import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pandastable import Table, TableModel


class Asset:
    def __init__(self):
        self.TFSA = pd.DataFrame()
        self.RRSP = pd.DataFrame()
        self.Savings = pd.DataFrame()