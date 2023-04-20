import cv2
import numpy as np

# Read image
im = cv2.imread("epi.png")
#voglio tagliare l'imagine prendendo da 0 a 200 di larghezz e tutta l'altezza
imCrop1 = im[0:200, 0:im.shape[1]] #cosi è prima riga
imCrop2 = im[200:410, 0:im.shape[1]] #cosi è seconda riga
imCrop3 = im[400:610, 0:im.shape[1]] #cosi è terza riga
imCrop4 = im[600:810, 0:im.shape[1]] #cosi è quarta riga
imCrop5 = im[800:1015, 0:im.shape[1]] #cosi è quinta riga
imCrop6 = im[1000:1215, 0:im.shape[1]] #cosi è sesta riga
imCrop7 = im[1200:1415, 0:im.shape[1]] #cosi è settima riga
imCrop8 = im[1400:1615, 0:im.shape[1]] #cosi è ottava riga
imCrop9 = im[1600:1815, 0:im.shape[1]] #cosi è nona riga
imCrop10 = im[1800:2015, 0:im.shape[1]] #cosi è decima riga

#taglio ogni riga in 10 colonne
#riga1->imCrop1
imCrop11 = imCrop1[0:imCrop1.shape[0], 0:200]
imCrop12 = imCrop1[0:imCrop1.shape[0], 200:410]
imCrop13 = imCrop1[0:imCrop1.shape[0], 400:610]
imCrop14 = imCrop1[0:imCrop1.shape[0], 600:810]
imCrop15 = imCrop1[0:imCrop1.shape[0], 800:1015]
imCrop16 = imCrop1[0:imCrop1.shape[0], 1000:1215]
imCrop17 = imCrop1[0:imCrop1.shape[0], 1200:1415]
imCrop18 = imCrop1[0:imCrop1.shape[0], 1400:1615]
imCrop19 = imCrop1[0:imCrop1.shape[0], 1600:1815]
imCrop110 = imCrop1[0:imCrop1.shape[0], 1800:2015]
#riga2
imCrop21 = imCrop2[0:imCrop2.shape[0], 0:200]
imCrop22 = imCrop2[0:imCrop2.shape[0], 200:410]
imCrop23 = imCrop2[0:imCrop2.shape[0], 400:610]
imCrop24 = imCrop2[0:imCrop2.shape[0], 600:810]
imCrop25 = imCrop2[0:imCrop2.shape[0], 800:1015]
imCrop26 = imCrop2[0:imCrop2.shape[0], 1000:1215]
imCrop27 = imCrop2[0:imCrop2.shape[0], 1200:1415]
imCrop28 = imCrop2[0:imCrop2.shape[0], 1400:1615]
imCrop29 = imCrop2[0:imCrop2.shape[0], 1600:1815]
imCrop210 = imCrop2[0:imCrop2.shape[0], 1800:2015]
#riga3
imCrop31 = imCrop3[0:imCrop3.shape[0], 0:200]
imCrop32 = imCrop3[0:imCrop3.shape[0], 200:410]
imCrop33 = imCrop3[0:imCrop3.shape[0], 400:610]
imCrop34 = imCrop3[0:imCrop3.shape[0], 600:810]
imCrop35 = imCrop3[0:imCrop3.shape[0], 800:1015]
imCrop36 = imCrop3[0:imCrop3.shape[0], 1000:1215]
imCrop37 = imCrop3[0:imCrop3.shape[0], 1200:1415]
imCrop38 = imCrop3[0:imCrop3.shape[0], 1400:1615]
imCrop39 = imCrop3[0:imCrop3.shape[0], 1600:1815]
imCrop310 = imCrop3[0:imCrop3.shape[0], 1800:2015]
#riga4
imCrop41 = imCrop4[0:imCrop4.shape[0], 0:200]
imCrop42 = imCrop4[0:imCrop4.shape[0], 200:410]
imCrop43 = imCrop4[0:imCrop4.shape[0], 400:610]
imCrop44 = imCrop4[0:imCrop4.shape[0], 600:810]
imCrop45 = imCrop4[0:imCrop4.shape[0], 800:1015]
imCrop46 = imCrop4[0:imCrop4.shape[0], 1000:1215]
imCrop47 = imCrop4[0:imCrop4.shape[0], 1200:1415]
imCrop48 = imCrop4[0:imCrop4.shape[0], 1400:1615]
imCrop49 = imCrop4[0:imCrop4.shape[0], 1600:1815]
imCrop410 = imCrop4[0:imCrop4.shape[0], 1800:2015]
#riga5
imCrop51 = imCrop5[0:imCrop5.shape[0], 0:200]
imCrop52 = imCrop5[0:imCrop5.shape[0], 200:410]
imCrop53 = imCrop5[0:imCrop5.shape[0], 400:610]
imCrop54 = imCrop5[0:imCrop5.shape[0], 600:810]
imCrop55 = imCrop5[0:imCrop5.shape[0], 800:1015]
imCrop56 = imCrop5[0:imCrop5.shape[0], 1000:1215]
imCrop57 = imCrop5[0:imCrop5.shape[0], 1200:1415]
imCrop58 = imCrop5[0:imCrop5.shape[0], 1400:1615]
imCrop59 = imCrop5[0:imCrop5.shape[0], 1600:1815]
imCrop510 = imCrop5[0:imCrop5.shape[0], 1800:2015]
#riga6
imCrop61 = imCrop6[0:imCrop6.shape[0], 0:200]
imCrop62 = imCrop6[0:imCrop6.shape[0], 200:410]
imCrop63 = imCrop6[0:imCrop6.shape[0], 400:610]
imCrop64 = imCrop6[0:imCrop6.shape[0], 600:810]
imCrop65 = imCrop6[0:imCrop6.shape[0], 800:1015]
imCrop66 = imCrop6[0:imCrop6.shape[0], 1000:1215]
imCrop67 = imCrop6[0:imCrop6.shape[0], 1200:1415]
imCrop68 = imCrop6[0:imCrop6.shape[0], 1400:1615]
imCrop69 = imCrop6[0:imCrop6.shape[0], 1600:1815]
imCrop610 = imCrop6[0:imCrop6.shape[0], 1800:2015]
#riga7
imCrop71 = imCrop7[0:imCrop7.shape[0], 0:200]
imCrop72 = imCrop7[0:imCrop7.shape[0], 200:410]
imCrop73 = imCrop7[0:imCrop7.shape[0], 400:610]
imCrop74 = imCrop7[0:imCrop7.shape[0], 600:810]
imCrop75 = imCrop7[0:imCrop7.shape[0], 800:1015]
imCrop76 = imCrop7[0:imCrop7.shape[0], 1000:1215]
imCrop77 = imCrop7[0:imCrop7.shape[0], 1200:1415]
imCrop78 = imCrop7[0:imCrop7.shape[0], 1400:1615]
imCrop79 = imCrop7[0:imCrop7.shape[0], 1600:1815]
imCrop710 = imCrop7[0:imCrop7.shape[0], 1800:2015]
#riga8
imCrop81 = imCrop8[0:imCrop8.shape[0], 0:200]
imCrop82 = imCrop8[0:imCrop8.shape[0], 200:410]
imCrop83 = imCrop8[0:imCrop8.shape[0], 400:610]
imCrop84 = imCrop8[0:imCrop8.shape[0], 600:810]
imCrop85 = imCrop8[0:imCrop8.shape[0], 800:1015]
imCrop86 = imCrop8[0:imCrop8.shape[0], 1000:1215]
imCrop87 = imCrop8[0:imCrop8.shape[0], 1200:1415]
imCrop88 = imCrop8[0:imCrop8.shape[0], 1400:1615]
imCrop89 = imCrop8[0:imCrop8.shape[0], 1600:1815]
imCrop810 = imCrop8[0:imCrop8.shape[0], 1800:2015]
#riga9
imCrop91 = imCrop9[0:imCrop9.shape[0], 0:200]
imCrop92 = imCrop9[0:imCrop9.shape[0], 200:410]
imCrop93 = imCrop9[0:imCrop9.shape[0], 400:610]
imCrop94 = imCrop9[0:imCrop9.shape[0], 600:810]
imCrop95 = imCrop9[0:imCrop9.shape[0], 800:1015]
imCrop96 = imCrop9[0:imCrop9.shape[0], 1000:1215]
imCrop97 = imCrop9[0:imCrop9.shape[0], 1200:1415]
imCrop98 = imCrop9[0:imCrop9.shape[0], 1400:1615]
imCrop99 = imCrop9[0:imCrop9.shape[0], 1600:1815]
imCrop910 = imCrop9[0:imCrop9.shape[0], 1800:2015]
#riga10
imCrop101 = imCrop10[0:imCrop10.shape[0], 0:200]
imCrop102 = imCrop10[0:imCrop10.shape[0], 200:410]
imCrop103 = imCrop10[0:imCrop10.shape[0], 400:610]
imCrop104 = imCrop10[0:imCrop10.shape[0], 600:810]
imCrop105 = imCrop10[0:imCrop10.shape[0], 800:1015]
imCrop106 = imCrop10[0:imCrop10.shape[0], 1000:1215]
#salvda da 106->index1 
cv2.imwrite("1.png", imCrop106)
cv2.imwrite("2.png", imCrop105)
cv2.imwrite("3.png", imCrop104)
cv2.imwrite("4.png", imCrop103)
cv2.imwrite("5.png", imCrop102)
cv2.imwrite("6.png", imCrop101)
cv2.imwrite("7.png", imCrop910)
cv2.imwrite("8.png", imCrop99)
cv2.imwrite("9.png", imCrop98)
cv2.imwrite("10.png", imCrop97)
cv2.imwrite("11.png", imCrop96)
cv2.imwrite("12.png", imCrop95)
cv2.imwrite("13.png", imCrop94)
cv2.imwrite("14.png", imCrop93)
cv2.imwrite("15.png", imCrop92)
cv2.imwrite("16.png", imCrop91)
cv2.imwrite("17.png", imCrop810)
cv2.imwrite("18.png", imCrop89)
cv2.imwrite("19.png", imCrop88)
cv2.imwrite("20.png", imCrop87)
cv2.imwrite("21.png", imCrop86)
cv2.imwrite("22.png", imCrop85)
cv2.imwrite("23.png", imCrop84)
cv2.imwrite("24.png", imCrop83)
cv2.imwrite("25.png", imCrop82)
cv2.imwrite("26.png", imCrop81)
cv2.imwrite("27.png", imCrop710)
cv2.imwrite("28.png", imCrop79)
cv2.imwrite("29.png", imCrop78)
cv2.imwrite("30.png", imCrop77)
cv2.imwrite("31.png", imCrop76)
cv2.imwrite("32.png", imCrop75)
cv2.imwrite("33.png", imCrop74)
cv2.imwrite("34.png", imCrop73)
cv2.imwrite("35.png", imCrop72)
cv2.imwrite("36.png", imCrop71)
cv2.imwrite("37.png", imCrop610)
cv2.imwrite("38.png", imCrop69)
cv2.imwrite("39.png", imCrop68)
cv2.imwrite("40.png", imCrop67)
cv2.imwrite("41.png", imCrop66)
cv2.imwrite("42.png", imCrop65)
cv2.imwrite("43.png", imCrop64)
cv2.imwrite("44.png", imCrop63)
cv2.imwrite("45.png", imCrop62)
cv2.imwrite("46.png", imCrop61)
cv2.imwrite("47.png", imCrop510)
cv2.imwrite("48.png", imCrop59)
cv2.imwrite("49.png", imCrop58)
cv2.imwrite("50.png", imCrop57)
cv2.imwrite("51.png", imCrop56)
cv2.imwrite("52.png", imCrop55)
cv2.imwrite("53.png", imCrop54)
cv2.imwrite("54.png", imCrop53)
cv2.imwrite("55.png", imCrop52)
cv2.imwrite("56.png", imCrop51)
cv2.imwrite("57.png", imCrop410)
cv2.imwrite("58.png", imCrop49)
cv2.imwrite("59.png", imCrop48)
cv2.imwrite("60.png", imCrop47)
cv2.imwrite("61.png", imCrop46)
cv2.imwrite("62.png", imCrop45)
cv2.imwrite("63.png", imCrop44)
cv2.imwrite("64.png", imCrop43)
cv2.imwrite("65.png", imCrop42)
cv2.imwrite("66.png", imCrop41)
cv2.imwrite("67.png", imCrop310)
cv2.imwrite("68.png", imCrop39)
cv2.imwrite("69.png", imCrop38)
cv2.imwrite("70.png", imCrop37)
cv2.imwrite("71.png", imCrop36)
cv2.imwrite("72.png", imCrop35)
cv2.imwrite("73.png", imCrop34)
cv2.imwrite("74.png", imCrop33)
cv2.imwrite("75.png", imCrop32)
cv2.imwrite("76.png", imCrop31)
cv2.imwrite("77.png", imCrop210)
cv2.imwrite("78.png", imCrop29)
cv2.imwrite("79.png", imCrop28)
cv2.imwrite("80.png", imCrop27)
cv2.imwrite("81.png", imCrop26)
cv2.imwrite("82.png", imCrop25)
cv2.imwrite("83.png", imCrop24)
cv2.imwrite("84.png", imCrop23)
cv2.imwrite("85.png", imCrop22)
cv2.imwrite("86.png", imCrop21)
cv2.imwrite("87.png", imCrop110)
cv2.imwrite("88.png", imCrop19)
cv2.imwrite("89.png", imCrop18)
cv2.imwrite("90.png", imCrop17)
cv2.imwrite("91.png", imCrop16)
cv2.imwrite("92.png", imCrop15)
cv2.imwrite("93.png", imCrop14)
cv2.imwrite("94.png", imCrop13)
cv2.imwrite("95.png", imCrop12)
cv2.imwrite("96.png", imCrop11)

