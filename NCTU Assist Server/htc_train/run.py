import os
import itertools
from multiprocessing import Pool
from os import listdir


def training(x):
   cmd = "python /home/moonorblue/public_html/htc_train/new.py -d "+x+" -s 0.1 -c 0.8"
   try:
       os.system(cmd)
   except:
       print ("can not run new.py")


#mypath = "/Users/KaeJer/Documents/HTC_research/data"
rootPath = "/home/ytwen/fbdata/"+userID	"/home/moonorblue/public_html/htc_logdata_withLabel"
fullDir = []

for mydir in listdir(mypath):
	fullDir.append(mypath+'/'+mydir)

pool = Pool()
pool.map(training,fullDir)

# a=['dog','cat','elephant','tiger','lion','monkey']
#pool.map(do,a)

# pool_size=multiprocessing.cpu_count()*2
# pool=multiprocessing.Pool(processes=pool_size,initializer=start_process,)
#pool.map(training,a)
# pool.close()


