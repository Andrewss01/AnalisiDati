print("Hello World!")

print("That was easy, right? Now let's load some libraries! ")

import vector #mi permette di definire i quadrivettore nel seguente modo:
p1 = vector.obj(px=1,py=0,pz=0,E=1)
p2 = vector.obj(px=1.5,py=0,pz=0,E=200)

print ("the sum of the momenta is ", p1+p2)
print('The mass is', (p1+p2).m)
#Lui riesce a fare la somma in maniera opportuna tra le componenti dei quadrivettori
#Quando scriviamo queste librerie ci sono delle utilities per sommare gli oggetti in modo trasparente. 
#Qui è stato definito il significato di somma tra quadrivettori
#Possiamo sfruttarla per farci stampare la massa. 
#I quasdrivettori sono caratteristiche delle particelle che in principio io ptorei voler studiare per questo lavoriamo con i quadrivettori. Adesso abbiamo realizzato