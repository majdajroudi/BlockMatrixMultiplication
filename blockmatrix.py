import sys
import threading

p=10
q=10
r=10

finalresult={}

matA=open(sys.argv[1], "r")
lines=matA.readlines()
A=[]
for line in lines:
	A.append(line.split())
matA.close()

matB=open(sys.argv[2], "r")
newlines=matB.readlines()
B=[]
for line in newlines:
	B.append(line.split())
matB.close()

if len(A[0])!=len(B):
	print("Incompatible matrices.")
	sys.exit()

while p>0:
	if len(A)%p==0:
		break
	p-=1

while q>0:
	if len(A[0])%q==0:
		break
	q-=1

while r>0:
	if len(B[0])%r==0:
		break
	r-=1

def matrixmultiply(X, Y):
	return [[sum(int(a)*int(b) for a,b in zip(X_row,Y_col)) for Y_col in zip(*Y)] for X_row in X]

def addM(a, b):
	global finalresult
	res = []
	for i in range(len(a)):
		row = []
		for j in range(len(a[0])):
			row.append(a[i][j]+b[i][j])
		res.append(row)
	return res

def threadfunct(i,k,x):
	global A
	global B
	global finalresult
	global p
	global r
	mat=[[0 for x in range(int(len(B[0])/r))] for y in range(int(len(A)/p))]
	for j in range(q):
		mat=addM(mat, matrixmultiply([row[i*int(len(A)/p):(i+1)*int(len(A)/p)] for row in A[j*int(len(A[0])/q):(j+1)*int(len(A[0])/q)]], [row[j*int(len(A[0])/q):(j+1)*int(len(A[0])/q)] for row in B[k*int(len(B[0])/r):(k+1)*int(len(B[0])/r)]]))
	finalresult[x]=mat
			
x=0
threads=[]
for i in range(p):
	for k in range(r):
		threads.append(threading.Thread(target=threadfunct, args=(i,k,x)))
		x+=1
				

for thread in threads:
	thread.start()

for thread in threads:
	thread.join()

f=open("output.txt", "w")
for k in range(r):
	for i in range(len(finalresult[0])):
		for j in range(p):
			f.write(str(finalresult[(j*k)+j][i])[1:-1] + " ")
		f.write("\n")