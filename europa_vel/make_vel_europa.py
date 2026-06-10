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

with open('europa_stahler_17.json', 'r') as file:
    data = json.load(file)
with open('iasp.json', 'r') as file:
    data = json.load(file)

# v=json.loads(data)
# print(json.dumps(data, indent=4))
# data['layers']=data['layers'][:5]

# sys.exit()
with taup.TauPServer(taup_path=taup_path,verbose=True) as taupserver:
    taupserver.timeout=50
    #Distance query to get garc from earthquake to station
    params = taup.TimeQuery()
    # params.velocitymodeltext('europa_stahler_17.json')
    params.velocitymodeltext(json.dumps(data))
    params.phase('P')
    svg = params.calc(taupserver)
