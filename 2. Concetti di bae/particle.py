import math, vector
# A partire da queste librerie imposto delle caratteristiche 

class particle:
    def __init__(self,px,py,pz,m):
        self.px = px
        self.py = py
        self.pz = pz
        self.m = m
        #Se voglio riferirmi a una quantità esterna faccio self.p4 = p4, dove p4 non 
        #lo definisco nelle caratteristiche iniziali.
        #Gli oggetti in python non hanno bisogno di specificare il tipo prima di tutto 
        #in secondo luogo non muoiono all'interno della funzione, in python l'oggetto non muore ma resta
        #l'equivalente delle parentesi è l'identazione devo mettere un tab
        #quando finisce la funzione me ne rendo conto perchè esco dal tab, ossia ha un'identazione diversa
        self.e = math.sqrt(m**2+(px**2+py**2+pz**2))
        #Crea l'energia a partire dalle altre componenti che ho
        self.p4=(self.px,self.py,self.pz,self.e)
        #Creo un vettore con le 3 componenti dell'impulso e l'energia
    #Definisce una funzione che ci inizializza la particella a partire dal quadrimomento, invece
    #di farlo da 4 float. 
    def particle_p4(self,lorentz_p4):
        return particle(px=lorentz_p4.px,py=lorentz_p4.py,pz=lorentz_p4.pz, m=lorentz_p4.m)

    def init_p4(self,lorentz_p4):
        self.__init__(px=lorentz_p4.px,py=lorentz_p4.py,pz=lorentz_p4.pz, m=lorentz_p4.m)
    
    def sum(self, other_part):
        px_sum = self.px + other_part.px
        py_sum = self.py + other_part.py
        pz_sum = self.pz + other_part.pz
        e_sum = self.e + other_part.e
        p_sum = (px_sum, py_sum, pz_sum, e_sum)
        return p_sum
    
    