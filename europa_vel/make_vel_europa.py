# uses taup velmerge to create a .json vel mode.
# chnage that to Europa's vel model.

import numpy as np
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import seaborn as sns
import json
####
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
#####
modelname = 'prem'
# taup velmerge --mod prem  --asjson
import taup

with open('iasp.json', 'r') as file:
    data = json.load(file)

print(json.dumps(data, indent=4))
data['layers']=data['layers'][:5]

sys.exit()
with taup.TauPServer(taup_path=taup_path) as taupserver:
    #Distance query to get garc from earthquake to station
    params = taup.DistazQuery()
