# -*- coding: utf-8 -*-
from ROOT import *
from array import array
from random import uniform
from numpy import exp,arctan,arange,clip
from math import pi,tanh,sqrt
from string import strip
	
	

histogram_test_fondo = TH1D("test","",100,-1,2)
histogram_test_segnale = TH1D("test","",100,-1,2)
histogram_training_fondo = TH1D("training","",100,-1,2)
histogram_training_segnale = TH1D("training","",100,-1,2)
histogram_data = TH1D("data","",1000,0,0)
histogram_massa = TH1D("massa","",1000,0,0)
histogram_massa_ricercata = TH1D("massa ricercata","",100,0,0)
ROC_gr = TGraph()


def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass

	return i + 1

##______________________________________________________________________________
def testfit(pesi):
		global npar
		#numero parametri
		gMinuit = TMinuit(npar) 
		gMinuit.SetFCN(somma_fondo_segnale)
		gMinuit.SetErrorDef(1)
		# non ha molta importanza, visto che l'errore sui parametri della net non sara' comunque
		# considerato
		
# Set starting values and step sizes for parameters
		for i in range(npar):
				gMinuit.DefineParameter( i, "peso " + str(i), pesi[i], 0.1,0,0)
		#gMinuit.DefineParameter(npar,"lambda",pesi[npar - 1],0.1,0,0)
			
	 # Now ready for minimization step
		for i in range(10):
			gMinuit.mnseek() # al posto di MIgrad usare Simplex mnsimp() o mnseek() ancora piu scemoc 
		

		#gMinuit.mnsimp() # al posto di MIgrad usare Simplex mnsimp() o mnseek() ancora piu scemoc 
		gMinuit.Migrad() # al posto di MIgrad usare Simplex mnsimp() o mnseek() ancora piu scemoc 

 # Print results
		
		# vuole come argomento il numero del parametro, dove 
		# salvare il parametro cambiato e dove salvare l'errore cambiato
		pesi_dopo_minimizzazione = [None]*npar
		errore_pesi_dopo_minimizzazione = [None]*npar
		for i in range(npar):
			a = Double(3)
			b = Double(3)
			gMinuit.GetParameter(i,a,b)
			pesi_dopo_minimizzazione[i] = a
			errore_pesi_dopo_minimizzazione[i] = b
		
		
		return pesi_dopo_minimizzazione 


##_creo la funzione che somma fondo e segnale ridati dalla funzione_differenza_____________________________________________________________________________
def somma_fondo_segnale( npar, gin, f, pesi, iflag ):
		'''
		xlambda = 0.15
		no_ovt = 0
		for i in range(6+2):
			for j in range(6):
				no_ovt += pesi[i*6+j]*pesi[i*6+j]
		'''
	
				
		f[0]  = funzione_differenza("TreeS",pesi,"segnale")
		f[0] += funzione_differenza("TreeB",pesi, "fondo") #+ (1.0/2.0)*xlambda*no_ovt 
		#print f[0]


# creo la funzione che deve essere minimizzata
# passo anche il tipo di dato che gli sto passando
def funzione_differenza(fname,pesi,dato):
		global npar
		n = file_len(fname)
		f = open(fname)
		funzione_minimizzare = 0
		
		
		xlambda = 0.15
		no_ovt = 0
		for i in range(6+2):
			for j in range(6):
				no_ovt += pesi[i*6+j]*pesi[i*6+j]
		
		
		for j in range(n/6):
			'''
			n +=1 
			if (n > 100):
				break
			'''
			if (j < (n/6)/2.0):
				var = [float(strip(f.readline())) for i in range(6)]
				if(dato == "segnale"):
					funzione_minimizzare +=	(funzione_output(var,pesi)-1)**2
				elif(dato == "fondo"):			
					funzione_minimizzare += (funzione_output(var,pesi))**2

		#print funzione_minimizzare * (1.0/2.0) + (1.0/2.0)* xlambda * no_ovt
		f.close()
		return funzione_minimizzare * (1.0/2.0) + (1.0/2.0)* xlambda * no_ovt


def comp(fname,pesi,dato):
	
	
	massa = open("MassaData")
	f = open(fname)
	n = file_len(fname)
	ind = 0
	segnale = [None]*(n/12)
	fondo = [None]*(n/12)
	for m in range(n/6):
		var = [float(strip(f.readline())) for i in range(6)]
		if (dato == "segnale"):
			if (m < (n/6.0)/2.):
				histogram_training_segnale.Fill(funzione_output(var,pesi))
			else:
				a = funzione_output(var,pesi)
				segnale[ind] = a
				histogram_test_segnale.Fill(a)
				ind +=1
				
		if(dato == "fondo"):
			if (m < (n/6.0)/2.):
				histogram_training_fondo.Fill(funzione_output(var,pesi))
			else:
				b = funzione_output(var,pesi)
				fondo[ind] = b
				histogram_test_fondo.Fill(b)
				ind +=1
		
		if(dato == "data"):
			
			
			histogram_data.Fill(funzione_output(var,pesi))
			if (funzione_output(var,pesi) > 0.85):
				histogram_massa_ricercata.Fill(float(strip(massa.readline())))
		
	 	
	massa.close()
	f.close()	
	if (dato == "segnale"):
		return segnale
	elif(dato == "fondo"):
		return fondo
		
		
# funzione di attivazione 
def sigmoide(x):
		
		#x = clip(x,-500,500)
		sigm  = (arctan(x) + pi/2.0)/pi
		#sigm = (tanh(x) + 1)/2 # funziona meglio non va in overflow
		#sigm = 1.0/(1 + exp(-x)) #dava errore overlfow numeri troppo grandi per exp
		return sigm
	
	
	
	
# funzione da minimizzare  pesi li creo a caso ne creo una ventina di set 
# e ne trovo il minimo di questi set e poi pesito da li per minimizzare 
def funzione_output(var,pesi):
	
		output_rete = 0
		# il ciclo va per ogni elemento di var
		# cioè gira per ogni nodo
						
		for i in range(len(var)):
			input_sigmoide = 0
		# il ciclo gira su ogni elemento del livello nascosto
		# che scelgo come dimensione uguale al primo livello
		
			for j in range(len(var)):
				input_sigmoide += pesi[i*6 + j] * var[j]

			# invece di prendere la la prima colonna e iterare sulle righe 
			# (cioé prendo la prima colonna per intero)
			# prendo la penultima 
			input_sigmoide += pesi[i+36]
			valore_di_attivazione = sigmoide(input_sigmoide)
			# invece di prendere la prima riga e iterare sulle colonne
			# (ovvero la prima riga intera)
			# prendo l'ultima 
			output_rete += pesi[42+i] * valore_di_attivazione
			# da un punto di vista computazionale non è un problema perché 
			# tanto sono parametri. Il punto 00 non lo prendo mai quindi no problem
			
		
		return output_rete 
		
		
def ROC(pesi):
	
	#la lunghezza di segnale e fondo sono uguali quindi ne prendo uno solo
	n_S = file_len("TreeS")
	f_S = open("TreeS")
	
	n_B = file_len("TreeB")
	f_B = open("TreeB")
	
	passo = 0.01
	gruppo_vero = [None]*int(1.0/passo)
	gruppo_falso = [None]*int(1.0/passo)
	indice = 0
	
	for t in arange(0,1,passo):
		# di fattto solo i vero pos e neg sono quando la rete azzecca 
		vero_pos = 0
		falso_pos = 0
		falso_neg = 0
		vero_neg = 0
		
		#mi interessa solo il training set
		for m in range((n_S/6)/2):	
			var_S = [float(strip(f_S.readline())) for i in range(6)]
			
				
			if (funzione_output(var_S,pesi) > t):
				vero_pos += 1	
			else:
				falso_neg += 1
		
		for z in range((n_B/6)/2):
			var_B = [float(strip(f_B.readline())) for h in range(6)]
			
			if(funzione_output(var_B,pesi) > t):
				falso_pos +=1
			else:
				vero_neg += 1
				
		f_S.seek(0)
		f_B.seek(0)
		
		ROC_gr.SetPoint(indice,falso_pos/float(falso_pos + vero_neg),vero_pos/float(vero_pos + falso_neg))
		indice += 1 
	
	
	f_S.close()
	f_B.close()
	
	
		

##________________________________________________________________________
if __name__ == '__main__':
				
		
		pesi = [1]*48
		npar = len(pesi)
		minimo =  funzione_differenza("TreeS",pesi,"segnale") + funzione_differenza("TreeB",pesi,"fondo")
		for i in range(100):
			peso = [uniform(0,6)/sqrt(2.0/6.0) for j in range(48)]
			f_min = funzione_differenza("TreeS",peso,"segnale") + funzione_differenza("TreeB",peso,"fondo") 
			if(f_min < minimo):
				minimo = f_min
				pesi = peso
			
		
		'''
		print "-------"
		print "-------"
		print pesi
		print minimo
		print "-------"
		print "-------"
		'''
		pesi_minimizzati = testfit(pesi)
		'''
		while abs(errore_NN(pesi_minimizzati,"segnale","training") - errore_NN(pesi_minimizzati,"fondo","test")) > 1 :
			print "-----------------------------"
			print "-----------------------------"
			print errore_NN(pesi_minimizzati,"segnale","training") - errore_NN(pesi_minimizzati,"fondo","test")
			print "-----------------------------"
			print "-----------------------------"
			pesi_minimizzati = testfit(pesi_minimizzati)
		'''
		
		
		with open("MassaData") as massa:
			n = file_len("MassaData")
			for n in range(n):
				histogram_massa.Fill(float(strip(massa.readline())))
		
		
		segnale = comp("TreeS",pesi_minimizzati,"segnale")
		fondo = comp("TreeB",pesi_minimizzati,"fondo")
		comp("Data",pesi_minimizzati,"data")
		
		ROC(pesi_minimizzati)
		
		c1 = TCanvas()
		c2 = TCanvas()
		c3 = TCanvas()
		
		c1.Divide(2,1)
		c2.Divide(2,2)
		
		c1.cd(1)          
		
		histogram_training_segnale.Draw()
		histogram_training_fondo.SetLineColor(2)
		histogram_training_fondo.Draw("SAME")
		
		c1.cd(2)
		
		histogram_test_segnale.Draw()
		histogram_test_fondo.SetLineColor(2)
		histogram_test_fondo.Draw("SAME")
		
		c2.cd(1)
		
		histogram_data.Draw()
		
		
		c2.cd(3)
		histogram_massa.Draw()
		
		c2.cd(4)
		histogram_massa_ricercata.Draw()
		
		
		c3.cd()
		
		
		ROC_gr.SetMinimum(0.)
		ROC_gr.SetMaximum(1.1)
		ROC_gr.Draw("AC")
		
		diag = TF1("diagonale","x",0,1)
		diag.Draw("SAME")
		
		gApplication.Run()
		
		
		
		
		

		
		
		
