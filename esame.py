#classe per includere gli errori
class ExamException(Exception):
    pass

#inizializzo la classe
class CSVTimeSeriesFile: 

    #metodo init 
    def __init__ (self, name):
        self.name = name
        #verifico che il nome che viene dato all'istanza sia una stringa
        try:
            self.name=str(name)
        except:
            raise ExamException('Errore, il nome del file non è una stringa e non è convertibile in tale')
        #verifico che il nome dell'istanza sia del tipo .csv
        try:
            nome=self.name.split('.')
            if nome[1]!='csv':
                raise ExamException('Errore, il file non è del tipo .csv')
        except:
            raise ExamException('Errore, il nome del file non ha un "." pertanto non può essere del tipo .csv')

    #metodo get_data per raccogliere i dati
    def get_data (self):
        #creo una lista vuota per inserire i valori
        values = []
        #creo una lista vuota per le date 
        dates = []
        #apro il file csv in lettura
        my_file = open(self.name, 'r')
        #creo una variabile che mi servirà per sostenere se le date saranno in ordine
        data_prec=0
        #per ogni riga del mio file CSV eseguo uno split
        for line in my_file:
            #splitto ogni riga sulla virgola 
            element=line.split(',')
            if len(element)!=2:
                continue             
            #divido data e temperatura
            data = element [0]
            value = element [1]
            #verifico che le date siano degli int o che siano convertibili in int
            try:
                data=int(data)
                value=float(value)
            except:
                continue
            #verifico che le date siano in ordine
            if data<data_prec:
                #verifico che il valore non si ripeta tra i precedenti o che non sia uguale a uno dei precedenti
                for i in range(0,len(dates)):
                    #controllo se è uguale ad una delle precedenti
                    if data==dates[i]:
                        if value==values[i]:
                            raise ExamException('una data coincide con una già presente nella lista')
                        else:
                            raise ExamException('una data coincide con una già presente nella lista ma i valori sono diversi, pertanto il dato viene escluso')
                            continue
                    else:
                        raise ExamException('una data non è inserita nel posto corretto in ordine cronologico')
            #aggiungo alla lista delle date la prima colonna e a quella dei valori la seconda
            dates.append (data)
            values.append(value)
        #dichiaro la lista da ritornare
        valori=[]
        #aggiungo tutti gli elementi nelle liste, che poi aggiungo alla lista da ritornare
        for i in range(0,len(values)):
            valore=[dates[i],values[i]]
            valori.append(valore)
        #chiudo la lettura del file csv
        my_file.close ()
        #ritorno la lista di liste
        return valori

#funzione che calcola le statistiche delle temperature giornata per giornata
def daily_stats(time_series):
    #creo la lista che conterrà a sua volta delle liste, indicanti i vari valori che ha assunto la temperatura durante le varie giornate
    giornate=[]
    #creo la lista che contiene i vari valori durante il giorno
    giorno=[]
    #decreto la mezzanotte del primo giorno
    partenza=time_series[0]
    if partenza[0]%86400==0:
        limite_giornata=partenza[0]+86400
    else:
        limite_giornata=partenza[0]-(partenza[0]%86400)+86400
    #analizzo ogni dato uno per volta
    for ora in time_series:
        #se l'ora non coincide con la mezzanotte ci troviamo nella stessa giornata
        if ora[0]<limite_giornata:
            #assegno alla lista il valore 
            giorno.append(ora[1])
        #se inizia una nuova giornata:
        else:
            #se la lista non è vuota
            if giorno!=[]:
                #prima di tutto aggiungo la giornata appena terminata alla lista
                giornate.append(giorno)
            #azzero la lista del giorno (è appena iniziato il giorno nuovo)
            giorno=[]
            #aggiungo alla lista il primo valore della giornata
            giorno.append(ora[1])
            limite_giornata+=86400
    giornate.append(giorno)
    #dichiaro la lista statistiche
    statistiche=[]
    #calcolo le statistiche di ogni singolo giorno
    for giorno in giornate:
        #assegno al primo valore del giorno sia il massimo,sia il minimo
        max=giorno[0]
        min=giorno[0]
        #dichiaro la somma
        somma=0
        #prendo in esame ogni rilevamento del giorno
        for i in range(0,len(giorno)):
            #se la temperatura risulta più bassa della temperatura minima registrata fin'ora, la assegno come valore minimo
            if giorno[i]<min:
                min=giorno[i]
            #se la temperatura risulta più alta della temperatura massima registrata fin'ora, la assegno come valore massimo
            if giorno[i]>max:
                max=giorno[i]
            #la somma aggiunge ad ogni giro il rilevamento effettuato
            somma+=giorno[i]
        #la media è la somma diviso il numero di rilevazioni (ovvero la lunghezza della lista giorno)
        media=somma/len(giorno)
        #una singola statistica è una lista di 3 elementi: massimo, minimo e media aritmetica
        statistica=[min,max,media]
        #ogni singola statistica viene aggiunta alla lista delle statistiche
        statistiche.append(statistica)
    #ritorno la lista delle statistiche
    return statistiche

#faccio una funzione per stampare a schermo le statistiche in modo carino
def print_stats(time_series_stats):
    #creo un indice che mi va ad indicare il giorno di cui stampo le informazioni 
    i=1
    #stampo le informazioni giorno per giorno
    for statistica in time_series_stats:
        #indico il giorno delle statistiche
        print ("Giorno {}:".format(i))
        #massimo
        print("Temperatura massima registrata: {}".format(statistica[1]))
        #minimo
        print("Temperatura minima registrata: {}".format(statistica[0]))
        #media
        print("Temperatura media della giornata: {}".format(statistica[2]))
        #aumento di uno l'indice
        i+=1
        print("\n")





#creo l'istanza del file csv
time_series_file = CSVTimeSeriesFile('data.csv')
#applico la funzione get data
time_series = time_series_file.get_data()
#print (time_series)
#applico la funzione daily_stats
time_series_stats=daily_stats(time_series)
#stampo i valori a schermo
print_stats(time_series_stats) 
