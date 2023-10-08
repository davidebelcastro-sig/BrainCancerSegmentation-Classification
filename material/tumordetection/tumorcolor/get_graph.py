import matplotlib.pyplot as plt
import numpy as np
import csv


def get(path,num):

    totali_totali = 0
    giuste_totali = 0
    errate_totali = 0
    #leggo il file csv
    csvfile = open(path, 'r')
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
           # plt.pie(y, labels = mylabels)
           # if num == 1:
             #   plt.title("Attendibilità color tumor\nPath:\n"+path)
          #  else:
           #     plt.title("Attendibilità color tumor magg\nPath:\n"+path)
           # plt.show()
        #calcolo percentuali totali
    perc_giuste_totali = (giuste_totali/totali_totali)*100
    perc_errate_totali = (errate_totali/totali_totali)*100
    #approssimo
    perc_giuste_totali = int(perc_giuste_totali)
    perc_errate_totali = int(perc_errate_totali)
    y = np.array([perc_giuste_totali, perc_errate_totali])
    mylabels = ["Giuste:"+str(perc_giuste_totali)+"%", "Errate:"+str(perc_errate_totali)+"%"]
    plt.pie(y, labels = mylabels)
    if num == 1:
        plt.title("Attendibilità color tumor\nGrafico totale")
    else:
        plt.title("Attendibilità color tumor magg\nGrafico totale")
    #plt.show() 
    plt.savefig("attendibilità_tumor_color.png")



if __name__ == '__main__':
    path = "attendibilità_tumor_color_brain_magg.csv"
    #get(path,0)
    path = "attendibilità_tumor_color.csv"
    get(path,1)