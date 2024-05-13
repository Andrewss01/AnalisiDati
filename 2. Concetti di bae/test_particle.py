print("Importing vector AND the particle module")
from os import pipe
import vector, particle, test_vector
#A questo punto import mi permette di importare il modulo che ho appena creato detto 'particle'. Che sta
#nella stessa cartella in cui sta test_particle
#import mi carica i moduli che sono nella stessa cartella. 
#Oltre a quello che è nella stessa cartella.
#Quando lui ha installato vector lo ha aggiunto alla lista di librerie che conosce. 
#Se io facessi import particle ma particle.py non sta nella cartella in cui sta il mio file allora 
#si incazzerebbe come na bestia 


print("We define our particle: ")
#La classe particle si chiama all'interno del modulo che si chiama sempre particle. 
#Io gli devo dire dell'oggetto "particle" mi deve dare quello che si trova all'intenro
#ossia la classe 'particle'. 
#Mettendo la parentesi lui mi chiama il costruttore della classe particle e mi restituirà un oggetto
#particella a cui ha eseguito le operazioni viste.
particle1=particle.particle(px=1,py=0,pz=0,m=0)
#Quando metto la parentesi dopo il nome della classe lui sa che deve chiamare la funzione init
print("and print it! What do we get?")
print(particle1)
#La funzione print cerca di trasformare in stringa quello che si trova affianco. Se non ha 
#mood di farlo ti dice che tipo di oggetto è e l'area di memoria in cui si trova l'oggetto

print(" let's print the vector: ")
print(particle1.p4)
#PEr stampare l'oggetto in maniera sensata mi stampo il p4 dell'oggetto che mi stampa il quadrimomento
#in termini dell'energia. 
print(" what is the energy? ")
print(particle1.e)
#Questo è un campo che ho definito dentro la init. Posso aggiungere ulteriori informazioni derivate
#anche senza passargliele direttamente. Questo perchè nel momento in cui definisco il quadrivettore
#io voglio tutte le informazioni possibili e non voglio dovermele ricalcolare
#ogni volta per ogni particella.
print("inizializziamo la particella a partire dal p4")
#Dobbiamo definire un quadrivettore, lo prendiamo dal p1 del test_vector per esempio
p1 = vector.obj(px=1,py=0,pz=0,E=1) #Questo è un quadrimomento

particle3 = particle.particle.particle_p4(None, p1)
print(particle3.p4)
#il metodo all'interno del particle ha un self quindi se non gli passo un self non va. 
#Devo fare questa funzione aa partire d auna particella esistente. 
print("la somma dei quadrimomenti è", particle.particle.sum(particle3,particle1))

print('Now let us make the sum of two arbitrary vectors')
print('The first vector is:', particle1.p4)
print('The second vector is:', particle3.p4)
print('The sum is:', particle1.p4 + particle3.p4)
#Questo succede perchè i p4 sono delle tuple o liste e quindi il problema
#è come sono definiti gli oggetti 
#Adesso li convertiamo in vettori
print('this happens because of the class operator is defined for the type of the object')
print(type(particle1.p4))
p1 = vector.obj(px = particle1.px, py= particle1.py, pz= particle1.pz,E = particle1.e)
p2 = vector.obj(px = particle3.px, py = particle3.py,pz= particle3.pz,E= particle3.e)
print('The sum returns:', p1+p2)
#La somma ci ridà px, py, pz, E. Se lo fai per componenti ma 
#Lo scopo è quello di non Reinventare le cose e quindi cerchiamo di farlo 
#rifare a chi l'ha già fatto. 
#Il problema è che facendolo per componenti non ci semplifichiamo la vita cpai. 
#Il secondo punto è che vogliamo definite p4 come un vettore dentro la particle
#e perhè non dico alla classe stessa come sommare i quadrimomenti?
#per questo passiamo a charged particele