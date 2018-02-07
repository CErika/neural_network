# -*- coding: utf-8 -*-
from ROOT import *
from array import array
from random import random
from numpy import exp


	
	






##______________________________________________________________________________
def testfit():

				
		# creo i parametri per la rete 
		# creo parametri per ogni evento
		rootfile = TFile.Open("TMVATest.root",'read')
		tree     = TTree()
		rootfile.ls()
		rootfile.GetObject("TreeS",tree)
	
	
		
	
		'''
		pesi =  [None]*10	
		
		for i in range(10):
		# il secondo for crea gli elementi della lista e il secondo li 
		# riempe creando a sua volta delle liste
		# il secondo array è definito dal numero di input
		# il secondo array è definito dal numero di input
		# mentre il secondo è definito dal numero di neuroni del primo 
		# livello nascosto  	
		'''
		pesi = [random() for j in range(36)]	
		
		
		print pesi
					
		# conto il numero di parametri
		#numero parametri
		gMinuit = TMinuit(36) 
		gMinuit.SetFCN(somma_fondo_segnale)
		gMinuit.SetErrorDef(1)
		# non ha molta importanza, visto che l'errore sui parametri della net non sara' comunque
		# considerato
		
# Set starting values and step sizes for parameters
		for i in range(6):
			for j in range(6):
				gMinuit.DefineParameter( i*6 + j, "peso " + str(i) + " " + str(j), pesi[i*6+j], 0.1,0,0)
			
	 # Now ready for minimization step
		gMinuit.mnsimp() # al posto di MIgrad usare Simplex mnsimpl() o seek 

 # Print results
		
		# voule come argomento il numero del parametro, dove 
		# salvare il parametro cambiato e dove salvare l'errore cambiato
		pesi_dopo_minimizzazione = [None]*36
		errore_pesi_dopo_minimizzazione = [None]*36
		for i in range(36):
			a = Double(3)
			b = Double(3)
			gMinuit.GetParameter(i,a,b)
			pesi_dopo_minimizzazione[i] = a
			errore_pesi_dopo_minimizzazione [i] = b
		
		#f_segnale = funzione_differenza("TMVATest.root","TreeS",pesi,"segnale")
		#f_fondo = funzione_differenza("TMVATest.root","TreeB",pesi, "fondo")
		return pesi_dopo_minimizzazione 







##_creo la funzione che somma fondo e segnale ridati dalla funzione_differenza_____________________________________________________________________________

# pesi vuole un double ma a me serve una matrice, metto un array 
def somma_fondo_segnale( npar, gin, f, pesi, iflag ):	
		 # la taglia di pesi diventa immensa 2147483647 mentre dovrebbe essere 36
		 # devo vedere f e scegliere f minimo da passare a minuit
		f = funzione_differenza("TMVATest.root","TreeS",pesi,"segnale") + funzione_differenza("TMVATest.root","TreeB",pesi, "fondo")	
		print f
		return
		







# creo la funzione che deve essere minimizzata
# passo anche il tipo di dato che gli sto passando
def funzione_differenza(fname,tname,pesi,dato):
		
		rootfile = TFile.Open(fname,'read')
		tree     = TTree()
		#rootfile.ls()
		rootfile.GetObject(tname,tree)

		#tree.Print()
		funzione_minimizzare = 0 
		
		for event in tree:
			if (event == 500):
				var = [event.Len, event.IP_B1, event.IP_B2, event.IP_A, event.Pt, event.MinDist] 
				# nel caso tirando a caso i parametri non riesco a trovare il minimo un idea è portare tutte 
				# le variabile centrate in zero e dividere per RMS)
			
				
				if(dato == "segnale"):
					funzione_minimizzare +=	abs(funzione_output(var,pesi))
				
				
				elif(dato == "fondo"):			
					funzione_minimizzare += abs(funzione_output(var,pesi) - 1)
						
		return funzione_minimizzare * (1.0/2)


def pluto(fname,tname,pesi,dato,histogram):
		
		rootfile = TFile.Open(fname,'read')
		tree     = TTree()
		#rootfile.ls()
		rootfile.GetObject(tname,tree)

			#tree.Print()
		funzione_minimizzare = 0 
		
		for event in tree:
			if (event == 500):
				var = [event.Len, event.IP_B1, event.IP_B2, event.IP_A, event.Pt, event.MinDist] 
				# nel caso tirando a caso i parametri non riesco a trovare il minimo un idea è portare tutte 
				# le variabile centrate in zero e dividere per RMS)
			
				
				if(dato == "segnale"):
					histogram.Fill(abs(funzione_output(var,pesi)))
				
				
				elif(dato == "fondo"):			
					histogram.Fill(abs(funzione_output(var,pesi)))
							
		return histogram

	
			
# funzione di attivazione 
def sigmoide(x):
	
	sigm = (1 + exp(-x))**(-1)
	return sigm
	
	
	
	
	
	
	
# funzione da minimizzare  pesi li creo a caso ne creo una ventina di set e ne trovo il minimo di questi set e poi pesito da li per minimizzare
def funzione_output(var,pesi):# segnale o fondo altrimenti non so cosa gli passo
		
	output_rete = 0
	# il ciclo va per ogni elemento di var
	# cioè gira per ogni nodo
	for i in range(len(var)):
		input_sigmoide = 0
		
		# il ciclo gira su ogni elemento del livello nascosto
		# che scelgo come dimensione uguale al primo livello
		for j in range(len(pesi)/len(var)):
			input_sigmoide += pesi[i*6 + j] * var[j]
		
		input_sigmoide += pesi[i*6+0]
		valore_di_attivazione = sigmoide(input_sigmoide)
		output_rete += pesi[0+i*6] * valore_di_attivazione
	return output_rete


##______________________________________________________________________________
if __name__ == '__main__':
		
		pesi = testfit()
		
		histogramS = TH1D("test","",100,-5,5)
		histogramB = TH1D("test","",100,-5,5)
		
		histogramS = pluto("TMVATest.root","TreeS",pesi,"segnale",histogramS)
		histogramB = pluto("TMVATest.root","TreeS",pesi,"fondo",histogramB)
		
		histogramS.Draw()
		histogramB.Draw("SAME")
		
		
		gApplication.Run(1)
		
		
		
		
		
		

		
		
		
