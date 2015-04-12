import sys
import getopt
import collections
import itertools
import json
import gc
import pprint
import time
import datetime
import math
import os
import json
import random
import collections


class vector3:
	def __init__(self, x_ = 0.0, y_ = 0.0, z_ = 0.0):
		self.x = x_
		self.y = y_
		self.z = z_
	def __add__(self, obj): 
		return vector3(self.x+obj.x, self.y+obj.y, self.z+obj.z)
	def __sub__(self, obj): 
		return vector3(self.x-obj.x, self.y-obj.y, self.z-obj.z)
	def __mul__(self, obj): 
		return self.x*obj.x+self.y*obj.y+self.z*obj.z
	def __div__(self, obj):
		return vector3(self.x/obj, self.y/obj, self.z/obj)
	def __eq__(self, obj):
		if(self.x==obj.x and  self.y==obj.y and self.z==obj.z ):
			return True
		else:
			return False
	def __str__(self): 
		return "["+str(self.x)+','+str(self.y)+','+str(self.z)+"]"
# end of class"vector3"

def av_vector3(IIIDarray):
	sum_vector=vector3(0.0,0.0,0.0)
	N=len(IIIDarray)
	for IIIDvector in IIIDarray:
		sum_vector+=IIIDvector
	#end of for
	return sum_vector/N
# end of class"av_vector3"

def sd_vector3(IIIDarray):
	N=len(IIIDarray)
	u=av_vector3(IIIDarray)
	
	SumOfX=0.0
	SumOfY=0.0
	SumOfZ=0.0
	for IIIDvector in IIIDarray:
		diff=IIIDvector-u
		SumOfX+= diff.x*diff.x
		SumOfY+= diff.y*diff.y
		SumOfZ+= diff.z*diff.z
		
	return vector3((SumOfX/N)**0.5,(SumOfY/N)**0.5,(SumOfZ/N)**0.5)
# end of class"sd_vector3"


def cal(value1,value2,testValue,type):
    #print("1:"+value1+"2:"+value2+"3:"+testValue)
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
            if((float(testValue) >= float(value1)) and ( float(testValue) < float(value2))):
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


class vector2:
	def __init__(self, x_ = 0.0, y_ = 0.0):
		self.x = x_
		self.y = y_
	def __add__(self, obj): 
		return vector2(self.x+obj.x, self.y+obj.y)
	def __sub__(self, obj): 
		return vector2(self.x-obj.x, self.y-obj.y)
	def __mul__(self, obj): 
		return self.x*obj.x+self.y*obj.y
	def __div__(self, obj):
		return vector2(self.x/obj, self.y/obj)
	def __eq__(self, obj):
		if(self.x==obj.x and  self.y==obj.y ):
			return True
		else:
			return False
	def __str__(self): 
		return "["+str(self.x)+','+str(self.y)+"]"
# end of class"vector2"

def av_vector2(IIDarray):
	sum_vector=vector2(0.0,0.0)
	N=len(IIDarray)
	for IIDvector in IIDarray:
		sum_vector+=IIDvector
	#end of for
	return sum_vector/N
# end of class"av_vector2"


def main():
# start of input
	dirname = None

	# try:
	# 	opts, args = getopt.getopt(sys.argv[1:], "d:")
	# except getopt.GetoptError as err:
	# 	print str(err)
	# 	sys.exit(2)
	# end of try

	# for o, a in opts:
		# if o == "-d":
			# dirname = a

		# end of if
	# end of for
	
	#print dirname
	
	# fileslist = os.listdir(dirname) 
	# fileslist.sort()
	# for filename in fileslist:
		#print filename
	# start parsing

	inputFileNAme = sys.argv[1]
	inputDir = "/home/moonorblue/public_html/htc_logdata/"+inputFileNAme
	#inputDir = inputFileNAme
	# fh1 = open(dirname+"/"+filename, "r")
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

	Magne=[]
	Gyro=[]
	Accel=[]
	Proximity=[]
	Light=[]
	GPS=[]
	Pressure=[]
	lifelable=""

	ItemsCount=0;
	FeatureDataList=[]
	for one_sec_data in dataset:
		ItemsCount+=1
		
		Magne+=one_sec_data['Magne']
		Gyro+=one_sec_data['Gyro']
		Accel+=one_sec_data['Accel']
		Proximity+=one_sec_data['Proximity']
		Light+=one_sec_data['Light']
		GPS+=one_sec_data['GPS']
		Pressure+=one_sec_data['Pressure']
		
		# lifelable=one_sec_data['lifelable']		
		resultList=[]
		if(ItemsCount==10):
			###Count & print
			#divide Date;TimePeriod;
			#divide Light;
			#divide AccelAvg;AccelSd;
			#divide GyroAvg;GyroSd;
			#divide MagneAvgX;MagneAvgY;MagneAvgZ;MagneSdX;MagneSdY;MagneSdZ;
			#divide GPSx;GPSy;GPSspeed;
			#divide proximity;
			#divide pressure;
			#divide label
			result=""
			
			#Light
			array=[]
			for oneLight in Light:
				#################
				ti=oneLight['time']
				#################
				temp=oneLight['X']
				array.append(temp)	
			if (len(array)!=0):
				av_Light=sum(array)/float(len(array))
				log_Light=float('%f' %math.log10(av_Light) )  # accuracy = 0.1f
				result+="Light="+str(log_Light)+ " "
			#else:
			#	result+="Light=NA"+ " "

			#Accel
			Accelforcelist=[]
			for oneAccel in Accel:
				#################
				ti=oneAccel['time']
				#################
				oneAccel_force= (oneAccel['X']*oneAccel['X']+oneAccel['Y']*oneAccel['Y']+oneAccel['Z']*oneAccel['Z'])**0.5
				Accelforcelist.append(oneAccel_force)
				#end of if
			#end of for
			if(len(Accelforcelist)!=0):
				AccelAvg=sum(Accelforcelist)/len(Accelforcelist)
				result+="AccelAvg=" +str(float('%f' %AccelAvg)) + " "
				
				sum_of_diff_sqr=0
				for force in Accelforcelist:
					sum_of_diff_sqr+=((force-AccelAvg)**2)
				AccelSd=(sum_of_diff_sqr/len(Accelforcelist))**0.5
				result+="AccelSd="  +str(float('%f' %AccelSd)) + " "
			#else:
			#	result+="AccelAvg=NA"+ " "
			#	result+="AccelSd=NA"+ " "

			#Gyro
			Gyroforcelist=[]
			for oneGyro in Gyro:
				#################
				ti=oneGyro['time']
				#################
				oneGyro_force= (oneGyro['X']*oneGyro['X']+oneGyro['Y']*oneGyro['Y']+oneGyro['Z']*oneGyro['Z'])**0.5
				Gyroforcelist.append(oneGyro_force)
				#end of if
			#end of for
			if(len(Gyroforcelist)!=0):
				GyroAvg=sum(Gyroforcelist)/len(Gyroforcelist)
				result+="GyroAvg=" +str(float('%f' %GyroAvg)) + " "
				
				sum_of_diff_sqr=0
				for force in Gyroforcelist:
					sum_of_diff_sqr+=(force-GyroAvg)**2
				GyroSd=(sum_of_diff_sqr/len(Gyroforcelist))**0.5
				result+="GyroSd="  +str(float('%f' %GyroSd)) + " "
			#else:
			#	result+="GyroAvg=NA"+ " "
			#	result+="GyroSd=NA"+ " "
			
			
			#Magne
			IIIDarrary=[]
			for oneMagne in Magne:
				#################
				ti=oneMagne['time']
				#################
				temp=vector3(oneMagne['X'],oneMagne['Y'],oneMagne['Z'])
				IIIDarrary.append(temp)
				#end of if
			#end of for
			if(len(IIIDarrary)!=0):
				av_Magne=av_vector3(IIIDarrary)
				sd_Magne=sd_vector3(IIIDarrary)
				result+= "MagneAvgX="+str(float('%f' %av_Magne.x))+" "
				result+= "MagneAvgY="+str(float('%f' %av_Magne.y))+" "
				result+= "MagneAvgZ="+str(float('%f' %av_Magne.z))+" "
				
				result+= "MagneSdX="+str(float('%f' %sd_Magne.x))+" "
				result+= "MagneSdY="+str(float('%f' %sd_Magne.y))+" "
				result+= "MagneSdZ="+str(float('%f' %sd_Magne.z))+" "
			#else:
			#	result+= "MagneAvgX=NA"+" "
			#	result+= "MagneAvgY=NA"+" "
			#	result+= "MagneAvgZ=NA"+" "
				
			#	result+= "MagneSdX=NA"+" "
			#	result+= "MagneSdY=NA"+" "
			#	result+= "MagneSdZ=NA"+" "
			#GPS
			IIDarrary=[]
			for oneGPS in GPS:
				#################
				ti=oneGPS['time']
				#################
				temp=vector2(oneGPS['X'],oneGPS['Y'])
				IIDarrary.append(temp)
				#end of if
			#end of for
			if (len(IIDarrary)!=0):
				av_GPS=av_vector2(IIDarrary)
				result+= "GPSx="+str(float('%f' %av_GPS.x))+" "
				result+= "GPSy="+str(float('%f' %av_GPS.y))+" "
			#else:
			#	result+= "GPSx=NA"+" "
			#	result+= "GPSy=NA"+" "			
				
			#GPS_Speed
			array=[]
			for oneGPS in GPS:
				temp=oneGPS['Speed']
				array.append(temp)
			if (len(array)!=0):
				av_GPS_Speed=sum(array)/float(len(array))
				result+=  "GPSspeed="+str(av_GPS_Speed)+" "
				#if(av_GPS_Speed==0):
				#	result+=  "GPSspeed=type1"+" "
				#elif(0<av_GPS_Speed<=1):
				#	result+=  "GPSspeed=type2"+" "
				#elif(1<av_GPS_Speed<=3):
				#	result+=  "GPSspeed=type3"+" "
				#elif(3<av_GPS_Speed<=9):
				#	result+=  "GPSspeed=type4"+" "
				#elif(9<av_GPS_Speed<=20):
				#	result+=  "GPSspeed=type5"+" "
				#elif(20<av_GPS_Speed<=30):
				#	result+=  "GPSspeed=type6"+" "
				#elif(30<av_GPS_Speed):
				#	result+=  "GPSspeed=type7"+" "

			#else:
			#	result+=  "GPSspeed=NA"+" "

			#Proximity
			array=[]
			for oneProximity in Proximity:
				#################
				ti=oneProximity['time']
				#################
				temp=oneProximity['X']
				array.append(temp)
			
			if (len(array)!=0):
				av_Proximity=sum(array)/float(len(array))
				if(av_Proximity==0):
					result+= "proximity=Zero"+" "
				else:
					result+= "proximity=NonZero"+" "	
			#else:
			#	result+= "proximity=NA"+" "	
						
			#Pressure
			array=[]
			for onePressure in Pressure:
				#################
				ti=onePressure['time']
				#################
				temp=onePressure['X']
				array.append(temp)	

			if (len(array)!=0):
				av_Pressure=sum(array)/float(len(array))
				if(av_Pressure>=980):
					upper=((int)(av_Pressure/2)+1)*2
					down=(int)(av_Pressure/2)*2
					
				else:
					upper=((int)(av_Pressure/5)+1)*5
					down=(int)(av_Pressure/5)*5
				# result+= "Pressure="+str(down)+"-"+str(upper)+" "	
				result+= "Pressure="+str(av_Pressure)+" "					
					
			#else:
			#	result+= "pressure=NA"+" "
				
			
			#time
			
			try:
				slot_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ti,"%Y-%m-%d %H:%M:%S")))
			except:
				slot_time = datetime.datetime.fromtimestamp(ti/1000.0)
				
				
			if(slot_time.isoweekday()<=5):
				result+="Date="+str(slot_time.isoweekday()) + " "
			elif(5<slot_time.isoweekday()<=7):
				result+="Date="+str(slot_time.isoweekday()) + " "
			


			if(6<slot_time.hour<=12):
				result+="Period="+str(slot_time.hour) + " "
			elif(12<slot_time.hour<=18):
				result+="Period="+str(slot_time.hour) + " "
			elif(18<slot_time.hour<=24):
				result+="Period="+str(slot_time.hour) + " " 
			elif(0<slot_time.hour<=6):
				result+="Period="+str(slot_time.hour) + " "				
			
			#upper=((int)((slot_time.hour+1)/3))*3+1
			#lower=((int)((slot_time.hour+1)/3))*3-1
			#if(lower<0):
			#	upper=25
			#	lower=23
			#result+="Period=[" +str(lower)+"-"+str(upper)+ "] "	

			#print
			# print lifelable+" "+result
			resultList.append(result)
			#appendToList
			FeatureDataList.append(result)
			
			# print "Array"
			#print FeatureDataList
			###reset
			ItemsCount=0
			Magne=[]
			Gyro=[]
			Accel=[]
			Proximity=[]
			Light=[]
			GPS=[]
			Pressure=[]			
			#end of if	

	inputFileNAme = sys.argv[1]
	inputID = inputFileNAme.split("_")[1].split(".")[0]
	path = "/home/moonorblue/public_html/htc_classifier/"+inputID




	rawLines = FeatureDataList
	classifierDir = None
	#rawLines = resultListclassifierDir=None
	if(os.path.isfile(path)):
		classifierDir = path
		#print ("use exist personal classifier")
	else:
		classifierName = "classifier"+str(random.randrange(1,3+1))
		classifierDir = "/home/moonorblue/public_html/htc_classifier/"+classifierName
		#print ("use public classifier")

	#with open(inputDir, 'r') as f:
	# with open('input.txt', 'r') as f:
	    # for line in f:
	        # rawLines.append(line)
	        #print (line)
	        #lines.append(json.loads(line))
	    #print (lines)


	linesList=[]
	for line in rawLines:
	    lineDict={}
	    clearLine = line.strip(" \n")
	    #print (clearLine)
	    attritubesAndValues = clearLine.split(' ')
	    for pair in attritubesAndValues:
	        x = pair.split('=')
	        lineDict[x[0]] = x[1]
	    linesList.append(lineDict)


	#print (random.sample(linesList,int((0.1*len(linesList)))))


	forPredict = random.sample(linesList,int((0.1*len(linesList))))


	ruleSet=[]

	with open(classifierDir, 'r') as f:
	#with open('classifier.txt', 'r') as f:
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
                # print ("noactivity="+str(noActivity))
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
	    # print ("noactivity="+str(noActivity))
	    #print ("flag :"+str(flag))
	    if(noActivity == 0):
	        # print ("not inferred, set default :"+defaultActivity)
	        activityInfer.append(defaultActivity)
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
	    # print(activity+" : "+ str(activityTable[activity])+"%")
        sort = collections.OrderedDict(sorted(activityTable.items(), key=lambda x: x[1],reverse = True))
	jsonFile = json.dumps(sort)

	print (str(jsonFile))	
	    # end of read all file in dir"
	# end of function "main"

if __name__ == "__main__":
	main()


