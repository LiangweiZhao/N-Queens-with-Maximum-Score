import time
#HW2 of LiangweiZhao
BELONG_SPLA = 1    #An applicant is already in SPLA
BELONG_LAHSA = -1  #An applicant is already in LAHSA
ONLY_SPLA = 1      #An applicant only can go to SPLA
ONLY_LAHSA = -1    #An applicant only can go to LAHSA
BOTH = 2           #An applicant can go both of them
#P is related to the meaning of applicant or homeless people
def checkApplicants(P_Arr_Belong,P_Info):
	#P_Info is a string which contains 20 chars
	P_ID = int(P_Info[:5])
	gender = P_Info[5]
	age = int(P_Info[6:9])
	pet = P_Info[9]
	medical = P_Info[10]
	car = P_Info[11]
	dL = P_Info[12]
	if gender == 'F' and age > 17 and pet == 'N': 
		if car == 'Y' and dL == 'Y' and medical == 'N': #Both
			P_Arr_Belong[P_ID] = BOTH
		else: #Only LAHSA 
			P_Arr_Belong[P_ID] = ONLY_LAHSA
	else: 
		if car == 'Y' and dL == 'Y' and medical == 'N': #Only SPLA
			P_Arr_Belong[P_ID] = ONLY_SPLA
		#Neither doesn't change the value

#Update the Week_States by add or delete applicant
def update_Wk_States(Week_States,P_Info,oper):
	Week_Info = P_Info[13:20]
	for i in range(1,len(Week_States)):
			Week_States[i] += int(Week_Info[i-1]) * oper
#To get current used space each day(Just for initializing)
def P_EachDay_Start(Week_States,P_Arr_SL,P_Info):
	P_ID = int(P_Info[:5])
	if P_ID in P_Arr_SL:
		update_Wk_States(Week_States,P_Info,1)

#Check applicant P_Info is fine to add(*It will change Week_States)
def check_Valid(Week_States,P_Info):
	global SPLA_pk
	Week_Info = P_Info[13:20]
	update_Wk_States(Week_States,P_Info,1)
	for i in Week_States:
		if i > SPLA_pk:
			update_Wk_States(Week_States,P_Info,-1)
			return False
	return True
#Add new applicant if it is valid
def add_New_P(Week_States,P_Info):
	if not check_Valid(Week_States,P_Info):
		update_Wk_States(Week_States,P_Info,-1)
		return False
	return True
#Get the subSet of remain applicants
def subSet(P_Arr_RmID):
	res = [[]]
	for i in P_Arr_RmID:
		tmp = [x+[i] for x in res]
		res.extend(tmp)
	return res
#Scores
def score(days_Arr):
	sum = 0
	for i in days_Arr:
		sum += int(i)
	return sum

#DP: two organizations select applicants
def dp_Select(subSets,totalRm):
	global Week_States_S, Week_States_L
	global P_Arr_RmID, P_Arr_Belong, score_Arr
	global opt_ID_L, opt_ID_S

	print Week_States_S
	print Week_States_L
	print "*****"
	week_S = {}
	week_L = {}
	s = {} #X[i](X=s or l) means use the i-th subset(X choose 1st), how many parking lots or beds they can get
	l = {} # s means SPLA, l means LAHSA. e.g. s[1] = [3,2], by using the 1st subset, SPLA can get 3 parkings lots, LAHSA can get 2 beds
	week_S[0] = Week_States_S
	week_L[0] = Week_States_L
	for i in range(1,totalRm+1):
		ID = subSets[i][0]
		subSetStr = str(subSets[i])
		if(P_Arr_Belong[ID] == 0):
			s[subSetStr] = [0,0]
			l[subSetStr] = [0,0]
			week_S[subSetStr] = Week_States_S
			week_L[subSetStr] = Week_States_L
		else:
			if(P_Arr_Belong[ID] == BOTH):
				if(add_New_P(Week_States_S,P_Arr[ID-1])):
					week_S[subSetStr] = list(Week_States_S)
					update_Wk_States(Week_States_S,P_Arr[ID-1],-1)
					s[subSetStr] = [score_Arr[ID],0]
				if(add_New_P(Week_States_L,P_Arr[ID-1])):
					week_L[subSetStr] = list(Week_States_L)
					update_Wk_States(Week_States_L, P_Arr[ID-1],-1)
					l[subSetStr] = [0,score_Arr[ID]]
			else:
				if(P_Arr_Belong[ID] == ONLY_LAHSA):
					if(add_New_P(Week_States_L,P_Arr[ID-1])):
						week_S[subSetStr] = list(Week_States_S)
						week_L[subSetStr] = list(Week_States_L)
						update_Wk_States(Week_States_L, P_Arr[ID-1], -1)
						s[subSetStr] = [0,score_Arr[ID]]
						l[subSetStr] = [0,score_Arr[ID]]
					else:
						s[subSetStr] = [0,0]
						l[subSetStr] = [0,0]
						week_S[subSetStr] = list(Week_States_S)
						week_L[subSetStr] = list(Week_States_L)
				else:
					if (add_New_P(Week_States_S, P_Arr[ID-1])):
						week_S[subSetStr] = list(Week_States_S)
						week_L[subSetStr] = list(Week_States_L)
						update_Wk_States(Week_States_S, P_Arr[ID-1], -1)
						s[subSetStr] = [score_Arr[ID],0]
						l[subSetStr] = [score_Arr[ID],0]
					else:
						s[subSetStr] = [0, 0]
						l[subSetStr] = [0, 0]
						week_S[subSetStr] = Week_States_S
						week_L[subSetStr] = Week_States_L

	for i in range(totalRm+1,len(subSets)):
		subset = subSets[i]
		maxScore_S = maxScore_L = score_S_S = score_L_L = 0
		opt_ID_L = opt_ID_S = -1
		for j in subset:
			if(P_Arr_Belong[j] >= ONLY_SPLA):
				tmpS = list(subset)
				tmpS.remove(j)
				score_S_S = score_Arr[j] + l[str(tmpS)][0]
				if score_S_S > maxScore_S:
					opt_ID_S = j
					maxScore_S = score_S_S
			if(P_Arr_Belong[j] == ONLY_LAHSA or P_Arr_Belong[j] == BOTH):
				tmpL = list(subset)
				tmpL.remove(j)
				score_L_L = score_Arr[j] + s[str(tmpL)][1]
				if score_L_L > maxScore_L:
					opt_ID_L = j
					maxScore_L = score_L_L
		if opt_ID_S != -1:
			tmpS = list(subset)
			tmpS.remove(opt_ID_S)
			s[str(subset)] = [maxScore_S, l[str(tmpS)][1]]
		else:
			if opt_ID_L != -1:
				tmpL = list(subset)
				tmpL.remove(opt_ID_L)
				l[str(subset)] = [s[str(tmpL)][0],maxScore_L]
				s[str(subset)] = l[str(subset)]
			else:
				s[str(subset)] = [0,0]
				l[str(subset)] = [0,0]
		if opt_ID_L != -1:
			tmpL = list(subset)
			tmpL.remove(opt_ID_L)
			l[str(subset)] = [s[str(tmpL)][0], maxScore_L]
		else:
			l[str(subset)] = s[str(subset)]

	return s[str(subSets[len(subSets)-1])]


start = time.clock()
input_file = open("input0.txt","r")
output_file = open("output.txt","w")

#Get Input Data
LAHSA_b = int(input_file.readline())
SPLA_pk = int(input_file.readline())
#People in LAHSA
P_LAHSA = int(input_file.readline())
P_Arr_LAHSA = []
for i in range(P_LAHSA):
	P_Arr_LAHSA.append(int(input_file.readline()))
#People in SPLA
P_SPLA = int(input_file.readline())
P_Arr_SPLA = []
for i in range(P_SPLA):
	P_Arr_SPLA.append(int(input_file.readline()))
#People total
P = int(input_file.readline())
P_Arr = [] #start by index 0
P_Arr_States = [0 for i in range(P+1)] # (0:free,-1:LAHSA,1:SPLA)
P_Arr_Belong = [0 for i in range(P+1)] # (0:Neither,-1:LAHSA,1:SPLA,2:Both)
Week_States_S = [0 for i in range(8)] # To store current states of parking lots each day
Week_States_L = [0 for i in range(8)] # To store current states of beds each day
for i in range(P):
	#Add all applicants' info
	tmp = input_file.readline()
	if tmp[-1] == "\n":
		tmp1 = tmp[:-1]
	else:
		tmp1 = tmp
	P_Arr.append(tmp1) 
	checkApplicants(P_Arr_Belong,tmp1) #check which service applicants can go
	P_EachDay_Start(Week_States_S,P_Arr_SPLA,tmp1) #update current parking lot occupied
	P_EachDay_Start(Week_States_L,P_Arr_LAHSA,tmp1) #update current beds occupied
	#Update current states of applicants
	if i < P_LAHSA:
		P_Arr_States[P_Arr_LAHSA[i]] = ONLY_LAHSA
	if i < P_SPLA:
		P_Arr_States[P_Arr_SPLA[i]] = ONLY_SPLA

opt_ID_S = -1
opt_ID_L = -1
P_Arr_RmID = [] #Remain applicants
for i in range(1,len(P_Arr_States)):
	if(P_Arr_States[i] == 0): P_Arr_RmID.append(i)
score_Arr = [0 for i in range(P+1)]
for i in P_Arr_RmID:
	score_Arr[i] = score(P_Arr[i-1][13:20])
subSets = subSet(P_Arr_RmID)
subSets.sort()
subSets =  sorted(subSets,key=len)
#still working
#print subSets
print dp_Select(subSets,len(P_Arr_RmID))


print Week_States_S
print Week_States_L
print opt_ID_S
print time.clock() - start
#output_file.write(opt_ID)
