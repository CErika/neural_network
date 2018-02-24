# script per normalizzare le variabili in entrata alla rete neurale
from ROOT import *
import numpy
import sys


histogram_len_norm = TH1D("LEN","",100,0,0)

if (len(sys.argv) != 5):
	sys.exit("Servono quattro argomenti da riga di commando in questo ordine: il nome del file, file di training, file di test e il file di dati")
	
file_name = sys.argv[1]
training = sys.argv[2]
test = sys.argv[3]


# apro il file di dati
rootfile = TFile.Open(file_name,'read')

treeS     = TTree()
rootfile.GetObject(training,treeS)

rootfile2 = TFile.Open(file_name,'read')
treeB = TTree()
rootfile2.GetObject(test,treeB)

rootfile1 = TFile.Open(file_name,'read')
Datas = sys.argv[4]
data = TTree()
rootfile1.GetObject(Datas, data)

# riempo degli array con i dati dei vari file e poi uso le funzioni mean e std di numpy
# TreeS
nS = treeS.GetEntries()
S_Len = [None]*nS 
S_IP_B1 = [None]*nS
S_IP_B2 = [None]*nS
S_IP_A = [None]*nS
S_Pt = [None]*nS
S_MinDist = [None]*nS

n = 0
for event in treeS:
	S_Len[n] = event.Len
	S_IP_B1[n] = event.IP_B1
	S_IP_B2[n] = event.IP_B2
	S_IP_A[n] = event.IP_A
	S_Pt[n] = event.Pt
	S_MinDist[n] = event.MinDist
	n += 1
	
mediaS_Len = numpy.mean(S_Len)
devS_Len = numpy.std(S_Len)
print mediaS_Len
mediaS_IP_B1 = numpy.mean(S_IP_B1)
devS_IP_B1 = numpy.std(S_IP_B1)

mediaS_IP_B2 = numpy.mean(S_IP_B2)
devS_IP_B2 = numpy.std(S_IP_B2)

mediaS_IP_A = numpy.mean(S_IP_A)
devS_IP_A = numpy.std(S_IP_A)

mediaS_Pt = numpy.mean(S_Pt)
devS_Pt = numpy.std(S_Pt)

mediaS_MinDist = numpy.mean(S_MinDist)
devS_MinDist = numpy.std(S_MinDist)

# TreeB

nB = treeB.GetEntries()
B_Len = [None]*nB 
B_IP_B1 = [None]*nB
B_IP_B2 = [None]*nB
B_IP_A = [None]*nB
B_Pt = [None]*nB
B_MinDist = [None]*nB

m = 0
for event in treeB:
	B_Len[m] = event.Len
	B_IP_B1[m] = event.IP_B1
	B_IP_B2[m] = event.IP_B2
	B_IP_A[m] = event.IP_A
	B_Pt[m] = event.Pt
	B_MinDist[m] = event.MinDist
	m +=1 
	
mediaB_Len = numpy.mean(B_Len)
devB_Len = numpy.std(B_Len)

mediaB_IP_B1 = numpy.mean(B_IP_B1)
devB_IP_B1 = numpy.std(B_IP_B1)

mediaB_IP_B2 = numpy.mean(B_IP_B2)
devB_IP_B2 = numpy.std(B_IP_B2)

mediaB_IP_A = numpy.mean(B_IP_A)
devB_IP_A = numpy.std(B_IP_A)

mediaB_Pt = numpy.mean(B_Pt)
devB_Pt = numpy.std(B_Pt)

mediaB_MinDist = numpy.mean(B_MinDist)
devB_MinDist = numpy.std(B_MinDist)

# Data

nD = data.GetEntries()
D_Len = [None]*nD 
D_IP_B1 = [None]*nD
D_IP_B2 = [None]*nD
D_IP_A = [None]*nD
D_Pt = [None]*nD
D_MinDist = [None]*nD

l = 0
for event in data:
	D_Len[l] = event.Len
	D_IP_B1[l] = event.IP_B1
	D_IP_B2[l] = event.IP_B2
	D_IP_A[l] = event.IP_A
	D_Pt[l] = event.Pt
	D_MinDist[l] = event.MinDist
	l += 1
	

mediaD_Len = numpy.mean(D_Len)
devD_Len = numpy.std(D_Len)

mediaD_IP_B1 = numpy.mean(D_IP_B1)
devD_IP_B1 = numpy.std(D_IP_B1)

mediaD_IP_B2 = numpy.mean(D_IP_B2)
devD_IP_B2 = numpy.std(D_IP_B2)

mediaD_IP_A = numpy.mean(D_IP_A)
devD_IP_A = numpy.std(D_IP_A)

mediaD_Pt = numpy.mean(D_Pt)
devD_Pt = numpy.std(D_Pt)

mediaD_MinDist = numpy.mean(D_MinDist)
devD_MinDist = numpy.std(D_MinDist)

# scrivo i file con i dati normalizzati
with open("TreeS",'w') as f:
	for event in treeS:
		f.write(str((event.Len - mediaS_Len)/devS_Len) + "\n")
		histogram_len_norm.Fill((event.Len - mediaS_Len)/devS_Len)
		f.write(str((event.IP_B1 - mediaS_IP_B1)/devS_IP_B1) + "\n")
		f.write(str((event.IP_B2 - mediaS_IP_B2)/devS_IP_B2) + "\n")
		f.write(str((event.IP_A - mediaS_IP_A)/devS_IP_A) + "\n")
		f.write(str((event.Pt - mediaS_Pt)/devS_Pt) + "\n")
		f.write(str((event.MinDist - mediaS_MinDist)/devS_MinDist) + "\n")

with open("TreeB",'w') as f:
	for event in treeB:
		f.write(str((event.Len - mediaB_Len)/devB_Len) + "\n")
		f.write(str((event.IP_B1 - mediaB_IP_B1)/devB_IP_B1) + "\n")
		f.write(str((event.IP_B2 - mediaB_IP_B2)/devB_IP_B2) + "\n")
		f.write(str((event.IP_A - mediaB_IP_A)/devB_IP_A) + "\n")
		f.write(str((event.Pt - mediaB_Pt)/devB_Pt) + "\n")
		f.write(str((event.MinDist - mediaB_MinDist)/devB_MinDist) + "\n")
		
with open("Data",'w') as f:
	for event in data:
		f.write(str((event.Len - mediaD_Len)/devD_Len) + "\n")
		f.write(str((event.IP_B1 - mediaD_IP_B1)/devD_IP_B1) + "\n")
		f.write(str((event.IP_B2 - mediaD_IP_B2)/devD_IP_B2) + "\n")
		f.write(str((event.IP_A - mediaD_IP_A)/devD_IP_A) + "\n")
		f.write(str((event.Pt - mediaD_Pt)/devD_Pt) + "\n")
		f.write(str((event.MinDist - mediaD_MinDist)/devD_MinDist) + "\n")

with open("MassaData",'w') as f:
	for event in data:
		f.write(str(event.Mass) + "\n")
		
c1 = TCanvas()

c1.cd()
histogram_len_norm.Draw()
gApplication.Run()

