from PIL import Image
import os, sys, random
import math
import ImageDraw
import numpy as np

#Cargamos la imagen de la Deteccion de Bordes
image = Image.open('luna2.png')
imagen = image.load()    
width,high = image.size
area = width*high 
percentage = []
center = []
detectedforms = 0


def bfs(image,color,a,b): 
    imagen=image.load()
    width,high=image.size 
    originalColor = imagen[a,b] #agarro el color original de la imagen
    c=[]
    xs=[]
    ys=[]
    c.append((a,b))#guardo las coordenadas iniciales
    n = 0
    while len(c) > 0:
        (x, y) = c.pop(0)
        currentColor = imagen[x, y]
        
#recorremos buscando igualdad de rgb o si ya se paso, si se encuentra uno nuevo se le asignamos el color, se guardan sus coordenadas y se agranda n
        if currentColor == originalColor or currentColor == color:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    i, j = (x + dy, y + dx)
                    if i >= 0 and i < width and j >= 0 and j < high:
                        detectedforms = imagen[i, j]
                        if detectedforms == originalColor:
                            imagen[i, j] = color
        
                            xs.append(i)
                            ys.append(j)
                            n += 1
                            c.append((i, j))

   # Test1 = image.save('Test1.png') Guarde esta parte para mejor explicacion en pdf
    return n, xs, ys

#Recorremos arreglo en busca del rgb(0,0,0)
for a in range(width):
 for b in range(high):
  if imagen[a,b] == (0, 0, 0):
   color = random.randint(0,255),random.randint(0,255),random.randint(0,255)
   n,xs,xy= bfs(image,color,a,b)
   average = float(n)/float(area) * 100.0 #promedio maximo
   
#Validar que si sea una forma, para eliminar posibles errores
   if average > 0.5:
    center.append((sum(xs)/len(xs),sum(xy)/len(xy))) #obtenemos los centros de la imagen
    percentage.append([average, (color)])
    detectedforms +=1
new_background = percentage.index(max(percentage)) #Calcular el porcentaje maximo
max_percentage_color = percentage[new_background][1] #Seleccion de color de acuerdo al porcentaje

#Coloreo de azul el color con mayor porcentaje
for i in range(width):
    for j in range(high):
     if imagen[i,j]==max_percentage_color:
         percentage[new_background][1]=(25,25,112)
         imagen[i,j]=(25,25,112)

# Test2 = image.save('Test2.png') Guarde esta parte para mejor explicacion en pdf            
print "Print Values:\n"
print "Area = "+str(area)+" pix"
#Dibujar los centros y las etiquetas en las formas 
draw = ImageDraw.Draw(image)
point=0
#Empieza a recorrer los centros guardados almacenandolos en i
for i in center:
 draw.ellipse((i[0]-2, i[1]-2,i[0]+2,i[1]+2), fill=(0,0,0)) #dibuja los puntos en los centros de las formas
 draw.text(((i[0]+4,i[1]+4),), str(point), fill=(0,0,0)) #muestra las etiquetas cerca de los centros
 point +=1

#Imprimir porcentajes de las Formas
detectedforms = 0
print " Detected Forms | Percentage | Center of mass | Color"
for average in percentage: #muestra el id de la etiqueta y el porcentaje de color de cada una
 print "      %d              %.2f     "%(detectedforms, average[0]),center[detectedforms],"     ",percentage[detectedforms][1]
 detectedforms +=1
  
Image2 = 'FeatureDetection.jpg'
image.save(Image2)
image.show()
print "Finish"


