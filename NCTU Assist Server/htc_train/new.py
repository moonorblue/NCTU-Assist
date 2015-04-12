import os
import sys
import getopt
import collections
import itertools
import json
import gc
import time
import datetime
import math
import operator
import pprint
import resource


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

def log2( x ):
	return math.log( x ) / math.log( 2 )
	
def CountClass(Array):
	counter = collections.defaultdict(lambda: 0.0)
	for item in Array:
		counter[item["lifelabel"]]=1.0
	return len(counter.keys())

def OptimalFunction_entropy(ArrayofDic):
	counter = collections.defaultdict(lambda: 0.0)
	for item in ArrayofDic:
		counter[item["lifelabel"]]+=1.0
	numberoflabel=float(len(ArrayofDic))
	entropy=0.0
	Prob_i=0.0
	TEST=0.0

	for classlabel in counter.keys():
		Prob_i=counter[classlabel]/numberoflabel
		TEST=Prob_i*math.log(Prob_i,2)
		entropy=entropy-TEST
		#print str(classlabel)+"\t"+str(counter[classlabel])+"\t" +str(Prob_i)+"\t"+str(math.log(Prob_i,2))+"\t"+str(TEST)
		
	return entropy

# end of class"OptimalFunction"

def Recursive_bunary_spilt(ArrayForCut,start,end,ArrayForPutCutpoint,ArrayForPutCutvalue,CutAttribute):
	Maximun_IGain=0.0
	Best_cut_pint=0
	N=len(ArrayForCut)
	k=CountClass(ArrayForCut)
	entropy_0=OptimalFunction_entropy(ArrayForCut)
	for testpoint in range(start+1,end-1):
		judge_function=0.0
		
		cond1=(ArrayForCut[testpoint]['lifelabel'] != ArrayForCut[testpoint-1]['lifelabel']) 
		cond2=(ArrayForCut[testpoint][CutAttribute] != ArrayForCut[testpoint-1][CutAttribute])
		cond3=(ArrayForCut[testpoint][CutAttribute] not in ArrayForPutCutvalue)

		if cond1 and cond2 and cond3:  # if equal was not the cut point
			left_part=ArrayForCut[start:testpoint]
			right_paert=ArrayForCut[testpoint:end+1]
			
			entropy_1=OptimalFunction_entropy(left_part)
			k1=CountClass(left_part)
			N1=len(left_part)
			
			entropy_2=OptimalFunction_entropy(right_paert)
			k2=CountClass(right_paert)	
			N2=len(right_paert)
			
			judge_function=((math.log(N-1.0,2) + math.log((3.0**k)-2.0,2) - k*entropy_0 +k1*entropy_1 +k2*entropy_2)/N)
			
			this_cut_E=0.0
			this_cut_E=float(float(N1)/N)*entropy_1+float(float(N2)/N)*entropy_2
			this_cut_IG=0.0
			this_cut_IG=entropy_0-this_cut_E
			
			if this_cut_IG>judge_function : # good enough
				if this_cut_IG>Maximun_IGain:
					Maximun_IGain=this_cut_IG
					Best_cut_pint=testpoint
		#end of "can" cut
	#end of this point	
	
	if(Maximun_IGain > 0.0 ): # have a legal cut point
		ArrayForPutCutpoint.append(Best_cut_pint)
		ArrayForPutCutvalue.append(ArrayForCut[Best_cut_pint][CutAttribute])
		Recursive_bunary_spilt(ArrayForCut,start,Best_cut_pint-1,ArrayForPutCutpoint,ArrayForPutCutvalue,CutAttribute)
		Recursive_bunary_spilt(ArrayForCut,Best_cut_pint,end,ArrayForPutCutpoint,ArrayForPutCutvalue,CutAttribute)
		
		
def discretization(inputDir):
# start of input
	dataList=[]
	dirname = inputDir

	# try:
	# 	opts, args = getopt.getopt(sys.argv[1:], "d:")
	# except getopt.GetoptError as err:
	# 	print str(err)
	# 	sys.exit(2)
	# # end of try

	# for o, a in opts:
	# 	if o == "-d":
	# 		dirname = a
	# 	# end of if
	# # end of for
	
	fileslist = os.listdir(dirname) 
	fileslist.sort()
	
	all_data_each_10sec=[]
	allLabel=[]


	for filename in fileslist:
		#print filename
	# start parsing

		fh1 = open(dirname+"/"+filename, "r")
		content = ""
		while 1:
			temp = fh1.readline()
			if not temp:
				break
			temp = temp.strip()
			content += temp
		# end of while
		
		#print filename
		try:
                    dataset = json.loads(content)
		except:
                    return 0

		Magne=[]
		Gyro=[]
		Accel=[]
		Proximity=[]
		Light=[]
		GPS=[]
		Pressure=[]
		lifelable=""
		
		ItemsCount=0;
		for one_sec_data in dataset:
			try:
				ItemsCount+=1
				
				Magne+=one_sec_data['Magne']
				Gyro+=one_sec_data['Gyro']
				Accel+=one_sec_data['Accel']
				Proximity+=one_sec_data['Proximity']
				Light+=one_sec_data['Light']
				GPS+=one_sec_data['GPS']
				Pressure+=one_sec_data['Pressure']
				
				lifelable=one_sec_data['lifelabel']		
				if(not(lifelable in allLabel)):
					allLabel.append(lifelable)
				
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
					ten_result={}
					
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
						ten_result["Light"]=av_Light
					else:
						ten_result["Light"]=None

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
						ten_result["AccelAvg"]=AccelAvg * 10 # let float can be seen

						
						sum_of_diff_sqr=0
						for force in Accelforcelist:
							sum_of_diff_sqr+=((force-AccelAvg)**2)
						AccelSd=(sum_of_diff_sqr/len(Accelforcelist))**0.5
						ten_result["AccelSd"]=AccelSd * 10 # let float can be seen
					else:
						ten_result["AccelAvg"]=None
						ten_result["AccelSd"]=None
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
						ten_result["GyroAvg"]=GyroAvg
						
						sum_of_diff_sqr=0
						for force in Gyroforcelist:
							sum_of_diff_sqr+=(force-GyroAvg)**2
						GyroSd=(sum_of_diff_sqr/len(Gyroforcelist))**0.5
						ten_result["GyroSd"]=GyroSd
					else:
						ten_result["GyroAvg"]=None
						ten_result["GyroSd"]=None
					
					
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
						
						ten_result["MagneAvgX"]=av_Magne.x * 10 # let float can be seen
						ten_result["MagneAvgY"]=av_Magne.y * 10 # let float can be seen
						ten_result["MagneAvgZ"]=av_Magne.z * 10 # let float can be seen
						ten_result["MagneSdX"]=sd_Magne.x * 10 # let float can be seen
						ten_result["MagneSdY"]=sd_Magne.y * 10 # let float can be seen
						ten_result["MagneSdZ"]=sd_Magne.z * 10 # let float can be seen
					else:
						ten_result["MagneAvgX"]=None
						ten_result["MagneAvgY"]=None
						ten_result["MagneAvgZ"]=None
						ten_result["MagneSdX"]=None
						ten_result["MagneSdY"]=None
						ten_result["MagneSdZ"]=None				

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
						ten_result["GPSx"]=av_GPS.x * 1000 # let float can be seen
						ten_result["GPSy"]=av_GPS.y	* 1000 # let float can be seen
					else:
						ten_result["GPSx"]=None
						ten_result["GPSy"]=None					
					#GPS_Speed
					array=[]
					for oneGPS in GPS:
						temp=oneGPS['Speed']
						array.append(temp)
					if (len(array)!=0):
						av_GPS_Speed=sum(array)/float(len(array))
						ten_result["GPSspeed"]=av_GPS_Speed
					else:
						ten_result["GPSspeed"]=None
			

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
						ten_result["proximity"]=av_Proximity
					else:
						ten_result["proximity"]=None
								
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
						ten_result["Pressure"]=av_Pressure
					else:
						ten_result["Pressure"]=None
					
					#time
					try:
						slot_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ti,"%Y-%m-%d %H:%M:%S")))
					except:
						slot_time = datetime.datetime.fromtimestamp(ti/1000.0)
				
					ten_result["Date"]=slot_time.isoweekday()
					ten_result["Period"]=slot_time.hour		
					
					#print
					ten_result["lifelabel"]=lifelable
					all_data_each_10sec.append(ten_result)

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
			except:
				continue
			#end of try catch
    # end of read all file in dir
	

	if(len(allLabel) == 1):
		return 0
	#for each attribute
	CutpointOfAttribute={}
	for attribute in all_data_each_10sec[0].keys():
		#print "handle",attribute
		if attribute == "lifelabel":
			continue
			
		start_point=0
		all_data_each_10sec.sort(key=operator.itemgetter(attribute)) # sort by this attribute
		for i in xrange(len(all_data_each_10sec)):
			if all_data_each_10sec[i][attribute]!=None:
				start_point=i
				break
		#end of for
		
		NoAttributeArray=all_data_each_10sec[0:start_point]
		ForTestArray=all_data_each_10sec[start_point:]
		
		# print NoAttributeArray

		# print ForTestArray
#		minnumber= ForTestArray[0][attribute]
#		maxnumber= ForTestArray[len(ForTestArray)-1][attribute] + 1 # +1 avoid no count of upper
#		rangesize=maxnumber-minnumber

		numberofitems=float(len(ForTestArray))
		Best_cutnumber_Light=0
		Mininumber=2147483647.0

		initial_entropy=OptimalFunction_entropy(ForTestArray)
		##############
		ArrayForPutCutpoint=[]
		ArrayForPutCutvalue=[]
		Recursive_bunary_spilt(ForTestArray,0,len(ForTestArray)-1,ArrayForPutCutpoint,ArrayForPutCutvalue,attribute)
		ArrayForPutCutpoint.sort()
		ArrayForPutCutvalue.sort()
		
		CutpointOfAttribute[attribute]=ArrayForPutCutvalue
		##############
		
	#end of for (attribute)
	
	#start discrete
	for data_10sec in all_data_each_10sec:
		result=""
		for attribute in data_10sec.keys():
			if attribute == "lifelabel":
				continue			
			if data_10sec[attribute]!=None :
				for bound_point in xrange(len(CutpointOfAttribute[attribute])):
					if  bound_point==0 and  (CutpointOfAttribute[attribute][bound_point] > data_10sec[attribute]):
						result+=attribute+"="  +"["+"???"+"-"+str(CutpointOfAttribute[attribute][bound_point])+")"+" "
						break
					elif  bound_point==len(CutpointOfAttribute[attribute])-1 and (CutpointOfAttribute[attribute][bound_point] <= data_10sec[attribute]):
						result+=attribute+"="  +"["+str(CutpointOfAttribute[attribute][bound_point])+"-"+"???"+")"+" "
						break
					elif  (CutpointOfAttribute[attribute][bound_point] <= data_10sec[attribute]) and (CutpointOfAttribute[attribute][bound_point+1] > data_10sec[attribute]):
						result+=attribute+"="  +"["+str(CutpointOfAttribute[attribute][bound_point])+"-"+str(CutpointOfAttribute[attribute][bound_point+1])+")"+" "
						break
		result=data_10sec['lifelabel']+" "+result
		dataList.append(result)
		# print result 
		#end of for (attribute)	
	#end of for (data_10sec)
	return dataList
# end of function "main"	
# end of function "main"

def rg(inputData,inputMinSUp,inputMinConf):
# start of input
	nowTime = time.time()
	filename = None
	minsup = inputMinSUp
	minconf = inputMinConf
	
	tStart = time.time()
	
	# try:
	# 	opts, args = getopt.getopt(sys.argv[1:], "s:c:")
	# except getopt.GetoptError as err:
	# 	print str(err)
	# 	sys.exit(2)
	# # end of try
	
	# for o, a in opts:
	# 	# if o == "-f":
	# 		# filename = a
	# 	# elif o == "-s":
	# 	if o == "-s":
	# 		minsup = float(a)
	# 	elif o == "-c":
	# 		minconf = float(a)	
		# end of if
	# end of for

	# print filename	
	# print minsup


	# assert filename is not None
	# assert minsup is not None

	# fh1 = open(filename, "r")
	
	Maxuse=0
	
	Transations=[]
	# while 1:
	for x in inputData:
		#######################################################
		now_resource=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
		if(now_resource>Maxuse):
			Maxuse=now_resource
		#######################################################	
			
		
		
		temp = x
		if not temp:
			break
		temp = temp.strip()
		temp = temp.split(' ')

		transation={}
		transation['item']=[]
		transation['label']=temp[0]
		transation['item'] = temp[1:]

		Transations.append(transation)
	# end of while
# end of input
	
# start of CBA-RG
	#start of k=1
	# print Transations

	N= len(Transations)
	#print "Transations=",N
	minsup2=N*minsup
	
	k=1
	L= collections.defaultdict(lambda: 0)
	
	for transaction in Transations: # each transaction is a Data
		#print transaction['item'],transaction['label']
		for item in set(transaction['item']):

			now_resource=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
			if(now_resource>Maxuse):
				Maxuse=now_resource
			#######################################################	
			one_rule=item+'>'+transaction['label']
			L[one_rule]+=1
			#print one_rule
		#print len(transaction['item'])
		# end of for	
	# end of for
	L = dict((rule, support) for rule, support in L.iteritems() if support >= minsup2)
	#print '--------------L',k,'---------------------'
	#print L
	prCAR= collections.defaultdict(lambda: [0,0,0])
	for rule, support in L.iteritems():
		rule_item=rule.split('>')
		rule_item=set(rule_item[0:1])
		condSupport=0
		Confidence=0.0
		for transaction in Transations:
			#######################################################
			now_resource=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
			if(now_resource>Maxuse):
				Maxuse=now_resource
			#######################################################	
			set_transaction = set(transaction['item'])
			if rule_item<=set_transaction:
				condSupport+=1
				
		Confidence=float(support)/float(condSupport)
		if Confidence>=minconf:
			prCAR[rule]=[support,Confidence,1]
	
	#end of k=1
	
	#start of k>=2
	while len(L) > 0:
		k+=1
		#
		# generate candidate
		#
		candidate=[]
		for pair in itertools.combinations(L, 2): #each of pair of k to generate k+1
			#######################################################
			now_resource=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
			if(now_resource>Maxuse):
				Maxuse=now_resource
			#######################################################	
			temp=pair[0].split('>')
			part_a_itemset=sorted(temp[0].split(','))#temp[0]
			part_a_label=temp[1]

			temp2=pair[1].split('>')
			part_b_itemset=sorted(temp2[0].split(','))#temp2[0]
			part_b_label=temp2[1]			
			
			if all(part_a_itemset[i]==part_b_itemset[i] for i in xrange(k-2)) :
				if part_a_label==part_b_label:
					rule={}
					rule['item']=[]
					rule['item']=(set(part_a_itemset)|set(part_b_itemset))
					rule['label']=part_a_label
					
					#print rule['item'],rule['label']
					candidate.append(rule)
			
				# end of if
			# end of if			
		# end of for	

		#
		# pruning
		#
		L_new = collections.defaultdict(lambda: 0)
		for transaction in Transations:
			set_transaction = set(transaction['item'])
			for rule in candidate:

				#######################################################
				now_resource=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
				if(now_resource>Maxuse):
					Maxuse=now_resource
				#######################################################	
				if rule['item']<=set_transaction and rule['label']==transaction['label']:
					itemset=','.join(sorted(list(rule['item'])))
					rule=itemset+'>'+transaction['label']
					L_new[rule]+=1
				# end of if
			# end of for	
		# end of for
		#print "--------------------------------------------"
		L_new = dict((rule, support) for rule, support in L_new.iteritems() if support >= minsup2)
		L=L_new
		
		###################
		for rule, support in L.iteritems():
			#print rule, support
			rule_item=rule.split('>')[0]
			rule_item=set(rule_item.split(','))
			condSupport=0
			Confidence=0.0
			#print rule_item, support			
			for transaction in Transations:

				#######################################################
				now_resource=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
				if(now_resource>Maxuse):
					Maxuse=now_resource
				#######################################################	
				set_transaction = set(transaction['item'])
				if rule_item <= set_transaction :
					condSupport+=1
			Confidence=float(support)/float(condSupport)
			if Confidence>=minconf:
				prCAR[rule]=[support,Confidence,k]			
					
		#print '--------------prCAR',k,'---------------------'
		#print prCAR
	
	
	# end of while
	# end of k>=2
	
	tEnd = time.time()
	#fh_Rescoure_Usage = open("Result/Resource", "w+")
	#fh_Rescoure_Usage.write( "-----------------CBA-RG-Usage-----------------"+"\n")
	#fh_Rescoure_Usage.write( "It cost"+ str(tEnd-tStart)+"sec" +"\n")
	#fh_Rescoure_Usage.write( "Resource:" + str(Maxuse) +"MB"+"\n")
	#fh_Rescoure_Usage.write( "-----------------CBA-RG-Usage-----------------"+"\n")
	
	rules = []

	for rule, SupConGen  in prCAR.iteritems():
		r = str(rule)+" "+str(SupConGen[0])+" "+str(SupConGen[1])+" "+str(SupConGen[2])
		rules.append(r)
		# print rule," ",SupConGen[0]," ",SupConGen[1]," ",SupConGen[2]
	return rules


	# print "time:"+str(nowTime - time.time())
	# return 0

# end of function "rg"

def Using(point):
    usage=resource.getrusage(resource.RUSAGE_SELF)
    return '''%s: usertime=%s systime=%s mem=%s mb
           '''%(point,usage[0],usage[1],
                (usage[2]*resource.getpagesize())/1000000.0 )


def sccb(input_d,input_rule):
# start of input
	filename = None
	r_filename= None
	storageconstraint = 0 # Bytes
	Maxuse=0

	storageconstraint = 99999999

	# try:
	# 	opts, args = getopt.getopt(sys.argv[1:], "d:r:c:")
	# except getopt.GetoptError as err:
	# 	print str(err)
	# 	sys.exit(2)
	# # end of try

	# for o, a in opts:
	# 	if o == "-d":
	# 		filename = a
	# 		#print filename
	# 	elif o == "-r":
	# 		r_filename=a
	# 		#print r_filename
	# 	elif o == "-c":
	# 		storageconstraint=(int)(a)
	# 		#print storageconstraint
	# 	# end of if
	# # end of for

	### input handle start
	# assert filename is not None
	# assert r_filename is not None

	# fh1 = open(filename, "r")
	# rs1 = open(r_filename, "r")

	Transations=[]
	# while 1:
	for x in input_d:
		# temp = fh1.readline()
		temp = x
		if not temp:
			break
		temp = temp.strip()
		temp = temp.split(' ')
		
		transation={}
		transation['item']=[]
		transation['label']=temp[0]
		transation['item'] = temp[1:]
		Transations.append(transation)

	# end of while
	
	Ruleset=[]
	# while 1:
	for y in input_rule:
		# temp = rs1.readline()
		temp = y
		if not temp:
			break
		temp = temp.strip()
		temp = temp.split(' ')
		
		#print temp
		rule={}
		rule['rule']=temp[0]
		rule['support']=float(temp[1])
		rule['confidence']=float(temp[2])
		rule['genorder']=float(temp[3])
		rule['size']= float(len(rule['rule']) + 2) #/n/r 
		
		Ruleset.append(rule)

	# end of while
	
	
	
	Ruleset.sort(cmp=comp,reverse=True)

	### input handle end	
	
	ClassifierSize=0
	default_class=""
		
	Classifer=[]
	for rule in Ruleset:
		rule_temp=rule['rule']
		rule_temp=rule_temp.split('>')
		rule_itemset=set(rule_temp[0].split(','))
		rule_label=rule_temp[1]
		rule_cover_some_tra=False
		
		#print rule

		
		CPred=0
		WPred=0
		remove_list=[]
		for i in range(0,len(Transations)):
			tra_itemset = set(Transations[i]['item'])
			tra_label = Transations[i]['label']
			
			if rule_itemset<=tra_itemset: 	###hit Condition
				if rule_label==tra_label: 		###correct prediction
					rule_cover_some_tra=True
					CPred+=1
					remove_list.append(i)
				else :							###wrong prediction
					WPred+=1
				#end of if
			#end of if
		#end of for
		

		if rule_cover_some_tra==True:	
			
			########Storage Constraint Part#########
			if ClassifierSize + rule['size'] <= storageconstraint:
				ClassifierSize = ClassifierSize + rule['size'] 
			########Storage Constraint Part#########
			
				###delete all the cases with the ids in temp from D
				remove_list.sort(reverse=True)
				for remove_index in remove_list:
					del Transations[remove_index]
				#end of for		
				
				###selecting a default class for the current C
				select= collections.defaultdict(lambda: 0)
				for transation in Transations:
					select[transation['label']]+=1
				#end of for	
				
				if(select):
					default_class=max(select, key=select.get)
				#end of if
				
				###insert r at the end of C; 
				C_rule={}
				C_rule['rule']=rule['rule']
				C_rule['errornumder']=WPred
				Classifer.append(C_rule)
		#end of if
		

	# end of for
	
	### Find the first rule p in C with the lowest total number of errors and drop all the rules after p in C;
	Min_point=None
	Min_number=sys.maxint
	for i in range(0,len(Classifer)):
		if	Classifer[i]['errornumder']<=Min_number:
			Min_point=i
			Min_number=Classifer[i]['errornumder']
		#end of if
	# end of for
	Classifer=Classifer
	
	
	#fh_Rescoure_Usage = open("Result/Resource", "a+")
	#fh_Rescoure_Usage.write( "-----------------CBA-CB-Usage-----------------"+"\n")
	#fh_Rescoure_Usage.write( "Resource:" + str(Maxuse) +"MB"+"\n")
	#fh_Rescoure_Usage.write( "-----------------CBA-CB-Usage-----------------"+"\n")

	model = []
	for C_rule in Classifer:
		model.append(C_rule['rule'])
		# print C_rule['rule']
	
	default = '>'+str(default_class)
	model.append(default)
	# print '>'+str(default_class)

	return model
# end of function "main"

def comp(x, y):
	if x['confidence'] > y['confidence']: #confidence large first
		return 1
	elif x['confidence'] < y['confidence']:
		return -1
	else:
		if x['support'] > y['support']:   #support large first
			return 1
		elif x['support'] < y['support']:
			return -1
		else:
			if x['size'] < y['size']:   #size small first.
				return 1
			elif x['size'] > y['size']: 
				return -1
			else:
				if x['genorder'] < y['genorder']:   #x is generated earlier than y. k small first
					return 1
				elif x['genorder'] > y['genorder']: 
					return -1
				else:
					return 0
			# end of if
		# end of if
	# end of if
# end of function "comp"

if __name__ == "__main__":

	try:
		opts, args = getopt.getopt(sys.argv[1:], "d:s:c:")
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	# end of try

	dirname = None
	minSupport = None
	minConfendence = None
  
	for o, a in opts:
		if o == "-d":
			dirname = a
		elif o == "-s":
			minSupport = float(a)
		elif o == "-c":
			minConfendence = float(a)	
		# end of if
	# end of for

		# end of for
	userID = os.path.basename(os.path.normpath(dirname))
	discretizationResult=[]
	rulseSet=[]
	model = []
	discretizationResult = discretization(dirname)
	if (discretizationResult == 0):
                localtime = time.asctime( time.localtime(time.time()) )
		print ("user:"+userID+"    FAIL"+"    Time:"+localtime)
		sys.exit()
	rulseSet = rg(discretizationResult,minSupport,minConfendence)
	if (rulseSet == 0):
		sys.exit()
	model = sccb(discretizationResult,rulseSet)
        fullPath = "/home/moonorblue/public_html/htc_classifier/"+userID
	f = open(fullPath,'w')
	for line in model:
		f.write(line+"\n")

	f.close()
        localtime = time.asctime( time.localtime(time.time()) )
        print ("user:"+userID+"    SUCCESS"+"    Time:"+localtime)
	# print (model)




