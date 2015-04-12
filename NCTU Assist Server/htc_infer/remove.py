import sys
import os
import shutil

userId = sys.argv[1]

userIdDoc = "/home/moonorblue/public_html/htc_logdata_withLabel/"+userId

if(os.path.exists(userIdDoc)):
    print ("exist")
    shutil.rmtree(userIdDoc)
else:
    print("none")
