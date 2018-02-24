Genero parametri a caso con MonteCarlo. Di questi metà li uso per il 
training metà per test della rete.

Idea: dai parametri di MOnteCarlo trovo il minimo di fcn, 
che non sarà il vero minimo, ma mi serve 
come punto di partenza per minimizzare con ROOT 
(uso MInuit per la minimizzazione). Questo mi trova il minimo cercato che 
è anche l'output della rete.

Se avanza tempo e voglia: invece di minimizzare con Minuit usare i 
genereci test di minimizzazione delle reti neurali

IMPLEMENTAZIONE:
teststat deve utilizzare la formula a pag 50 lez9 e la funzione equivale 
alla y, di fatto è la funzione da minimizzare
Creato la funzione di attivazione (sigmoide)
funclass è la funzione a pag 52 lez9
va poi aggiunta in funclass una funzione che mi faccia la differenza fra 
il valore trovato e il valore quello atteso, cioè una costfunction che 
mi faccia 
1 - segnale
0 - fondo  
e che dica di continuare se la sottrazione (differenza output valore 
voluto) non è sufficiente (continuare vuol dire ridare minuit) 
mi serve altrimenti non so come minimizzare



Quando trovo il set giusto di pesi per la funzione teststat, quelo per cui 
funclass è minima, allora posso usare la mia rete su dei dati e non piu sul training 
e quello che mi interesserà sarà solo l'output di teststat.   

Alla rete neurale arriva sempre una riga per matrice di osservazioni (Len,IP_B1,ecc)
e per ogni riga c'è un valore di output. 
Devo avere un valore di output per ogni variabile in Len,IP_B1,ecc
per tutti questi valori trovo una funzione differenza con una matrice di pesi scelta
la minimizzo e trovo un valore numerico.Lo faccio con dieci matrici di pesi
diversi.

Cambiati i pesi ora li prendi in maniera gaussiana tra un numero casuale 
fino al massino di input,
input normalizzati
