import vector

p1 = vector.obj(px=1000,py=0,pz=0,E=1000)
p2 = vector.obj(px=2000,py=0,pz=0,E=2020)

print (p1+p2)

from charged_particle import *

charged_1 = charged_particle(px=1000,py=0,pz=0,e=1000)
#PEr come ho definito la particella succederà che la sua carica di default sarà nulla. Mi darà un 
#warning in cui mi dice guarda che metto catica nulla. 
print ("Th 4momentum is: ", charged_1.p4,"the charge is: ",charged_1.charge)

#Definisco charget2 a partire da un vettore, ossia a partire da un quadrimomento.
charged_2 = charged_particle_p4(p2,-1)
print("The 4momentum is: ",charged_2.p4,"The charge is: ", charged_2.charge)

new_particle=charged_1+charged_2
print("sum of the two is ", new_particle)
