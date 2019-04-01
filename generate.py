import cv2 as cv
import numpy as np
import random
import cPickle as pickle

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


def computeShares(shareIdImages, keyImage, F, G, n, k):
	row, col =  shareIdImages[0].shape
	FYC = np.zeros((row, col, k))
	GYC = np.zeros((row, col, k))
	for imIndex in range(len(shareIdImages)):
		shareValImage = np.zeros((row, col))
		for x in range(row):
			for y in range(col):
				F[0,0] = keyImage[x][y]
				sid = shareIdImages[imIndex][x][y]
				for j in range(k) :
					fcoef = 0
					gcoef = 0
					for i in range(k):
						fcoef =(fcoef+ (F[j,i] * (power(sid, i)))%MOD)%MOD
						gcoef = (gcoef + (G[j,i] * (power(sid, i)))% MOD)%MOD
					FYC[x][y][j] = fcoef
					GYC[x][y][j] = gcoef
				shareValImage[x][y] = FYC[x][y][0]
		cv.imwrite(str(imIndex+1)+".pgm", shareValImage)
		pickle.dump(FYC, open(str(imIndex+1)+".fyc", 'wb'))
		pickle.dump(GYC, open(str(imIndex+1)+".gyc", 'wb'))



"""totalShares = input("Enter total number of shares : ")
threshold = input("Enter threshold value : ")
keyImageName = raw_input("Enter the secret key image name : ")
"""
totalShares = 4
threshold = 3
imNames = ["s1.pgm", "s2.pgm", "s3.pgm", "s4.pgm", "s5.pgm"]
keyImage = cv.imread(imNames[0], 0)
row, col = keyImage.shape
k = threshold
images = [0 for i in range(totalShares)]
for i in range(totalShares):
	images[i] = cv.imread(imNames[i+1], 0)

F = np.zeros((k, k))
G = np.zeros((k, k))
for i in range(k) :
	for j in range(i+1):
		F[i, j] = F[j, i] = random.randint(1, 250)
		G[i, j] = G[j, i] = random.randint(1, 250)


computeShares(images, keyImage, F, G, totalShares, k)

