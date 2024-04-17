import pyphysio as ph
import pyphysio.filters as flt
import pyphysio.specialized.heart as heart_tools
from pyphysio.indicators import compute_indicators

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

datadir = 'data_analysis/data/'
filename = 'bitalino.txt'
id_signal = 5
fsamp = 1000

data = pd.read_table(f'{datadir}/{filename}',
                     skiprows=3,
                     sep='\t')

data_values = data.values

signal = ph.create_signal(data_values[:,id_signal], sampling_freq=fsamp)
signal.p.plot()
plt.xlim(5,20)
plt.show()
