__author__ = 'KaeJer'

import json
import sys
import random
from pprint import pprint


def cal(value1,value2,testValue,type):
    #print("hi"+value1+" "+value2+" "+testValue)
    if (type == 1):
        if(value1 == "???"):
            if(float(testValue) <= float(value2)):
                return True
            else:
                return False
        elif(value2 == "???"):
            if(float(testValue) >= float(value1)):
                return True
            else:
                return False
        else:
            if((float(testValue) >= float(value1)) and (float(testValue) <= float(value2))):
                return True
            else:
                return False

    elif (type == 2):
        if(value1 == "???"):
            if(float(testValue) < float(value2)):
                return True
            else:
                return False
        elif(value2 == "???"):
            if(float(testValue) >= float(value1)):
                return True
            else:
                return False
        else:
            if((float(testValue) >= float(value1)) and (float(testValue) < float(value2))):
                return True
            else:
                return False

    elif (type == 3):
        if(value1 == "???"):
            if(float(testValue) <= float(value2)):
                return True
            else:
                return False
        elif(value2 == "???"):
            if(float(testValue) > float(value1)):
                return True
            else:
                return False
        else:
            if((float(testValue) > float(value1)) and (float(testValue) <= float(value2))):
                return True
            else:
                return False

    elif (type == 4):
        if(value1 == "???"):
            if(float(testValue) < float(value2)):
                return True
            else:
                return False
        elif(value2 == "???"):
            if(float(testValue) > float(value1)):
                return True
            else:
                return False
        else:
            if((float(testValue) > float(value1)) and (float(testValue) < float(value2))):
                return True
            else:
                return False


inputFileNAme = sys.argv[1]
#classifierName = sys.argv[2]
classifierName = "classifier"+str(random.randrange(1,3+1))

#print (inputName +"   "+classifierName)


rawLines = []

inputDir = "/home/moonorblue/public_html/htc_logdata/"+inputFileNAme
classifierDir = "/home/moonorblue/public_html/htc_classifier/"+classifierName

print (inputDir)

with open(inputDir, 'r') as f:
    for line in f:
        rawLines.append(line)
        #print (line)
        #lines.append(json.loads(line))
    #print (lines)


linesList=[]
for line in rawLines:
    lineDict={}
    clearLine = line.strip(" \n")
    attritubesAndValues = clearLine.split(' ')
    for pair in attritubesAndValues:
        x = pair.split('=')
        lineDict[x[0]] = x[1]
    linesList.append(lineDict)


#print (random.sample(linesList,int((0.1*len(linesList)))))


forPredict = random.sample(linesList,int((0.1*len(linesList))))


ruleSet=[]

with open('/home/moonorblue/public_html/htc_classifier/classifier.txt', 'r') as f:
    for line in f:
        ruleSet.append(line)

ruleDicSet=[]
defaultActivity=''
for rule in ruleSet:
    #print (rule)
    ruleData={}
    ruleContents=[]

    clearLine = rule.strip("\n")
    split = clearLine.split(">")
    activity = split[1] #activity

    if("," in clearLine):
        #multi
        rules = split[0].split(",")
        for singleRule in rules:
            ruleDic={}
            attribute = singleRule.split("=")[0]
            range = singleRule.split("=")[1]
            ruleDic["attribute"] = attribute
            ruleDic["range"] = range
            ruleContents.append(ruleDic)

    else:
        #single
        if('=' in split[0]):
            ruleDic={}
            attribute = split[0].split("=")[0]
            range = split[0].split("=")[1]
            ruleDic["attribute"] = attribute
            ruleDic["range"] = range
            ruleContents.append(ruleDic)
        else:
            ruleData["ruleContents"] = "default"
    if(len(ruleContents)>0):
        ruleData["ruleContents"] = ruleContents
    ruleData["activity"] = activity

    ruleDicSet.append(ruleData)

#print (ruleDicSet)

randomInput = random.sample(linesList,int((0.1*len(linesList))))
#randomInput = linesList
defaultActivity = 0
for rule in ruleDicSet:
            if(rule["ruleContents"] == "default"):
                defaultActivity = rule["activity"]

#print ("Total input :"+str(len(randomInput)))
#print ("Total input :"+str(len(linesList)))
inputCount = 0

activityInfer = []
#for input in randomInput:
for input in linesList:
    inputCount = inputCount+1
    #print ("currentCount :"+str(inputCount))
    #print ("input :" +str(input))
    noActivity=0
    for rule in ruleDicSet:
        flag = 0
        ruleActivity=rule["activity"]
        #print ("rule : "+str(rule))
        for attr in input:
            testValue = input[attr]
            if(flag == 0):
                hit = 0
                count = 0
                if(isinstance(rule["ruleContents"], list)):
                    count = len(rule["ruleContents"])
                    for content in rule["ruleContents"]:
                        #print (rule)
                        range = content['range']
                        attribute = content['attribute']
                        if (attr == attribute):
                            #print ("in ----> "+str(rule))
                            if (range.startswith('[') and range.endswith(']')):
                                values = range[1:-1].split('-')
                                if(range[1:-1].count('-') == 1):
                                    firstValue = values[0]
                                    secondValue = values[1]
                                elif(range[1:-1].count('-') == 2):
                                    if(values[0].endswith('e')):
                                        firstValue = values[0]+'-'+values[1]
                                        secondValue = values[2]
                                    else:
                                        firstValue = values[0]
                                        secondValue = values[1]+'-'+values[2]

                                elif(range[1:-1].count('-') == 3):
                                    firstValue = values[0]+'-'+values[1]
                                    secondValue = values[2]+'-'+values[3]
                                if((cal(firstValue,secondValue,testValue,1)) == True):
                                    hit = hit + 1
                            elif (range.startswith('[') and range.endswith(')')):
                                values = range[1:-1].split('-')
                                if(range[1:-1].count('-') == 1):
                                    firstValue = values[0]
                                    secondValue = values[1]
                                elif(range[1:-1].count('-') == 2):
                                    if(values[0].endswith('e')):
                                        firstValue = values[0]+'-'+values[1]
                                        secondValue = values[2]
                                    else:
                                        firstValue = values[0]
                                        secondValue = values[1]+'-'+values[2]

                                elif(range[1:-1].count('-') == 3):
                                    firstValue = values[0]+'-'+values[1]
                                    secondValue = values[2]+'-'+values[3]
                                if((cal(firstValue,secondValue,testValue,2)) == True):
                                    hit = hit + 1
                            elif (range.startswith('(') and range.endswith(']')):
                                values = range[1:-1].split('-')
                                if(range[1:-1].count('-') == 1):
                                    firstValue = values[0]
                                    secondValue = values[1]
                                elif(range[1:-1].count('-') == 2):
                                    if(values[0].endswith('e')):
                                        firstValue = values[0]+'-'+values[1]
                                        secondValue = values[2]
                                    else:
                                        firstValue = values[0]
                                        secondValue = values[1]+'-'+values[2]

                                elif(range[1:-1].count('-') == 3):
                                    firstValue = values[0]+'-'+values[1]
                                    secondValue = values[2]+'-'+values[3]
                                if((cal(firstValue,secondValue,testValue,3)) == True):
                                    hit = hit + 1
                            elif (range.startswith('(') and range.endswith(')')):
                                values = range[1:-1].split('-')
                                if(range[1:-1].count('-') == 1):
                                    firstValue = values[0]
                                    secondValue = values[1]
                                elif(range[1:-1].count('-') == 2):
                                    if(values[0].endswith('e')):
                                        firstValue = values[0]+'-'+values[1]
                                        secondValue = values[2]
                                    else:
                                        firstValue = values[0]
                                        secondValue = values[1]+'-'+values[2]

                                elif(range[1:-1].count('-') == 3):
                                    firstValue = values[0]+'-'+values[1]
                                    secondValue = values[2]+'-'+values[3]
                                if((cal(firstValue,secondValue,testValue,4)) == True):
                                    hit = hit + 1

                            if(hit == count):
                                #print (rule["ruleContents"])
                                #print ("infer Activity :" + ruleActivity +"--->"+ attr+" :"+ testValue)
                                flag = 1
                                noActivity = 1
                                activityInfer.append(ruleActivity)
                                break

        if(flag == 1):
            break

    #print ("flag :"+str(flag))
    if(noActivity == 0):
        #print ("not inferred, set default :"+defaultActivity)
        activityInfer.append(ruleActivity)
                #if(hit == count):
                #    print ("infer Activity :" + ruleActivity)
                #    break
                #else:
                #    print ("not inferred, set default :"+defaultActivity)
                #print (content)
#ff = open('parse.txt', 'w')

#for line in lines:
#    ff.write("%s " % line["Location"]['coordinates'])
#ff.close()


activityTable={}
for activity in activityInfer:
    if((activity in activityTable) == False):
        activityTable[activity]=0

for activity in activityInfer:
    activityTable[activity] = activityTable[activity]+1

for activity in activityTable:
    activityTable[activity] = float(activityTable[activity]/len(activityInfer))*100
    #print(activity+" : "+ str(activityTable[activity])+"%")

jsonFile = json.dumps(activityTable)

print (str(jsonFile))
