import ROOT
import sys,os
import numpy as np
import math

#Vogliamo fare lo scan della likelihood con delle funzioni pre determinate in funzione dei parametri s e b. Parliamo dello scan della  funzione di verosimiglianza
#intorno a uno o più parametri. Abbiamo detto che se la distribuzione dei dati è gaussiano fissado theta = theta cappuccio, allor ci dobbiamo aspettare che
#Facendo uno scan del parametro troveremo una -2loglikelihood che è parabolica intorno al valore di minimo. 
#Vogliamo prendere una extended maximum likelihood in cui abbiamo un certo numero di eventi che fluttua poissonianamente e delel distribuzioni continue Ps e Pb che sono
#delle distirbuzioni in funzioni della variabile x, che noi prendiamo come dataset unbinned.
#Vogliamo minimizzare la -2log likelihood in funzioni di parametri
#Adesso noi fisdiamo gli altri parametri che civengono dati dal modello e facciamo los can in funzione di s e b. 

#Questo file serve per fornire un esempio su come si creano delle librerie. 

#Ci permette di linkare la libreria di python che si trova all'interno della nostra cartella
#lui ci dice con sys.path il percorso da cui si prende le librerie di python ossia ci da la lista
#di cartelle da cui si prende le librerie tra cui " " che significa la cartella attuale
#Quindi aggiungiamo allalista sys.path e aggiungiamo la liberia che ci interessa
#Non gli devo passare il percorso assoluto!
#
sys.path.append(os.getcwd()+("/python")) #aggiungiamo il path di python, dove metteremo le librerie
print(sys.path)
#posso trattare tutto quello che si trova nella cartella di python come se si trovasse in loca
#cosi come io ho fatto import ROOT senza importarmente un cazzo perchè sta nelle cartella
#da cui io prendo le liberrie


#Parte 1: costruiamo il modello dal file di configurazione
#Possiamo fare import utilies e lui lo vede come se fosse in locale e lui lo tratta
#come se fosse nella stessa cartella. Questo è il trucco per allegare pacchetti che 
#potresti aver definito da un'altra parte. 

from utilities import getModel #carichiamo la funzione model che usiamo per prendere i modelli  

fg,fe,fge,fgefrac=getModel("models/model_3.txt") #vedere getModel: restituisce funzione gaussiana, esponenziale e somma
#Get Model è una funzione che ci ha fatto per costruire  il modello a partire dai parametri 
#Nota: se abbiamo usato una notazione consistente
#dovremmo poter scegliere l'analisi variando solo il numero "3"
#che sta prima dell'estensione del file, qui e nei vari punti dove è necessario

#Parte 2: usiamo le utilities di root per il fit
print(fge)
#La prima cosa che gli abbiamo chiesto di fare è di stampare l'istogramma 
#del modello gaussiana + esponenziale
fileHistos=ROOT.TFile("LLFile_3.root")#prendiamo il file creato prima

#Ha preso il file e ha fittato una gaussiana e un exp e di disegnare
h3=fileHistos.Get("data_exercise_Likelihood_3_txt")
fge.SetParameters(780,50,200,70,800,850)
fge.FixParameter(5,850)
h3.Fit(fge.GetName(), "LEMS")

h3min = h3.GetBinLowEdge(1)
h3max = h3.GetBinLowEdge(1000)
binwidth = h3.GetBinWidth(1)
print("ns =", fge.GetParameter(3)," nb= ",fge.GetParameter(4))
print("integrals ",fge.Integral(h3min,h3max),h3.Integral())

c1=ROOT.TCanvas()
c1.Draw()
h3.Draw()
c1.SaveAs("fitGaussExpo1.png")

#Ricordiamo che la funzione era 4* esponenziale normalizzato + 3* una gaussiana normalizzata
#p0 centro gaussiana, p1 sigma della gaussiana, p2 il fattore dell'esponenziale
#p3 e p4 i fattori che mettiamo davanti le due funzioni
#Vediamo che lui fa un fit al punto centrale del bin e abbiamo visto che 
#Fare questa cosa può portare ad alcuni problemi quando la stastistica è bassa
#un modo è, fargli usare l'opzione i. 

#PEr fare il likelihood scan dobbiamo prendere e scrivere la funzione e valutarla, nel caso dell unbinned in ognuno dei punti
#nel caso dei bin dobbiamo fare una produttoria sui singoli bin.

#Domanda pazza: abbiamo trovato 850 eventi ma può essere S+b diverso da 850????
#Il punto è che S+B avrà una fluttuazione poissoniana intorno a qualunque sia il valore vero. Nel momento in cui lo minimizzo se non avessi questo termine (non so quale)
#Allora l'unico minimo possibile sarebbe 850. Non è fissato perchè c'è il termine di shape che mi dice che la combinazione di gaussiana ed esponenziale 
#può non essere compatibile con 850.


#Parte 3: facciamo il likelihood scan attorno theta = theta cappuccio e trovare i valori di L al variare della test statistic.

#Supponiamo di avere un solo parametro, ossia di avere B= N -S. Questo non è corretto perchè in principio s+b luttua ma stiamo semplificanod. 
#Se noi avessimo solo il parametro S come facciamo a ottenere lo scan di theta attorno al suo minimo?
#Dobbiamo fare un loop sui valori possibili di s perchè il parametro potra avere dei valori in un determinato range.
from utilities import txtToArray #carichiamo la funzione model che usiamo per prendere i modelli  

#otteniamo il vettore "unbinned": ho bisogno di riprendere il file di dati. Una copia è in "models"
x_array=txtToArray("models/exercise_Likelihood_3.txt")
#print (x_array)


#otteniamo il vettore "binned"
xbinned_array= np.array([ h3.GetBinContent(i) for i in range(1,h3.GetNbinsX()+1)]) 
#print (xbinned_array)

#Esercizio:
#Usando le funzioni fge.Eval(x) e fge.Integral(xmin,xmax)
#proviamo a valutare la likelihood
#in funzione del numero di eventi di segnale e fondo

do_simple_scan = False
outfile = ROOT.TFile.Open("likelihood_exersise.root", "RECREATE")

N_events = len(x_array) #Il numero di eventi è guuale al numero di entries nell'istogramma
nll_vector = [] #Vettore di negative log likelihood
nll_values = ROOT.TH1F("nll_values", "nll_values", N_events, 0, N_events)

if do_simple_scan:
    for s in range(0,  N_events):

        b = N_events -s 
        #Se noi facciamo il range stiamo andando da lontanissimo, fino al minimo fino a molto lontano
        #Il valore del minimo che ci aspettiamo di trovare è quello del fit (in realtà non proprio perchè 
        # nwl fit abbiamo fatto variare tutti i parametri invece ora fissiamo alcuni)
        #Per ognuno dei valori del parametro otteniamo la funzione di lieklihood e facciamo il caso
        #semplificato in cui B è legato a S
        #Per valutare la funzione dobbiamo utilizzare la funzione eval nel caso della distribuzione unbinned
        #che ci dice il valore della ditribuzione calcolato in quel particolare punto.
        #fissiamo gli altri parametri a quelli che sappiamo della teori.
        fgefrac.SetParameters(800, 50,200, s, b)
    

        #I parametri p3 e p4 rappresentano, se gaussiana ed esponenziale sono normalizzate, sono l'integrale della funzione
        #L'integrale della funzione è valutato su tutto il range e quello che si confronta dovrebbe essere il valore
        #corrispondente al valore del bin, quindi per essere normalizzato correttamente va diviso per la larghezza del bin
        nll = 0
        lik_value = 1

        #print("signal value is", s)
        for xi in x_array:
            #print("xi is", xi, "value is", fgefrac.Eval(xi))
            value_xi = fgefrac.Eval(xi)
            #con il loop possiamo fare la produttoria del valore della funzione
            lik_value = lik_value*value_xi
            #Per avere una funzione parabolica dobbiamo fare il logaritmo
            nll = nll -2 * math.log(value_xi)
            #print("likelihood is", lik)
            #print("nll is", nll)
        #Stiamo valutando la verosimiglianza nell'ipotesi in cui è tutto esponenziale
        #Ho sicuramente quei punti del tonfo strevzo che no ci azzeccano. 
        #Man mano che aggiungo x la likelihood continua a decrescere fin quando poi non arriva a zero perhcè è arrivato alla precisione
        #Del floating point. Questo è un buon motivo per cui è meglio usare il logaritmo. 
        #Quello che vogliamoo è che per ogni s vogliamo vedere che succede stampandoci la nll
        #print("the total negative log-likelihood sample for the above value of s is:", nll)
        #Vediamo che il valore di nll decresce e poi ricresce quindi da qualche parte sto minimo ci sta. 
        #Vediamo come visualizzarlo
        nll_values.SetBinContent(s+1, nll)
        nll_vector.append(nll)
    c2 = ROOT.TCanvas()
    nll_values.Draw("")
    c2.SaveAs("nll_values_1D_no_poisson.png")
    nll_values.Write()

#Quando l'andiamo a guardare non sembra parabolica ma a me non interessa che sia
#gaussiana in qualunque punto dell'asse perchè potrei trovarmi in regioni no sense del parametro di interesse. 
#s = 800 vuol dire che ho solo un unico piccone di s 800, questo non ha senso! Il valore di nll deve quindi essre 
#molto grande per S =800 infatti escono dei valori insensati. 
#Cosa succede intorno a dei valori + decenti? il numero di eventi di segnale sono circa un 80.
#Quindi ci aspettiamo di osservare un minimo a circa 70/80 eventi. 
#Mi viene in aiuto il file root. se prendo il file root posso andare a zommare 
#e vedo una forma simil parabolico.
#Il range di variazione di 1 sigma è quello per cui la likelihood cambia di un'unità. 
#L'intervallo che noi stiamo vedendo è circa 4 sigma quindi ci sta che la forma sia non gaussiana
#Se mi tengo nell'intervallo dei 3 sigma vediamo la shape approssimativamente parabolica.
#Il fatto che sia asimmetrica vuol dire che l'errore da dx è diverso da quello da sx
#Qualunque algoritmo di minimizzazione farà uno scan di una funzione del genere
#La likelihood è la metrica che vogliamo minimizzare ma qualsiasi algoritmo che utilizziamo per far eun fit
#Anche gli algorimti di ML fanno l'operazione di cercare il minimo da qualche parte
#Tipicamente c'è una metrica e un algoritmo che fa fare un certo numerod i passi
#Dobbimamo avere una metrica e un algoritmo di spostamento
#E' abbastanza ovvio perchè non abbiamo altri minimi relativi nel senso che la derivata
#ci porta sempre  dall astessa parte e, andando avanti e indietro troverò il minimo.

#A detta sua è un esempio semplice ed esplicativo

#Qui siamo volto vicini allo zero e al limtie fisico e questa cosa contribuisce
#alla natura asimmetrica di questa cosa. Se il minimo fosse in un parte + centrale forse saremmo messi megli


#Un numero di eventi segnale + grande, in questo particolare caso, fissando l'integrale di entrmabi a 1
#Avrei la distirbuzione gaussiana sarà + alta credo. Abbiamo un numero di eventi di segnale S2 > S1
#In questo caso questo significa. Ovviamente quale delle due sia migliore dipende dal dataset, quale dei fit è migliore.
#Lo decide il dataset quando è il valore di minimo della nll.

#quello che possiamo fare è valutare che cosa succede se s e b fluttuano in maniera "indipendente"
#Potrebbe darsi che il modello di fondo non è quello o c'è una componente di fondo che non abbiamo considerato
#quindi magari il fondo non ha la shape esponenziale che ci aspettiamo ma ha una forma diversa
#Non è nemmeno detto che la shape esponenziale e gaussiana debbano fittare bene  idati, può darsi che l'informaizone
#sul numero di eventi ci dia un vincolo su quanti eventi di fondo e segnale ci sono ma magari la shape
#esponenziale dà un contributo negativo alla likelihood

#Stiamo dicendo che s e b fluttino attorno a n però con qualche libertà. Dopodichè dicimao che debbano rispettare un'altra relaizone
#ossia una esponenziale e l'altra gaussiana.
#Se io andassi a vedere al funzione solamente esponenziale allora mi pesa negativamente 
#questo tipo di distribuzione. Se io guardassi solo la shape io vorrei metter euna shape che preferisce avere
#0 esponenziale e tutto gausssiana, questa sarebbe la forma ideale.
#Succede che rispetto al numero di eventi toale questo è esponenziale e quindi per fittare
#il numero di eventi ttoale, nle momento in cui metto il numeor di eventi, la shape non torna con la normalizzazione solo gaussiana
#il fatto che ci sia il numero di eventi che preferisce essere guuale al numero di eventi
#totale.
#può essere che il num. di eventi spinga l'esponenziale verso l'alto e la shape lo 
#spinga verso il basso. Non necessariamente il termine poissonianao e quello di shape
#spingono nella stessa direzione. 
#Le cose potrebbero non tornare esattamente come le vedimao
#Una cosa del genere potrebbe avvenire anche per una questione di sottofluttuazione perchè
#noi stiamo valutando quello che succede in un particolare dataset. 


#aggiungiamo ora un pezzo poissoniano per il numero di eventi e la varazione del parametro b
#dobbiamo scrivere la poissoniana intorno ad s+b e aggiungere il contributo corrispondente nella nostra
#extended maximum likelihood

#dobbiamo considerare due loop: uno su s e uno su b

pois = ROOT.TF1("Nevents", "TMath::Poisson(x,[0])", 0, N_events)
n_split = 10 

#Se vogliamo essere puntigliosi s e b devono essere tra 0 e n_events ma in teoria
#potrebbero essere superiori di neventi se entrmabi sono una sottofluttuazione del numero di eventi attesi

nll_values_2D_counting = ROOT.TH2F("nll_values_2D_counting", "nll_values_2D_counting", int(N_events/n_split), 0, N_events, int(N_events/n_split), 0, N_events)
nll_values_2D_shape    = ROOT.TH2F("nll_values_2D_shape", "nll_values_2D_shape", int(N_events/n_split), 0, N_events, int(N_events/n_split), 0, N_events)

if do_simple_scan:
    for s in range(0, N_events, int(n_split)):
        for b in range(0,N_events, int(n_split)):
            #Mi aspetto che i valori s+b molto lontani da n_Eventi saranno soppressi 
            #sal termine di poissoniana della likelihood
            pois.SetParameter(0, s+b)
            #cI SIAMO fatti una funzione che valuta la poissoniana. Adesso ci dimentichiamo
            #la parte di shape e facciamo solo un counting experiment. Cosa succede?
            #Ci aspettiamo che il valore migliore sia proprio s+b = n_events ossia il numero di eventi nei dati. 
            #Se io avessi s+b diverso da n_events, allora avremo che la probabilità di questo valore sarà basso.
            #Il valore massimo della probabilità si avrà quando s+b = n_event, con una fluttuazione che dipenderà 
            #dalla radice di n?
            #print("s and b are:", s, "+", b, " the likelihood is: ", pois.Eval(N_events))
            #posso distinguere s da b con questo modello? no non posso con un counting experiment
            #a meno che io non abbia una stima iniziale di s o di b.
            #Da un grafico 2d i punti si distribuiranno lungo la retta s+b = N_events
            nll_poisson = 0 
            if (pois.Eval(N_events) != 0):
                nll_poisson = -2*math.log(pois.Eval(N_events))
                nll_values_2D_counting.SetBinContent(int((s+1)/n_split),int((b+1)/n_split), nll_poisson)
            else: 
                nll_poisson = 0
                nll_values_2D_counting.SetBinContent(s+1,b+1, nll_poisson)
            #Set bin content mette il bin i-esimo ed ora è diverso dal contenuto del bin iesimo. una cosa è l'indice una cosa è l'asse
            fgefrac.SetParameters(800,50,200,s,b)

            nll = 0
            lik_value =1
            for xi in x_array:
                value_xi = fgefrac.Eval(xi)
                #Questo eval è sempre diverso da zero perchè sto facendo sempre il valore della funzione
                lik_value = lik_value*value_xi
                nll = nll - 2* math.log(value_xi)
            
            if nll_poisson != 0:
                nll_tot = nll + nll_poisson
                nll_values_2D_shape.SetBinContent(int((s+1)/n_split), int((b+1)/n_split), nll_tot)
                #print('nll tot is:', nll_tot)
            else:
                nll_values_2D_shape.SetBinContent(int((s+1)/n_split),int((b+1)/n_split), 0)
    c3 = ROOT.TCanvas()
    nll_values_2D_counting.Draw("colZ")
    c3.SaveAs("nll_2D_counting.png")
    nll_values_2D_counting.Write()
    nll_values_2D_shape.Draw("colZ")
    c3.SaveAs("nll_2D_shape.png")
    nll_values_2D_shape.Write()
#vediamo che ha una forma diagonale perchè è legato al fatto che s+b
#sono al 100% anticorrelate. Le rette sono le superfici equiprobabilit e i triangolini
#sono i valori in cui non riesce a calcolare la likelihood perhcè è troppo bassa per la precisione 
#numerica che abbiamo
#1400 sono 1400 ordini di grandezza! non è scontato che riesca a fare sta valutazione, il minimo sarà da qualche parte lungo questa retta. 
#La cosa importante è che capimao che la poissoniana ci aiuta.

#ci metterà una vita perchè deve girare su tutti gli s e tutti i b
#Sarà un equivalente del plot 1d ma in 2d mi aspetto una concavità. Se i parametri fossero
#scorrelati ma se sono scorrelati allora sarà un ellisse in cui gli assi non sono uguali ma sono
#sono paralleli a asse x e y, nell'estremo la correlazione sarà una retta in cui sono al 100% correlati
#la maniera + intelligente è farlo per step di 10 o 5 s e b perchè altrimenti ci vuole troppo tempo epr falro.

#Osserviamo nel grafico 2D_shape che ci sono delle zone che sono quelle che hanno la stessa probabilità in qeusta scala z
#notiamo che ci sono dei valori concentrici di probabilità. 

#Vediamo che il plot "lego" somgilia a quello 1D che abbiamo visto prima.

#Il plot lego sembra a uqello che abbiamo fatto 1D, quindi è come se fosse la sua versione
#bidimensionale. Ci sono delle zone con stesso colore che sono le zone di isoprobabili.
#Succede che facendo il grafico colz vedi degli ellissi che diventano valori più bassi 
#man manco hce sono + verdi quindi il minimo sta dove sta il verde e vediamo che  è 
#circa 80 per il segnale e 850 - 80 per il fondo. Ovviamenre è una stima grossolana poi
#Andrebbe cerctao nel ciclo il minimo

#Una variazione un'unità sulla likelihood dobbiamo variare sull'asse z di uno,
#i bin osono dell'ordine di 500 rispetto delta L quindi è impossibile vedee l'errore dal grafico
#dobbiamo fare uno scan molto più fitt.abs#Abbimao una forma di questo tipo in 2D che possiamo usare per proeittare la parabola in 2 dimensioni

#Se il minimo del segnale sta a 80 mi aspetto che il minimo del fondo stia a 850-80
#Questo perchè il temrine poissoniano obbliga la forma a stare sulla diagonale.abs
#La poissoniana preferisce che s+b siano sulla diagonale perchè questi sono i casi
#in cui il dataset sta sulla diagonale
#quindi se s+b è diverso da 850 il pezzo di likelihood che proviene dalla poissoniana
#darà un +1400 e quindi cerca di sfavorirlo.
#La parte di shape varia fino a 16mila circa quindi fa lei laparte da leone. quindi poisson mi forza il numero di eventi a stare nella regione
#però non sarà così tanto potente.
#Per questo non necessariamente s+b = 850 perchè magari il termine additivo di poisson non è altrettanto forte quanto quello di shape. 

#Adesso vogliamo passare una likelihood binnata, dobbiamo trasformare la funzione di probabilità o in una multinomiale o in un prodotto di tante
#poissoniana, una per ogni bin in cui ognuna è centrata attorno il valore di aspettazion
#Ci conviene avere il contenuto non evento per evento ma raccolto in dei bin. 
#Noi avevamo messo i nostri eventi nell'histogramma e avevamo preso l'array binnato, che è un array
#costruito dal contenuto dell'istogramma.

pois_bin = ROOT.TF1("Poisson_bin", "TMath::Poisson(x,[0])", 0, N_events) 
#Questa è la possoniana che usamo bin per bin
nsplit = 10
nll_values_2D_shape_binned = ROOT.TH2F("nll_values_2D_shape_binned","nll_values_2D_shape_binned",int(N_events/nsplit),0,N_events, int(N_events/nsplit), 0, N_events)

if do_simple_scan:
    for s in range(0,N_events, int(nsplit)):
        for b in range(0, N_events, int(nsplit)):
            #Dobbiamo fare un loop sui bin e possiamo farlo in due modi.
            #O scriviamo una poissoniana davanti e poi ci calcoliamo l'epsilon_i/n_i fattoriale (vedi teoria)
            #o facciamo la produttoria di tante poissoniana
            fgefrac.SetParameters(800,50,200,s,b)
            nll = 0
            print((s,b))
            for i in range(len(xbinned_array)):
                x_data = xbinned_array[i]
                x_i_min = h3.GetBinLowEdge(i)
                x_i_max = h3.GetBinLowEdge(i+1)
                #Se l'istogramma arriva alla fine dei bin lui si prende il bin id "overflow", 
                #ossia quello che contiene tutto quello che è rimasto fuori quando abbiamo riempito l'istogramma. 
                #così come il bin al di sotto ti fanno l'underflow ossia tutto quello che è riempito
                #alla fine dell'asse.
                epsilon_i = fgefrac.Integral(x_i_min, x_i_max)
                #epsilon_i quanto vale? epsilon è l'integrale della funzione di probabilità all'interno
                #degl estremi del bin quindi se ho una distribuzione di probabilità come in questo caso devo farne 
                #l'integrale da zmin e xmax e questa è la probabilità di avere un evento all'interno
                #di quel bin.
                #Invece di calcolarcela punto per punto ci facciamo l'integrale fra gli estremi del bin.
                nu_i = (s+b)*epsilon_i
                #I parametri della poissoniana come li settiamo
                pois_bin.SetParameter(0,nu_i)
                pois_i = pois_bin.Eval(x_data)
                #quindi poi valuto la poissoniana nel contenuto del bin i-esimo
                
                nll_i =0
                if pois_i != 0:
                    nll_i = -2*math.log(pois_i)
                else:
                    nll_i =  10000
                    #Se la poissoniana del bin viene zero non posso mettere come contributo alla likelihood zero
                    #Questo ci va ad abbassare la nll, se ci mettiamo zero non sto scartando quel bin ma lo
                    #sto favorendo. Sto dando un valore buono ad aeventi cattivi
                    #Noi vogliamo che -2log () dovrebbe essere infinito. 
                    #Nel caso di prima abbiamo risolto senza proprio riempire, perchè stavamo calcolando una sola poissoniana
                    #in questo caso siccome stiamo sommando tanti pezzi se al pezzo non virtuoso ci metto 0 lo sto aiutando in qualche modo
                    #Prima la poisosnaian era quella di tutti gli eventi e il valore minimo si aveva per s+b = n. Man mano che mi allontano i valori salgono
                    #quelli che stavano nell'angolino sono punti in cui la nll esplode e quello che noi abbiamo fatto è stato proprio toglierli da mezzo, non considerarli. 
                    #Perchè hanno dei valori che altrimenti sarebbero infinito
                    #Adesso noi stiamo facendo la somma di tante poissoniane piccole, un pezzetto per ogni bin. 
                    #Se noi ai pezzi che esplodono ci sommiamo 0 allora  0 è un valore virtuoso non un valore che esplode
                    #Nella somma li stiamo premiando!   
                if (s == 80 and b == 770):
                    print('bin is', i, 'xmin', x_i_min, 'xmax', x_i_max,'nu is', nu_i, 'epsilon is', epsilon_i)
                nll += nll_i    
            nll_values_2D_shape_binned.SetBinContent(int((s+1)/nsplit), int((b+1)/nsplit), nll)

    # A questo punto sostituiamo in ognuno di questi bin la poissoniana e 
    c3 = ROOT.TCanvas()
    nll_values_2D_shape_binned.Draw("colZ")
    c3.SaveAs("nll_values_2D_shape_binned.png")
    nll_values_2D_shape_binned.Write()

#Si vede bene il minimo intorno a 80 e intorno a 750. Questo non è un bene
#questo m dice che sono in grado di vedere i vari step della funzione di verosimiglianza molto di più rispetto l'altro caso!
#Ha degli step di likelihood abbastanza rapidi, riusciamo a vedere lo step da 450 a 460 fino a 500. Questo valore è il valore 
#della negative log likelihood quidni sono gli stepp della funzione di liejlihood
#In questo cas l'altezza della parabola è più bassa ma un'altezza minmore significa che l'intervallo
#attorno al parametro s che corrisponde a una Delta L di 1 è più grande quindi ho un errore maggiore
#Nel caso unbinned succede invece che il Delta L corrisponde a un errore sul parametro minore
#Quindi se le due parabole corrispondono allo stesso valore del segnale s avere un
#escursione piccola intorno al minimo non è bene, mi dà un errroe maggiore!
#E' quello che mi aspetto perchè la versione binnata perde di informazione rispetto quella unbinned!

#Altra cosa da notare è che il lopp x_binned è più veloce perchè non loopa su 800 eventi ma sul numero dei bin ma il numero dei bin
#Se sono 850 ci ridurrà il tempo. 

#sicocme avevamo la forma funzionale Esatta in questo caso non c'è una vera motivazione per 
#usare l'unbinned rispetto la binned. La binned l'unica cosa positiva che ha è il tempo di calcolo
#Ma permette anche di "integrare" su qualche effetto di calcolo sistematico però di principio sto comunque 
#perdendo informazione. 


#Vogliamo usare il teorema di Wilk per marginalizzare alcuni die parametri.
#Per ogni valore del nostro scan dovremo effettuare dei fit diversi. 
#Avrà al numeratore la likelihood massimizzata fissando s, avremo a questo punto m-1 parametri e su questi massimizziamo
#al denominatore c'è il termine che ci dà la base del parabloide, il valore di partenza, Che è il vlaore di verosimiglianza
#massimizzato in funzione di tutti i parametri. 

#Per tutte le figure che abbiamo visto il valore del minimo non è in zero perchè
#per avere il max della likelihood bisogna massimizzare su TUTTI i parametri 
#e in questo caso non lo abbiamo fatto abbiamo massimizzato intorno s e b però l'abbiamo fatto in maniera iterativa fissando gli altri a valori arbitrari
#dati dalla nostra conoscenza esterna del modello. 


do_profile = True
#la lambda avrà la distribuzione di un chi quadro di ordine 2, per semplicità però
#facciamo il profile solo attorno a s
if do_profile:
    nllratio_values_profile = ROOT.TH1F('nllratio_values_profile', 'nllratio_values_profile', N_events, 0, N_events)
    #C'è un aspetto importante: noi prima abbiamo fittato solo il termine di shape, non abbiamo
    #fatto il fit al pezzo poissoniano quindi per ora facciamo solo la parte di shape
    #aBBIAMO bisogno del valore max della likelkihood su tutti i  parametri.
    #Prendo i valori dei parametri che arrivano dal fit complessivo

    #Calcoliamo la likelihood complessiva su tutti i parametri
    pois = ROOT.TF1("Nevents", "TMath::Poisson(x, [0])", 0, 3*N_events)
    #Aumentiamo il range della funzione altrimenti è un apoissoniana talgiata
    #I parametri ce li prendiamo dal fit di sopra.
    mean_v= fge.GetParameter(0) #valore centrale gaussiana dal fit "totale"
    sigma_v= fge.GetParameter(1) #valore sigma gaussiana dal fit "totale"
    lambda_v= fge.GetParameter(2) #valore lambda esponenziale dal fit "totale"
    s_v =fge.GetParameter(3) #valore segnale dal fit "totale"
    b_v =fge.GetParameter(4) #valore fondo dal fit "totale"
    #Sono i valori migliori che lui trova per il numeor di eventi del segnale e del fit. 
    #Troviamo dei valori strani perchè? PErchè lui mi restituisce un valore tale che 
    #l'integrale complessivo della funzione non è uguale al numero di eventi, il valore che mi compara
    #è il valore al centro del bin. 
    #ROOT di suo quando fa il fit compara il valore centrale della funzione e quidni l'integrale della funzione
    #non è il nuemero di entries ma è il valore migliore della funzione che passa per il valore centrale
    #Root è come se facesse il fit punto per punto al centro dell'istogramma e non fitta
    #il termine poissoniano.
    #Lui confornta il valore centrale del punto con il valore centrale della funzione che fitta
    #però non pesa questa cosa con dei termini poissoniani.
    
    pois.SetParameter(0, s_v+b_v)
    lik_pois_max = pois.Eval(N_events)
    nll_pois_max = -2*math.log(lik_pois_max)

    fgefrac.SetParameters(mean_v, sigma_v, lambda_v, s_v,b_v)
    nll = 0
    likelihood_value = 1

    for xi in x_array:
        value_xi = fgefrac.Eval(xi)
        likelihood_value = likelihood_value*value_xi
        nll = nll -2*math.log(value_xi)
    
    print('max likelihood value is:', nll+nll_pois_max ,'; poisson part is: ', nll_pois_max, '; p.d.f. part is: ', nll )

    max_nll = nll + nll_pois_max
    #PEr ognuno degli eventi dobbiamo fare il fit complessivo, poi fissare il parametro s 
    #e poi procedere con il fit e fare la nll per quel valore di s

    #Adesso dobbiamo modificare il valore di s e vedere cosa succede. PEr ognuno dei valori di s
    #Dobbiamo rifare il fit. 
    for s in range(0, N_events):
        fge.SetParameters(780, 50, 200, 70, 870, 850)
        fge.FixParameter(5, 850)
        fge.FixParameter(3,s)
        h3.Fit(fge.GetName(), "LEMSQ")
        #Gli mettiamo la L in modo che lui faccia il fit con la verosimiglianza e non 
        #con il chi2.
        #Cosa importante: noi facciamo il fit alla funzione binnata prendendo i parametri
        #dall'unbinned. Questa cosa potrebbe essere un problema ma manco eccessivamente

        mean_v= fge.GetParameter(0) #valore centrale gaussiana dal fit "totale"
        sigma_v= fge.GetParameter(1) #valore sigma gaussiana dal fit "totale"
        lambda_v= fge.GetParameter(2) #valore lambda esponenziale dal fit "totale"
        s_v =fge.GetParameter(3) #valore segnale dal fit "totale"
        b_v =fge.GetParameter(4) #valore fondo dal fit "totale"

        pois.SetParameter(0, s_v+b_v)
        lik_pois_max = pois.Eval(N_events)

        doSkip = False
        if(lik_pois_max >=0):
            nll_pois_s = -2*math.log(lik_pois_max)
        else:
            doSkip = True

        fgefrac.SetParameters(mean_v, sigma_v, lambda_v, s_v,b_v)
        nll = 0
        likelihood_value = 1

        for xi in x_array:
            value_xi = fgefrac.Eval(xi)
            if(value_xi <= 0):doSkip = True
            if(doSkip):continue

            likelihood_value = likelihood_value*value_xi
            nll = nll -2*math.log(value_xi)
        if doSkip:
            continue
        
        print('s is: ', s, 'max likelihood value is: ',nll + nll_pois_s,'poisson part is: ', nll_pois_s, 'p.d.f. part is: ', nll)  
        nllratio_values_profile.SetBinContent(s, nll+nll_pois_s - max_nll)
        #print('max likelihood value is:', nll+nll_pois_max,  '; poisson part is: ', nll_pois_max, '; p.d.f. part is: ', nll )
    c4 = ROOT.TCanvas()
    nllratio_values_profile.Draw()
    c4.SaveAs('nllratio_values_profile.png')
    nllratio_values_profile.Write('nllratio_values_profile_signal')
    #Lui invece di salvarlo con il nome che ha lo salva con il nome che gli ho messo 
    #tra le parentesi
    #Resettiamo l'istogramma per riutilizzarlo successivamente
    nllratio_values_profile.Reset("ICES")
    #Questa serve a svuotare l'istogramma
    for mass in range(0,1000):
    
        fge.SetParameters(780,50,200,70,870,850)
        fge.FixParameter(5,850)
        fge.FixParameter(0,mass)
        h3.Fit(fge.GetName(),"LEMSQ")
        
        mean_v= fge.GetParameter(0) #valore centrale gaussiana dal fit "totale"
        sigma_v= fge.GetParameter(1) #valore sigma gaussiana dal fit "totale"
        lambda_v= fge.GetParameter(2) #valore lambda esponenziale dal fit "totale"
        s_v =fge.GetParameter(3) #valore segnale dal fit "totale"
        b_v =fge.GetParameter(4) #valore fondo dal fit "totale"

        print()
        
        pois.SetParameter(0,s_v+b_v)
        lik_pois_max = pois.Eval(N_events)
        doSkip=False
        if(lik_pois_max>=0):
                nll_pois_m = -2 * math.log(lik_pois_max) 
        else:
                doSkip=True
        fgefrac.SetParameters(mean_v,sigma_v,lambda_v,s_v,b_v)#componente "continua"
        
        nll = 0
        likelihood_value=1
        #print (" signal hypothesis is s = " +str(s))
        
        for xi in x_array:
                value_xi = fgefrac.Eval(xi)
                if(value_xi<=0):doSkip=True
                if(doSkip):continue
                likelihood_value= likelihood_value*value_xi
                nll = nll -2 * math.log(value_xi)
                #print("xi is ", xi, " pdf is ", value_xi," nll ", nll )

        if doSkip:
                continue
        print("m is ",mass," max likelihood value is: ", nll+nll_pois_m," ; poisson part is ", nll_pois_m, " ; p.d.f. part is: ", nll)              
        nllratio_values_profile.SetBinContent(mass,nll+nll_pois_m - max_nll)
        #per ognuno di questi valori del parametro cosa devo fare?

        #dobbiamo prendere il valore della massima verosimiglianza facendo il fit fissato s


    c5 = ROOT.TCanvas()
    nllratio_values_profile.Draw()
    c5.SaveAs("nllratio_values_profile_mass.png")
    nllratio_values_profile.Write("nllratio_profile_values_mass")
    

#facciamo il draw e il saveas. Dopodichè facciamo il write nel file root.
#Il minimo non è esattamente a zero questo perchè il fit che abbiamo fatto non è alla
#stessa quantità perchè la likelihood è unbinned ma il fit lo abbiamo fatto alla distribuzione binnata
#Ora Noi abbiamo fatto il fit alla funzione binned, istogramma, e costruito la funzione unbinned usando i parametri
# #ottenuti dalla binned. 
#Può succedere che il minimo dell'unbinned sia diverso dalla binned, se ci fosse una grande differenza
#questo minimo potrebbe essere shiftata. 
#Se facciamo zoom vediamo che il delta L = 1 corrisponde a un errore di circa 10 sul parametro s

#Vediamo che non è esattamente simmetrico e che se ci allontaniamo dal minimo
#vediamo delle cose strane. perchè quella è una minimizzazione rispetto a piu parametri
#E come se ci fossero + possibili minimi, più valli, nello spazio multidimensionale
#quella cosa strana è  quando passiamo da una valle all'altra(?)
#Vediamo delle distribuzioni spezzatate perchè noi vediamo tante vallate in piu parametri.
#tra 250 e 273 lui ha dei problemi mentali e questi porblemi si thanno proprio dove sta la transizione. 
#Ha finito e passa alla nuova distribuzione
#Li lui salta tra due minimi relativi chhe noi non vediamo perchè stiamo facendo il profile
#rispetto un solo parametro.

#Processo che si può fare anche rispetto ai èparametri di nuisance e verifichiamo
#se effettivamente il minimo in cui ci troviamo è gaussiano in tutti quanti oppure 
#può capitare che se abbiamo una dipendenza molto debole da un parametro la gaussiana diventa molto larga
#Rischio di trovarmi in un regime in cui la likelihood non è gaussian -> irregolarità al variare del parametro -> minimo ballerino
#tipicamnte lo si fa come sanity check.

#Quello della massa ha una faccia diversa. 
#Vedete che per valori bassi di massa la likelihood ha valori a caso e dopo ha una forma gaussiana
#Nemmeno qui è perfettamente intorno allo zero ma è ragionevolmente vicino, l'errore che vediamo è circa
#790 pm 8 e vediamo che ci troviamo più o meno nel fit viene 5
#La distribuzione qua non ci azzecca niente con la parabola appena mi allontano dal picco, 
#cambia addirittura la concavità
#Si può fare per tutti i parametri, se dipendenza debole -> da subito non sono in regime gaussiano
#quindi anche stima errore sbagliata

outfile.Close()








