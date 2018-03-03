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
		#numero arametri
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
		
		for i in range(100):
			gMinuit.mnseek() # al posto di MIgrad usare Simplex mnsimp() o mnseek() ancora piu scemoc 
		
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
			
		f[0]  = funzione_differenza("TreeS",pesi,"segnale")
		f[0] += funzione_differenza("TreeB",pesi, "fondo") 


# creo la funzione che deve essere minimizzata
# passo anche il tipo di dato che gli sto passando
def funzione_differenza(fname,pesi,dato):
		global npar
		n = file_len(fname)
		f = open(fname)
		funzione_minimizzare = 0
				
		xlambda = 0.1
		no_ovt = 0
		for i in range(6+2):
			for j in range(4):
				no_ovt += pesi[i*4+j]*pesi[i*4+j]
				
		for j in range(n/6):
			if (j < int((n/6)*(2.0/3.))):
				var = [float(strip(f.readline())) for i in range(6)]
				if(dato == "segnale"):
					funzione_minimizzare +=	(funzione_output_2_layer(var,pesi)-1)**2
				elif(dato == "fondo"):			
					funzione_minimizzare += (funzione_output_2_layer(var,pesi))**2

		
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
			if (m < int((n/6.0)*(2./3.))):
				histogram_training_segnale.Fill(funzione_output_2_layer(var,pesi))
			else:
				histogram_test_segnale.Fill(funzione_output_2_layer(var,pesi))
			
				
		if(dato == "fondo"):
			if (m < int((n/6.0)*(2./3.))):
				histogram_training_fondo.Fill(funzione_output_2_layer(var,pesi))
			else:
				histogram_test_fondo.Fill(funzione_output_2_layer(var,pesi))
				
		
		if(dato == "data"):
			a = float(strip(massa.readline()))
			b = funzione_output_2_layer(var,pesi)
			histogram_data.Fill(b)
			if (b >= 0.98):
				#if (a > 4920):
				histogram_massa_ricercata.Fill(a)
				
	 	
	massa.close()
	f.close()	
	
		
# funzione di attivazione 
def sigmoide(x):
	
		sigm  = (arctan(x) + pi/2.0)/pi
		return sigm
	
	
	
	
# funzione da minimizzare  pesi li creo a caso ne creo una ventina di set 
# e ne trovo il minimo di questi set e poi pesito da li per minimizzare 
def funzione_output_1_layer(var,pesi):
	
		output_rete = 0
		# il ciclo va per ogni elemento di var
		# cioè gira per ogni nodo
						
		for i in range(4):
			input_sigmoide = 0
		# il ciclo gira su ogni elemento del livello nascosto
		# che scelgo come dimensione uguale al primo livello
		
			for j in range(6):
				input_sigmoide += pesi[i*4 + j] * var[j]

			# invece di prendere la la prima colonna e iterare sulle righe 
			# (cioé prendo la prima colonna per intero)
			# prendo la penultima 
			input_sigmoide += pesi[i+24]
			valore_di_attivazione = sigmoide(input_sigmoide)
			# invece di prendere la prima riga e iterare sulle colonne
			# (ovvero la prima riga intera)
			# prendo l'ultima 
			output_rete += pesi[28+i] * valore_di_attivazione
			# da un punto di vista computazionale non è un problema perché 
			# tanto sono parametri. Il punto 00 non lo prendo mai quindi no problem
			
		
		return output_rete 
		
		
def funzione_output_2_layer(var,pesi):
	
	output_rete = 0
	input_sigmoide = 0 
	
	for i in range(2):
		for j in range(4):
			input_sigmoide += pesi[32 + 4*i +j] * sigmoide(funzione_output_1_layer(var,pesi))
		valore_attivazione = sigmoide(input_sigmoide)
		output_rete += pesi[39 + i]*valore_attivazione
	
	return output_rete
	
def ROC(pesi):
	
	#la lunghezza di segnale e fondo sono uguali quindi ne prendo uno solo
	n_S = file_len("TreeS")
	f_S = open("TreeS")
	
	n_B = file_len("TreeB")
	f_B = open("TreeB")
	
	passo = 0.001
	gruppo_vero = [None]*int(1.0/passo)
	gruppo_falso = [None]*int(1.0/passo)
	indice = 0
	
	for t in arange(0,1,passo):
		# di fatto solo i vero pos e neg sono quando la rete azzecca 
		vero_pos = 0
		falso_pos = 0
		falso_neg = 0
		vero_neg = 0
		
		#mi interessa solo il training set
		for m in range(int((n_S/6)*(2./3.))):	
			var_S = [float(strip(f_S.readline())) for i in range(6)]
			
				
			if (funzione_output_2_layer(var_S,pesi) > t):
				vero_pos += 1	
			else:
				falso_neg += 1
		
		for z in range((n_B/6)/2):
			var_B = [float(strip(f_B.readline())) for h in range(6)]
			
			if(funzione_output_2_layer(var_B,pesi) > t):
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
				
		
		pesi = [1]*42
		npar = len(pesi)
		minimo =  funzione_differenza("TreeS",pesi,"segnale") + funzione_differenza("TreeB",pesi,"fondo")
		for i in range(100):
			peso = [uniform(-10,10) for j in range(42)]
			f_min = funzione_differenza("TreeS",peso,"segnale") + funzione_differenza("TreeB",peso,"fondo") 
			if(f_min < minimo):
				minimo = f_min
				pesi = peso
			
		
		pesi_minimizzati = testfit(pesi)			
		
		comp("TreeS",pesi_minimizzati,"segnale")
		comp("TreeB",pesi_minimizzati,"fondo")
		comp("Data",pesi_minimizzati,"data")
		
		ROC(pesi_minimizzati)
		
		c1 = TCanvas()
		c2 = TCanvas()
		c3 = TCanvas()
		c4 = TCanvas()
		c5 = TCanvas()
		
		c1.Divide(2,1)
		#c2.Divide(2,2)
		
		c1.cd(1)          
		
		histogram_training_segnale.GetXaxis().SetTitle("Output rete")
		histogram_training_segnale.Draw()
		histogram_training_fondo.SetLineColor(2)
		histogram_training_fondo.Draw("SAME")
		
		c1.cd(2)
		
		histogram_test_segnale.GetXaxis().SetTitle("Output rete")
		histogram_test_segnale.Draw()
		histogram_test_fondo.SetLineColor(2)
		histogram_test_fondo.Draw("SAME")
		
		c2.cd()
		histogram_test_segnale.Draw()
		histogram_training_segnale.SetLineColor(7)
		histogram_training_segnale.Draw("SAME")
		
		c5.cd()
		histogram_data.GetXaxis().SetTitle("Output rete")
		histogram_data.Draw()
		
		'''
		c2.cd(3)
		
		histogram_massa.GetXaxis().SetTitle("Massa")
		histogram_massa.GetYaxis().SetTitle("Entrate")
		histogram_massa.Draw()
		'''
		
		c3.cd()
		f = TF1 ("fit","[0]*exp(-0.5*((x-[1])/[2])**2) + exp([3] + [4]*x)",5000,5600)
		f.SetParameter(0,30)
		f.SetParameter(1,5360)
		f.SetParameter(2,10)
		f.SetParameter(3,40)
		f.SetParameter(4,-0.3)
		histogram_massa_ricercata.GetXaxis().SetTitle("Massa [GeV/c^2]")
		histogram_massa_ricercata.GetYaxis().SetTitle("Entrate")
		histogram_massa_ricercata.Draw("PE")
		histogram_massa_ricercata.Fit("fit","R")
		
		
		c4.cd()
		
		
		ROC_gr.SetMinimum(0.)
		ROC_gr.SetMaximum(1.1)
		ROC_gr.SetTitle("Curva ROC")
		ROC_gr.GetXaxis().SetTitle("Percentuale falsi positivi")
		ROC_gr.GetYaxis().SetTitle("Percentuale veri positivi")
		ROC_gr.Draw("AC")
		
		diag = TF1("diagonale","x",-0.1,1)
		diag.Draw("SAME")
		
		gApplication.Run()
		
		
		
		
		

		
		
		
