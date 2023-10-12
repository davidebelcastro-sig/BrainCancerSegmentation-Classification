import matplotlib.pyplot as plt
import numpy as np
import csv

totali_totali = 0
giuste_totali = 0
maggiori_totali = 0
errate_totali = 0


#leggo il file csv
csvfile = open('./attendibilità_tumor_detection.csv', 'r')
for row in csvfile:
    path = row.split(',')[0]
    if path != "Totali" and path != "Dir":
        row = row[0:-1]
        row = row.split(',')
        giuste = int(row[1])
        giuste_totali += giuste
        errate = int(row[2])
        errate_totali += errate
        perc_giuste = row[3][:-1]
        perc_giuste= float(perc_giuste)
        perc_giuste = int(perc_giuste)
        perc_errate = row[4][:-1]
        perc_errate = float(perc_errate)
        perc_errate = int(perc_errate)
        totali = int(row[5])
        totali_totali += totali
        y = np.array([perc_giuste, perc_errate])
        mylabels = ["Giuste:"+str(perc_giuste)+"%","Errate:"+str(perc_errate)+"%"]     
        plt.pie(y, labels = mylabels)
        plt.title("Attendibilità tumor segmentation\nPath:\n"+path)
        plt.show()
    #calcolo percentuali totali
perc_giuste_totali = (giuste_totali/totali_totali)*100
perc_errate_totali = (errate_totali/totali_totali)*100
#approssimo
perc_giuste_totali = int(perc_giuste_totali)
perc_errate_totali = int(perc_errate_totali)
y = np.array([perc_giuste_totali, perc_errate_totali])
mylabels = ["Giuste:"+str(perc_giuste_totali)+"%", "Errate:"+str(perc_errate_totali)+"%"]
plt.pie(y, labels = mylabels)
plt.title("Attendibilità tumor segmentation\nGrafico totale")
plt.show() 