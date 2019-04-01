import cv2 as cv
import numpy as np
import cPickle as pickle
import random 

MOD = 251

def power(x, y):
	if y==0 :
		return 1
	p = power(x, int(y/2)) % MOD
	p = (p*p)%MOD
	if y%2==1 :
		p = (x*p)%MOD
	return p

def modInverse(b):
	return power(b, MOD-2)

numSum = 0 
def combin(xArray, index, pos, l, product):
	global numSum
	if pos > l :
		numSum += product
		return

	for i in range(index, len(xArray)) :
		product *= (-1*xArray[i])
		combin(xArray, i+1, pos+1, l, product)
		product /= (-1*xArray[i])


def getCoeff(xArray, i):
	global numSum
	numSum=0
	combin(xArray, 0, 1, len(xArray)-i, 1)
	return numSum

def genPoly(xArray,yArray):
	xArray = map(int, xArray)
	yArray = map(int, yArray)
	intercept = 0
	k = len(xArray)
	coefficientsArray = np.zeros((k,1))
	for i in range(len(yArray)) :
		y = yArray[i]
		denominator = 1
		numerator = 1
		for j in range(len(xArray)) :
			if i!=j :
				numerator = (numerator * (MOD - xArray[j])%MOD ) % MOD
				denominator = (denominator * (xArray[i]-xArray[j] + MOD)%MOD) % MOD

		intercept = ((y*numerator)%MOD * modInverse(denominator))%MOD 
		coefficientsArray[0] = (coefficientsArray[0]+intercept) % MOD
		curX = xArray[:i]+xArray[i+1:]
		for ii in range(1, k):
			coeff = ((getCoeff(curX, ii)*y)%MOD * modInverse(denominator))%MOD
			coefficientsArray[ii] = (coefficientsArray[ii] + coeff) % MOD
	return coefficientsArray

def calFunctionValue(funCoefs,val):
	res = 0
	k = len(funCoefs)
	for i in range(k):
		res = (res + (funCoefs[i]*(power(val, i)))%MOD)%MOD
	return res

def detectOutsideCheater(f,g,shareId,k):
	c = random.randint(1, 10)
	d = random.randint(1, 10)
	ci = np.zeros((k,1))
	di = np.zeros((k,1))
	for i in range(k):
		for j in range(k):
			ci[i] = (ci[i] + (f[i][j]*(power(c, j)))%MOD + (g[i][j]*(power(c, j)))%MOD)%MOD
			di[i] = (di[i] + (f[i][j]*(power(d, j)))%MOD + (g[i][j]*(power(d, j)))%MOD)%MOD
	hc = genPoly(shareId,ci)
	hd = genPoly(shareId,di)
	if(calFunctionValue(hc,d)!=calFunctionValue(hd,c)):
		print("There is an Outside cheater")
		return True
	else:
		return False

def detectInsideCheater(f,shareId,k):
	e = random.randint(1, 10)
	vi = np.zeros((k,1))
	mi = np.zeros((k,1))
	for i in range(k):
		for j in range(k):
			vi[i] = (vi[i] + (f[i][j] * (power(e, j)))%MOD)%MOD
		mi[i] = f[i][0]
	he = genPoly(shareId,vi)
	h0 = genPoly(shareId,mi)
	if(calFunctionValue(he,0)!=calFunctionValue(h0,e)):
		print("There is an inside cheater")
		return -1
	else:
		return h0[0]


shareIdList = ["s2.pgm", "s3.pgm", "s4.pgm","s5.pgm"]
shareFnames = ["1.fyc", "2.fyc", "3.fyc", "4.fyc"]
shareGnames = ["1.gyc", "2.gyc", "3.gyc", "4.gyc"]
k = 3

images = [0 for i in range(k)] 
for i in range(k):
	images[i] = cv.imread(shareIdList[i], 0)

row, col = images[0].shape
keyImage = np.zeros((row, col))

FYC = []
GYC = []
for i in range(k):
	FYC.append(pickle.load(open(shareFnames[i], 'rb')))
	GYC.append(pickle.load(open(shareGnames[i], 'rb')))


for x in range(row):
	for y in range(col):
		F = []
		G = []
		sid = []
		for i in range(k):
			F.append(FYC[i][x][y])
			G.append(GYC[i][x][y])
			sid.append(images[i][x][y])
		b = detectOutsideCheater(F, G, sid, k)
		if b :
			exit(0)
		b = detectInsideCheater(F, sid, k)
		if b==-1 :
			exit(0)
		keyImage[x][y] = b

cv.imwrite("key.pgm", keyImage)


