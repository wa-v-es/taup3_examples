# selects sac files based on sts in a grid number
import numpy as np
import sys,re,os
import glob as glob
import shutil
####

eq_path = os.path.expanduser('~/Research/AK_all_stations/sac_files/220526_120223_SA_inc2_r2.5/')

dst='sac_eq_220526_120223/'
with open('sac_eq_220526_120223/STA_DISTANCE_LOC_gridnumber63.txt', 'r') as file:
    for line in file:
        line=line.split()
        name=line[2]

        pattern = os.path.join(eq_path, f'*{name}*.sac')

        for sacfile in glob.glob(pattern):
            shutil.copy2(sacfile, dst)
