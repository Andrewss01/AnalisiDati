from scipy.stats import poisson, binom, expon
import ROOT
import math
import matplotlib.pyplot as pls
import os 

#Partiamo da alcuni parametri
e_init = 10
e_lambda = 50 
res_sigma = 5
events = 200
nrebin = 10

initdir =  "energy_resolution_dir"
if not os.path.exists(initdir):
    os.system("mkdir " + initdir)

#Abbiamo creato una cartella dicendogli che se non trova la directory
#La deve creare lanciando il comando mkdir nella shell di comando. 

#A questo punto creiamo l'esponenziale

exp1 = ROOT.TF1("exponential", "1/[0]*exp(-(x-[1])/[0])", 10, 200)
exp1.SetParameters(e_lambda, e_init)

res = ROOT.TF1("resolution", "1/sqrt([1]*TMath::Pi())*exp(-((x-[0])*(x-[0]))/(2*[1]*[1]))",-200,200)
res.SetParameter(0,0)
res.SetParameter(1, res_sigma)

c1 = ROOT.TCanvas("")
exp1.Draw()
prefix = "_l_" + str(e_lambda) + "_s_"+str(res_sigma)+"_n_"+str(events)
if nrebin != 1:
    prefix = prefix + "_rebin_" + str(nrebin)

c1.SaveAs(initdir+"/exponential_"+prefix+ ".png")

res.Draw()
c1.SaveAs(initdir+"/resolution_"+prefix+".png")

#Adesso vogliamo effettuare la generazione. Prima per ognuno degli eventi, 
# (in questo caso abbiamo scelto 200), devo generare secondo la distribuzione originaria
#e poi centrare la gaussiana nel valore E_09 che ho preso 
GenSample = ROOT.TH1F("GenSample", "Generated Sample", 190, 10, 200)

for i in range(events):
    e0 = exp1.GetRandom()
    res.SetParameter(0, e0)
    e1 = res.GetRandom()
    GenSample.Fill(e1)

if nrebin !=1:
    GenSample.Rebin(nrebin)

GenSample.Draw()
c1.SaveAs(initdir+"/data_l_"+ prefix+ ".png")

GenSample.Draw("e")
c1.SaveAs(initdir+"/data_witherror_l_"+prefix+".png")

