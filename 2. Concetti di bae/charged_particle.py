import math, vector
from particle import particle
#Dal modulo particle importa l'oggetto particle che sta all'interno del modulo. 

#Creiamo la classe di particella charged_particle che EREDITA dalla classe di particella ossia
#potrà utilizzare tutti gli stessi metodi della classe madre. 
#Abbiamo aggiunto sia l'energia sia la carica. Possiamo scegliere se inizializzare con la massa 
#o con lenergia. 
class charged_particle(particle):
    def __init__(self,px,py,pz,m=-1,e=-1,charge=None):
        if charge is None:
            print("warning! Charge not specified! Given default charge=0")
            self.charge=0
            #Mi stampa un errore se io non gli inizializzo la carica.
        else:
            self.charge=charge
        if(m!=-1):
            self._m = m
            self._e = math.sqrt(m**2+(px**2+py**2+pz**2))
            #Inizializza o la massa a partire dall'energia o l'energia a partire dalla massa.
        if(e!=-1):
            self._e = e
            if(e**2-(px**2+py**2+pz**2)<0):
                print("warning! E>p+m, unphysical particle! ")
            self._m = math.sqrt(e**2-(px**2+py**2+pz**2))
        super().__init__(px,py,pz,self._m)#questo metodo ripete quanto fatto dalla classe madre
        #utilizzo il metodo inizializzazione della classe madre, ossia gli dico di fare l'inizializzazione
        #della classe particle. Mi viene anche definito un p4 che è una collezione di 4 oggetti
            #self.p4=(self.px,self.py,self.pz,self.e)
        #Vengono defintii degli oggetti .px .py .pz e .p4 
        #Per chiamare l'inizializzazione come la faceva particle devo chiamare super. Questo metodo 
        # di inizializzazione nuovo richiaa il metodo di inizalizzazione della classe madre
        #sono due init diversi. 
        #Io voglio ripetere set px,py e pz ma voglio semplicemente chiamare come lo faceva la classe 
        #madre e oltre a questo faccio altre operazion e questo rendono diverso questo init
        #quello diverso della classe madre.
        self.p4=vector.obj(px=px,py=py,pz=pz,E=self._e)
        #Nella classe particella p4 era solo un insieme di 4 oggetti, invece per come l'ho fatto qua
        #questo è un oggetto della classe vector.

    def charged_particle_p4(self,lorentz_p4,charge):
        return charged_particle(px=lorentz_p4.px,py=lorentz_p4.py,pz=lorentz_p4.pz, e=lorentz_p4.E,charge=charge)
    #Qua vediamo come inizializzare a partire dal quadrimomento, come fatto anche prima. 
    #Non ci sono dei metodi built in per fare varie inizializzazioni diverse, quindi fare
    #dei metodi che lo facciano è la cosa più veloce in python

    def __add__(self,other):
        #Definiamo la somma tra due particella come una cosa che ci dà una nuova particella
        #All'interno della classe definisco questo metodo speciale __add__ che viene interpretato come
        #quello che deve fare l'operazione di +!!
        sum_p4=self.p4+other.p4
        sum_charge=self.charge+other.charge
        #Questa somma è fatta correttamente perchè funziona come volevamo perchè li abbiamo definito
        #come vettori
        return self.charged_particle_p4(lorentz_p4=sum_p4,charge=sum_charge)
    def __str__(self):
        return ("px = "+str(self.p4.px)+" py = "+str(self.p4.py)+" pz = "+str(self.p4.pz)+" E = "+str(self.p4.E)+" charge = "+str(self.charge))
    #Questo metodo speciale ci dice cosa deve fare quanto proviamo a convertirlo in stringa ossia a 
    #stamparlo. Se io non metto questo metodo li stampa il tipo di oggetto e la
    #casella di memoria. 
    #La conversione in stringa è quello che fa automaticamente print.

def charged_particle_p4(lorentz_p4,charge):
    return charged_particle(px=lorentz_p4.px,py=lorentz_p4.py,pz=lorentz_p4.pz, e=lorentz_p4.E,charge=charge)
