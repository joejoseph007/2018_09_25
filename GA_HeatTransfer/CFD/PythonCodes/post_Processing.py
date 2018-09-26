import re, numpy, os,operator,time,math
import matplotlib.pyplot as plt
from multiprocessing import Pool

global deltaT,write

def read_integers(filename,t):
    with open(filename) as f:
        if t=='f':
            return [float(x) for x in f]
        
        if t=='i':
            z=[int(x) for x in f]
            return z[0]

        if t=='fxy':
            x=[];y=[];z=[]
            for i in f:
                row = i.split()
                x.append(float(row[0]))
                y.append(float(row[1]))
                z.append(float(row[2]))
            return x,y,z



def function(I):
	global deltaT,write
	
	y,T,p = read_integers('../postProcessing/sample/%s/Oulet_T_p.xy'%I, 'fxy')

	#print sum(T)/len(T)
	#plt.plot(y,T)
	#plt.show()
	def Fourier(F,no,l,deltaT,Name,S="No"):
		F1=[]
		F1[:] = [x - numpy.mean(F[no:l]) for x in F]
		
		Fbar=numpy.fft.fft(F1[no:l])
		freq=numpy.fft.fftfreq(len(Fbar))

		if S!="No":
			l1=plt.semilogx(freq[0:len(freq)/2]/deltaT,numpy.abs(Fbar[0:len(Fbar)/2])**0.7)
			plt.setp(l1, linewidth=0.6, color='k')
			plt.grid(True)
			i=numpy.argmax(numpy.abs(Fbar[0:len(Fbar)/2]))
			frequency=freq[i]/deltaT
			plt.title('Max Freq %.2fHz'%frequency,loc='right',fontsize=15)
			plt.savefig('%s.svg'%Name, bbox_inches='tight')
			plt.close()

		return Fbar,freq

	def Plot(Fx,T,no,l,deltaT,Name,Fy=None,S="No"):
		Fx1=[]
		Fx1[:] = [x - numpy.mean(Fx[no:l]) for x in Fx]
		x = numpy.arange(0, l-no, 1)
		
		lines = plt.plot(T[no:l], Fx[no:l], T[no:l], Fx1[no:l])
		l1, l2 = lines
		plt.grid(True)
		plt.setp(l1, linewidth=0.8, color='k')  
		plt.setp(l2, linewidth=0.1, color='b')
		
		if (Fy!=None):
			
			Fy1=[]
			Fy1[:] = [i - numpy.mean(Fy[no:l]) for i in Fy]
			
			lines = plt.plot(T[no:l], Fy[no:l], T[no:l], Fy1[no:l])
			l1, l2 = lines
			plt.grid(True)
			plt.setp(l1, linewidth=0.1, color='g')  
			plt.setp(l2, linewidth=0.7, color='g')

		if S!="No":
			plt.title('%s'%Name,loc='right',fontsize=15)
			plt.savefig('%s.svg'%Name, bbox_inches='tight')
			plt.close()

	def run(a):

		global Fx,Fy,Fz,Mx,My,Mz,T
		
		if a==1:
			Plot(Fx,T,no,l,deltaT,"ForcesX%i"%I,S="Yes")
		elif a==2:
			Plot(Fy,T,no,l,deltaT,"ForcesY%i"%I,S="Yes")
		elif a==3:
			Plot(Fx,T,no,l,deltaT,"ForcesXY",Fy,S="Yes")
		elif a==4:
			Plot(Mz,T,no,l,deltaT,"MomentZ%i"%I,S="Yes")
		elif a==5:
			Fourier(Fx,no,l,deltaT,"Fourier_Fx",S="Yes")
		elif a==6:
			Fourier(Fy,no,l,deltaT,"Fourier_Fy",S="Yes")
		elif a==7:
			Fourier(Mz,no,l,deltaT,"Fourier_Mz",S="Yes")

	return y,T

maxtime=1.5
deltaT=0.0001
write =5000
arr =[round(deltaT*write+deltaT*write*i,3) for i in range(int(maxtime/deltaT/write))]

for i in range(len(arr)):
	if (arr[i]).is_integer():
		arr[i]=int(arr[i])
		print 'yes'

#print arr



y = Pool()
result= y.map(function,arr)
y.close()	
y.join() 
#print len(result[0][0])
#print result[119][1][0]

#plt.show()
plt.close()
Tavg=[]
Tavg1=[0]*len(result[0][0])
c=0

for i in range(len(result)):
	Tavg.append(sum(result[i][1])/len(result[i][0]))
	if i>len(result)/2:
		for j in range(len(result[0][0])):
			Tavg1[j]=result[i][1][j]+Tavg1[j]
		c+=1
#print c
Tavg1=[Tavg1[i]/c for i in range(len(Tavg1))]	

#print Tavg1, len(Tavg1)
print Tavg[len(Tavg)-1] 
plt.plot(Tavg)
plt.show()

plt.plot(result[0][0],Tavg1)
for i in xrange(len(result)/2,len(result)):
 	plt.plot(result[i][0],result[i][1])

#plt.plot(result[119][0],result[119][1])
plt.show()
