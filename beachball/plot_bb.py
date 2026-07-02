import numpy as np
import taup
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
##

eventdepth=607
phases=['PKP','PKIKP','PKJKP']
taup_path="~/Research/sct_wat/TauP/build/install/TauP/bin/taup"
mpl.rcParams.update({'font.size': 14.5})
########
params = taup.BeachballQuery()

with taup.TauPServer(taup_path=taup_path) as taupserver:
    params.model('prem')
    params.sourcedepth(eventdepth)
    params.phase(phases)
    # params.station(*sta)
    # params.degree(np.arange(125,136,10))
    # params.amp(True)
    # params.mw(8.2)
    params.strikediprake(17,7,-62)
    BB = params.calc(taupserver)
####
