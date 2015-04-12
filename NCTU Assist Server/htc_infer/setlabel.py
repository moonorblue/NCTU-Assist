import json
import sys
import fileinput
import os

inputFileNAme = sys.argv[1]
userId = sys.argv[2]
label = sys.argv[3]

userIdDoc = "/home/moonorblue/public_html/htc_logdata_withLabel/"+userId

if not os.path.exists(userIdDoc):
    os.makedirs(userIdDoc)



inputDir = "/home/moonorblue/public_html/htc_logdata/"+inputFileNAme
fh1 = open(inputDir,"r")
content = ""
while 1:
	temp = fh1.readline()
	if not temp:
		break
	temp = temp.strip()
	content += temp
# end of while

dataset = json.loads(content)

#print (str(len(dataset)))
count = 0
for line in dataset:
    count = count + 1
    line['lifelabel'] = label
    #print (line['lifelabel'])


outputDir = userIdDoc+"/"+inputFileNAme
jsondata = json.dumps(dataset)

f = open(outputDir,'w')
f.write(jsondata)
f.close()

print ("done")
