Genero parametri a caso con MOnteCarlo. Di questi metà li uso per il 
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
alla y
funclass è la funzione a pag 52 lez9
va poi aggiunta in funclass una funzione che mi faccia la differenza fra 
il valore trovato e il valore quello atteso, cioè una costfunction che 
mi faccia 
1 - segnale
0 - fondo  
e che dica di continuare se la sottrazione (differenza output valore 
voluto) non è sufficiente (continuare vuol dire ridare minuit) 
