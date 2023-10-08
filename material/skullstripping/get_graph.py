import matplotlib.pyplot as plt
import numpy as np
import csv

totali_totali = 0
giuste_totali = 0
maggiori_totali = 0
errate_totali = 0


#leggo il file csv
csvfile = open('./attendibilità_skull_stripping.csv', 'r')
for row in csvfile:
    path = row.split(',')[0]
    if path != "Totali" and path != "Dir":
        row = row[0:-1]
        row = row.split(',')
        giuste = int(row[1])
        giuste_totali += giuste
        maggiori = int(row[2])
        maggiori_totali += maggiori
        errate = int(row[3])
        errate_totali += errate
        perc_giuste = row[4][:-1]
        perc_giuste= float(perc_giuste)
        perc_giuste = int(perc_giuste)
        perc_maggiori = row[5][:-1]
        perc_maggiori = float(perc_maggiori)
        perc_maggiori = int(perc_maggiori)
        perc_errate = row[6][:-1]
        perc_errate = float(perc_errate)
        perc_errate = int(perc_errate)
        totali = int(row[7])
        totali_totali += totali
        y = np.array([perc_giuste, perc_maggiori, perc_errate])
        mylabels = ["Giuste:"+str(perc_giuste)+"%", "Maggiori:"+str(perc_maggiori)+"%", "Errate:"+str(perc_errate)+"%"]     
        plt.pie(y, labels = mylabels)
        plt.title("Attendibilità skull stripping\nPath:\n"+path)
        plt.show()
    #calcolo percentuali totali
perc_giuste_totali = (giuste_totali/totali_totali)*100
perc_maggiori_totali = (maggiori_totali/totali_totali)*100
perc_errate_totali = (errate_totali/totali_totali)*100
#approssimo
perc_giuste_totali = int(perc_giuste_totali)
perc_maggiori_totali = int(perc_maggiori_totali)
perc_errate_totali = int(perc_errate_totali)
y = np.array([perc_giuste_totali, perc_maggiori_totali, perc_errate_totali])
mylabels = ["Giuste:"+str(perc_giuste_totali)+"%", "Maggiori:"+str(perc_maggiori_totali)+"%", "Errate:"+str(perc_errate_totali)+"%"]
plt.pie(y, labels = mylabels)
plt.title("Attendibilità skull stripping\nGrafico totale")
plt.show() 