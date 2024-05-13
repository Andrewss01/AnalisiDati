#In questo esercizio vogliamo simulare il flusso dei muoni cosmici
#usiamo scipy.stats per le definizioni di distribuzione esponenziale e binomiale:
from scipy.stats import poisson,binom,expon
#importiamo matplotlib e math:
import matplotlib.pyplot as plt
import math
#prendiamo il flusso totale al livello del mare al di sopra di 10 GeV (https://www.diva-portal.org/smash/get/diva2:1597287/FULLTEXT01.pdf):
#il flusso integrale è ordine di 10-3 [cm-2 s-1 sr-1]:

#Se io lo voglio integrare soltanto nell'angolo solido quello che succede è che
#avrò bisogno dell'angolo solido della sfera, ossia 4 pigreco. 
#Datp che a noi serve solo la semisfera superiore perchè vogliamo solo i cosmici 
#che vengono dall'alto e quindi 2pi
I_0=0.001

#L'angolo solido totale è 2pi (anche se non ne siamo sicuro)
#poi integriamo sulla superficie e sul tempo
#Se tu integri questa su tutto l'angolo solido in realtà ti dovrebbe venire 
# 4/3 pi. Quindi forse il 2 pigreco è sbagliato
#L'integrale totale però deve venire 1 perchè se tu integri su tutto l'angolo solido
#da qualche parte deve venire questo raggio quindi dobbiamo normalizzare
#La distribuzione di probabilità considerando che la probabilità su tutto l'angolo
#solido fa 1. 
#Siccome quella che abbiamo noi è il flusso differenziale noi dobbiamo integrare
#sull'angolo solido per avere il rate totali.

omega=2*math.pi
area=100 # in cm^2
hours=48 # 2 giorni di acquisizione
t_data=hours*3600

#Il rate totale di muoni in un certo numero di ore è 

muon_rate = I_0*omega*t_data*area
print('Il rate di muoni in', str(hours), 'ore è: ', str(muon_rate))

#al di sopra di 10 GeV i muoni cosmici hanno una distribuzione in energia 
#che è un esponenziale decrescente
#Consideriamo per semplicità un esponenziale decrescente con "vita media" 50 GeV: 

e1 = expon(scale = 50, loc = 10)
#nota bene: in realtà dovremmo definirla solo al di sopra di 10 GeV, 
# teniamo questa come prima approssimazione 
#(1/scale)*  e-((x-loc)/scale) --> scale è 
# l'equivalente di 'tau', la vita media, loc è il punto di partenza

#Adesso dobbiamo generare randomicamente secondo questa variabile casuale
#il metodo rvs genera un vettore di oggetti di dimensione scelta da me 
#per esempio generiamo un numero di muoni cosmici compatibile con il rate 
#previsto
energies = e1.rvs(size=int(muon_rate))
#print(energies)
#Sono generati casualmente a partire dall'esponenziale, quindi avranno energie
#che parte da 10 e scende esponenzialmente con una pendenza di 50 GeV
#Se io vado a fare l'istogramma di questo dataset dovrei trovare una forma esponenziale

fig,ax = plt.subplots(1,1)
ax.hist(energies, density = True, bins = 'auto', histtype = 'bar',
alpha = 0.2)
#plt.show()
plt.savefig('figures/exponential.png')

#La scelta degli assi lui la fa ad hoc per ogni istogramma
#sull'asse y lui di default divide il numero di eventi per la larghezza di bin
#che è legato al parametro density. Si riferisce al fatto che, se divido
#per la larghezza di bin sto interpretando quella fuzione come
#densità di probabilità.
#Questa è una feature e bisogna fare attenzione perchè può portare 
# a degli istogrammi che sembrano non avere senso. 
#Ricordatevi che le densità di probabilità possono avere anche
#valori maggiori di 1!!!
#Adesso è piccolo perchè il bin è grande però se il bin è piccolo allora
#ti possono venire numeri più grandi di 1


#Esercizio 1.1 
#Provare a generare il numero di eventi
#Il numero di eventi è fissato ma sappiamo che questo può fluttuare. 
#Quindi dobbiamo generare non solo l'energia ma anche il numero di eventi, poissonianamente

import numpy as np
#Definiamo una nuova muon prob che è una poissonaiana con valore di aspettazione 
#pari al rate atteso.
muon_prob = poisson(muon_rate)
ndatasets = 10000

#Metodo pmf
x = np.arange(muon_prob.ppf(1.0/ndatasets), muon_prob.ppf(1-1.0/ndatasets))
#La ppf inverte la cumulativa della funzione quindi mi da il punto che ha una porbabilit
#di 0.01 e quello con probabilità 0.99
#come estremi della PPF metto 1/(la dimensione del dataset):
#prendo essenzialmente i valori per cui mi aspetto al più 1 evento a sx e 
# 1 evento a dx generando un numero di volte n=(dimensione del dataset)
#Facendo questo trucco uno si trova che i range delle due distribuzioni sono abbastanza simili

ax.clear()
ax.plot(x, muon_prob.pmf(x), 'ro', ms = 2, label = ' N muon probability')
#plt.show()
plt.savefig('figures/poisson_prob.png')
#pmf = probabilità mass function è una funzione di probabilità discreta, e non è una densità di probabilit. 
# Si chiama mass perchè è come se 
#fosse una densità integrata perchè l'integrale della densità è la massa
#Siccome è una probabilità discreta se invece di 1000 eventi scegliamo

#Metodo campionata
#Qua la facciamo campionata generando un certo numero di dati 
#Seconod una poissoniana
n_datas = muon_prob.rvs(ndatasets)
#Generiamo un certo numero di dataset con la funzoone rvs distribuiti poissonianamente
ax.clear()
ax.hist(n_datas, density = True , bins = 'auto', histtype= 'stepfilled', alpha = 0.2)
#plt.show()
plt.savefig('figures/poisson_sampled_prob.png')
#Quando aumentiamo il numero di eventi troviamo una cosa sempre più campaniforme 
#e la distirbuzione tenderà a somigliare sempre di piu alla pmf.
#Man mano che aumento il numero di eventi la mia distribuzione campionata
#Quindi anche se non sono in grado id calcolare l'integrazione posso 
#prendere questa distirbuzione come un'approssimazione della funzione di distribuzioone
#con un errore legato alla radice del numero di eventi che c'è dentro. 

#Se voglio utilizzare quella campionata come approssimazione della pmf
#Devo normalizzarla a uno. Qeullo che fa plt è dividere ogni bin per la sua larghezza
#In modo che rappresenti una funzione normalizzata. 

#Esercizio 1.2 
#Proviamo ora ad aggiungerci un'efficienza del 40%

#Metodo 1
#Semplicemente prendiamo che il numero di eventi sono sempre distribuiti in maniera
#Poissoniana dove ora il valore di aspettazione è scalato per l'efficienza
efficiency = 0.1
muon_prob_eff = poisson(muon_rate * efficiency)
n_eff_datas = muon_prob_eff.rvs(ndatasets)

#Metodo 2
n_gen_pois = muon_prob.rvs()
#Genero un solo valore e poi devo fare la binomiale che prende come input 
#n_gen_pois e l'efficienza. 
n_gen_pois_eff = binom(n_gen_pois, efficiency).rvs()
print("il numero generato di eventi, con efficienza pari a ", efficiency, 'è', n_gen_pois_eff)

#Prendo i dataset, ossia i nuemri di eventi, generati con la poisosniana
n_datas_eff = []
for j in n_datas:
    binom_eff = binom(j, efficiency)
    #applico la distirbuzione binomiale per ognuno dei dataset dove il numero non 
    #è il numero originario ma il numero del dataser 
    #Genero secondo una probabilità minomiale, con numero atteso pari aul numero
    #dell'estraizone poissoniana e probabilità pari all'efficienza
    ngen = binom_eff.rvs()
    n_datas_eff.append(ngen)

ax.clear()
ax.hist(n_eff_datas, density = False, bins = 'auto', histtype= 'stepfilled', alpha = 0.2)
plt.savefig('figures/Poisson_eff_sampled_prob_v1.png')
ax.hist(n_datas_eff, density= False , bins = 'auto', histtype='stepfilled', alpha = 0.2 )
plt.savefig('figures/poisson_eff_sampled_prob_v2.png')

#C'è una distribuzione a rastello perchè ha scelto lui i bin perchè a volte finiscono i bin 
#tra due numeri interi invece andrebbe scelto in odp che si centrino su un intero
#La seconda distribuzione è stata fatta in maniera diversa, non ho generato una votla ma 2 volte. 
#Ovviamente il 1° metodo è più efficiente perchè ho generato una sola volta invece di 2. 

#Esercizio 2
#proviamo a definire una collezione di particelle a partire da questi muoni
#considerandoli tutti verticali
#PEr ognuno di questi muoni provo a definire una particella. Se sono esattamente
#verticali il quadrimomenti saranno solo pz
#In questo caso abbiamo solo pz e l'energia. Se l'energia è molto maggiore della massa del muone
#Allora l'energia e pz saranno uguali. 

from charged_particle import charged_particle as particle

#Avremo un certo numero di particelle generate dalla nostra probabilità poissoniana
n_particles = muon_prob_eff.rvs()
print('Il numero generato di particelle è:', n_particles)
#Costruisco lo spettro in energia legato al numero id evetni generato a caso all'interno
#del rivelatore
spectrum = e1.rvs(size = int(muon_prob_eff.rvs()))

#Se voglio creare un vettore di particelle  devo  creare una lista di particelle
muon_particles = []
m_mu = 0.106 #esprimendo in GeV -> quindi ci aspettiamo che la distirbuzione di

pz_1 = []
pz_2 = []
Verbose = False 
for energy in spectrum:
    #Prendo il costruttore delle mie particelle
    pz = math.sqrt(energy*energy  - m_mu*m_mu)
    #Devo farlo a mano perchè abbiamo un costruttore che può prendere o una massa
    #o un'energia, non abbiamo fatto un costruttore in cui passiamo sia e sia m
    mu_e_mass = particle(px = 0, py = 0, pz = pz, e = energy, charge =-1)
    #muon_particles.append(mu_with_mass)
    mu_e = particle(px = 0, py = 0, pz= energy, e = energy, charge = -1)

    #px  e py sono zero perchè le particell le stiamo considerando verticali. 
    pz_1.append(energy) #Facciamo due vettori uno in cui definiamo pz considerando la massa
    pz_2.append(pz) #e l'altro in cui invece approssimiamo pz con l'energia perchè vogliamo confrontare le due 
    #distribuzioni ottenute in quesot modo
    
    if Verbose:
        print((energy, pz))

#Abbiamo controllato che le due def. di pz, trascurando o meno la massa, e abbiamo
#Controllato che i due si somigliassero. 
count, bins = np.histogram(spectrum)
ax.clear()
ax.hist(pz_1, bins = bins, density= False, histtype= 'stepfilled', alpha = 0.2)
plt.savefig('figures/muon_energy_distribuction.png')

ax.hist(pz_2, bins= bins, density= False, histtype= 'stepfilled', alpha = 0.2)
plt.savefig('figures/muon_pz_distribuction.png')    

#Mettiamo denisty false perchè vogliamo proprio la distribuzione del numero di eventi 
#che mi aspetto

#Quello che io vedo nel rivelatore dobbiamo vedere quanto veramente è influenzato dalla catena di approssimazioni
#Diventa non trascurabile al di sotto del GeV ma sopra i 10 GeV è assolutamentr trascurabile
#Questo è per farvi capire in che modo possiamo sfruttare la generazione di numeri casuali per avere una distribuzione del genere
#Io so che l'energia ha distribuzione esponenziale ma quale sarà la distribuzione del pz?
#Lo so fare analiticamente? PEr farlo devo fare facendo la trasformazione dall'esponenziale  a pz invece con questo metofo
#Possiamo ottenerla analticamente ed è sfruttabile anche nel caso di funzioni più complicate. 


#Esercizio 2.2
#Se i muoni hanno una distribuzione angolare che va come cos^2 theta
#che cosa cambierà? COme possiamo considerare la distribuzione?
#Se io ho una distribuzione angolare in costheta come posso implementarla?
#Se ora non sono tutti verticali ossia andiamo a considerare le dipendenze
#da theta e da phi allora px e py non sono nulli. In realtà rispetto
#phi sono uniformi ma con theta?

#Se hanno un angolo diverso da zero -> px e py non saranno più nulli.
#Pz sarà p per il coseno di theta. Poi abbiamo pT ossia impulso sul piano trasverso. 
#L'impulso trasverso avrà componente px e py. px = pt cos phi e py= pt sin ohi
#Invece pT  = p sin theta. 
#Invece pz = p cos theta. 
# Se theta = 0 pt = 0 e p = pz
#Questo è il modo in cui posso ricostruire i quadrimomenti. 
#Come genero in theta e phi? COme genero per una funzione arbitraria per cui non ho un
#Conto già fatto?

#Il metodo standard è trovare l'integrale della distirbuzione, calcolarne la cumulativa, 
#Invertirla etc....
#Però se ho una funzione posso calcolarla su un asso, integrare e poi generar euniformemente
#e trovare la quantità inversa come abbiamo visto l'altra volta. 
#Si può fare a mano per una funzione però root ce lo fa di default per una qualunque funzione

import ROOT

#print(math.pi)
#DOpodichè per ogni punto si calcola l'equivalente funzione cumulativa, poi generi
#casualmente e fai il loop su tutti i valori della x e vedi il riusltato
#più vicino a quella della cumulativa. Se hai la funzione hai anche la cumulativ
#perchè pioi fare integrale in maneira numerica.

#Dobbiamo per prima cosa definire una funzione 

xMin = -0.5*math.pi
xMax = 0.5*math.pi


cos2 = ROOT.TF1("cos2theta", "[0]*cos(x)*cos(x)+[1]+[2]*x", xMin, xMax)
#TF1 vuol dire che è una funzione di dimensione 1. Ha un nome, una formula e poi ci vuole 
# un minimo e u massimo
cos2.SetParameter(0,1)
cos2.SetParameter(1,0)
cos2.SetParameter(2,0)

#Se non setti il parametro lui mette un numero a caso quindi è buona norma settarlo 

normalization = cos2.Integral(xMin,xMax)
print("L'integrale della funzione è:", normalization)
cos2.SetParameter(0, 1./normalization)
print("Dopo aver normalizzato l'integrale vale: ", cos2.Integral(xMin,xMax))

cFunc = ROOT.TCanvas()
cFunc.Draw()
cos2.Draw()
cFunc.SaveAs('figures/cos2.png')

#Vogliamo vedere un istogramma riempito tramite questa funzione

nevents = 100000
histocos2 = ROOT.TH1F("histocos2", "Histogram Sampled from cos2 distribution", 100, xMin, xMax)
histocos2.FillRandom("cos2theta", nevents)
#Quando ROOT crea un oggetto crea sempre una mappa/dizionario. Nel momento in cui si trova
#in cui file lui crea un oggetto e una chiave per accedervi
#in modo che quando uno va a salvarlo lo salva con il nome della chiave che ha messo
#C'è un nome locale dell'oggetto nel codice ma quando root la crea fa l'oggetto funzione
#con la sua chiave che è data dal nome che ci mettiamo
#Quadno root deve accedere agli oggeti spesso vi accede tramite la chiave e non tramite
#il nome locale. 
#Il fill Random lo fa prendendo la chiave dell'ogetto stesso.

#Il problema è che potrei chiamare due oggetti con la stessa chiave, lui va a sovrascrivere
#la chiave e quindi non ha più modo di accedere al primo oggetto.

#Con il metodo Fill Random io riempirò l'istogramma con un certo numero di eventi
# #Facendo un'estrazione secondo cos2 theta. 
histocos2.Scale(1./nevents)
#Posso scalare l'istogramma per la sua normalizzazione
#Stai semplicemente considerando che la somma degli eventi deve fare 1, ma in realtà
#Quando vado a disegnare la funzione è la funzione che integrata che mi fa 1. 
#Quindi se voglio comprare la distirbuzione con il numero di eventi
#Devo nromalizzare con la larghezza del bin.
#Se vogliamo il valore centrale vale 1/nevents ma è l'integrale (base * altezza) 
#quindi o calcolo l'integrali delle funzioni e li comparo ai dati o semplicemente
#Divido l'istogramm aper la larghezza del bin
histocos2.Scale(1./histocos2.GetBinWidth(1))
print("Larghezza del bin", histocos2.GetBinWidth(1))
#Devo fare in modo che anche la funzione gradino che mi è data dall'istogramma faccia 1.

histocos2.Draw("esame")
cFunc.SaveAs("figures/cos2_withhisto.png")

#Quello che proviamo a fare è fare la stessa cosa ma con una distribuzione
#piatta in phi tra 0 e 2pi e proviamo a fare una nuova classe
#di particelle disegnandoci px,py e pz prendendoli dalla distirbuzione angolare che 
#otteniamo

phif = ROOT.TF1("phi", "[0]", 0, 2*math.pi)
phif.SetParameter(0,1/(2*math.pi))

#theta che ci dice quanot sono verticali e phi direzione rispetto asse z.

px_3 = []
py_3 = []
pz_3 = []

#Un cosmico può arrivare con un certo angolo theta. E la distirbuzione è proprozionale a 
#coseno quadro di theta. Quindi io ho un certo numero N tot che è proporzionale
#All'integrale della distribuzione iin sin theta dphi dtheta dA dt
#Adesso stiamo estraendo in funzione di theta e phi. Sappiamo che la distirbuzione va 
#come coe^2 theta -< estraiamo i theta. I valori di phi saranno casuali uniformi in 2 pi
#Livello di complessità maggiore: se ho un rivelatore che ha una certa forma magari
#il problema è uniforme in phi ma il rivelatore no
#Noi dobbiamo generare delle distirbuzioni uniformi in phi e che vanno come 
#cos^2 theta e non avremo un solo risultato ne avremo tanti. Tante coppie di angoli
#con cui calcoleremo le componenti dei quadrimpulsi. 
for energy in spectrum:
    p_tot = math.sqrt(energy*energy - m_mu*m_mu)
    theta = cos2.GetRandom()
    phi = phif.GetRandom()

    ct = math.cos(theta)
    st = math.sin(theta)
    cp = math.cos(phi)
    sp = math.sin(phi)

    pz = p_tot*ct
    py = p_tot*st*sp
    px = p_tot*st*cp
    #print(px,py)

    muon = particle(px = px, py = py, pz = pz, e= energy, charge = -1)

    px_3.append(px)
    py_3.append(py)
    pz_3.append(pz)


count, bins = np.histogram(pz_3)

ax.clear()
ax.hist(pz_3, bins = bins, density= False, histtype= 'stepfilled', alpha = 0.2)
plt.savefig('figures/muon_pz_full.png')

count, bins = np.histogram(px_3)
ax.clear()
ax.hist(px_3, bins = bins, density= False, histtype= 'stepfilled', alpha = 0.2)
plt.savefig('figures/muon_px_full.png')

ax.clear()
ax.hist(py_3, bins = bins, density= False, histtype= 'stepfilled', alpha = 0.2)
plt.savefig('figures/muon_py_full.png')

#px e py saranno centrate in zero e sono identiche perhcè se li scambio non cambia niente
#invece pz non può essere minore di zero per come è costruito perchè c'è il coseno di theta
#perchè il coseno di theta è sempre positivo per come l'abbiamo definito.
#Se la mia energia viene misrata con risoluzione gaussiana dell'ordine del 10 GeV?