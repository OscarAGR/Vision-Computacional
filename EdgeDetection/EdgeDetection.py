from PIL import Image
import os, sys, random
import math
import numpy as np

im = Image.open("Cjpg.jpg") #se abre la imagen a usar con el comando open de Image almacenandolo en im
pix = im.load() #se cargan todos los valores RGB de los pixeles de la imagen inicializandolo en pix
(width, height) = im.size #Agarro las dimenciones (ancho,alto) de la imagen

x=0 #inicializo valor x
y=0 #inicializo valor y
mask_x = ([-1,0,1],[-2,0,2],[-1,0,1])
mask_y = ([1,2,1],[0,0,0],[-1,-2,-1])#mascara para las coordenadas en y


#Recorro los pixeles de la imagen con 2 ciclos for con los rangos de sus dimenciones  
for x in range(width):
 for y in range(height):
            average = sum(pix[x,y])/3  #Saco el promedio de los RGB de cada pixel recorrido
            gray = (average,average,average) #declaro RGB de acuerdo al promedio de cada pixel recorrido
            pix[x,y]=gray #cambio el valor RGB del pixel recorrido para cambiarlo a escala de grises


#declaro un nuevo recorrido de la imagen inicializando las variables
x=0
y=0
for x in range(width):
 for y in range(height):
   sumx=0.0
   sumy = 0.0
   #recorro la mascara para cada pixel recorrido
   for m in range(len(mask_x[0])):
       for h in range(len(mask_y[0])):
          try: #declaro el try para reparar el posible error de salida de la imagen al aplicar la mascara
             x2=x+m #Visito los vecinos del pixel seleccionado 
             y2=y+h 
             sum_x= mask_x[m][h] * pix[x2, y2][0] #multiplico el valor de la mascara a la coordenada en x del pixel
             sum_y= mask_y[m][h] * pix[x2, y2][0] #multiplico el valor de la mascara a la corrdenada en y del pixel
          except: #delaro el except si se salio del area de la imagen y declaro que la suma de x y y es igual a 0
             sum_x=0
             sum_y=0
          sumx=sum_x+sumx #sumo el resultado de la suma en x y asi mismo en y
          sumy=sum_y+sumy
   valuex = pow(sumx,2) #elevo a la segunda potencia lo resultante de la suma
   valuey = pow(sumy,2)
   grad = int(math.sqrt(valuex + valuey)) #calculo el gradiante 
   if grad <= 0: # declaro el umbral de corte para lipiar posible ruido, lo declaro en 0 para declarar que es negro
      grad = 0
   elif grad >= 135:# asi mismo declaro el umblar de corte para el blanco
      grad = 255
   pix[x,y] = (grad, grad, grad)

          

im.save("luna2", "png") #Guardamos el resultado de la imagen con el nombre "luna2" y el tipo "JPEG"
im.show() #Mosatramos la imagen por el metodo show 
print "Finish"
