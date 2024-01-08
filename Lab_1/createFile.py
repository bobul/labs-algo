from random import randint
N=100
f=open("largefile","w")
k=0
while True:
 n=randint(0,N)
 f.write(str(n)+"\n")
 k=k+1
 if k==100000000:
  f.close()
  break
