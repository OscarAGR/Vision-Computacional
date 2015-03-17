from PIL import Image
import os, sys, random
import math
from math import sqrt, ceil, floor, fabs
import ImageDraw
import numpy as np

#Cargamos la imagen de la Deteccion de Bordes
image = Image.open('CircleTest22.png')
imagen = image.load()    
width,high = image.size
area = width*high 
percentage = []
center = []
detectedforms = 0
Idform = 0.0
BorderFigure=[[]]
BorderFigurex=[[]]
BorderFigurex.append([])
BorderFigurey =[[]]
BorderFigurey.append([])
Vote=[[]]
Vote.append([])
Vote.append([])
Votex=[[]]
Votex.append([])
Votey=[[]]
Votey.append([])
valor=0
fila =[]
resultado=[]
Vacio=[]
radio=0
diameter=0


def bfs(image,color,a,b,Idform):
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
                            #Guardo los valores de los pixales del borde para cada figura

                            #Consigo el los pixeles de los diferentes circulos
                            BorderFigurex[int(Idform)].append(i)
                            BorderFigurey[int(Idform)].append(j)

                            xs.append(i)
                            ys.append(j)
                            n += 1
                            c.append((i, j))
    
    return n, xs, ys

Idforms = 0

sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]


#Recorremos arreglo en busca del rgb(0,0,0)
for a in range(width):
 for b in range(high):
  if imagen[a,b] == (0, 0, 0):   
   color = random.randint(0,255),random.randint(0,255),random.randint(0,255)
   n,xs,xy= bfs(image,color,a,b,Idform)
   Idform = Idform+1
   average = float(n)/float(area) * 100.0 #promedio maximo
   
#Validar que si sea una forma, para eliminar posibles errores
   if average > 0.5:
    center.append((sum(xs)/len(xs),sum(xy)/len(xy))) #obtenemos los centros de la imagen
    percentage.append([average, (color)])
    detectedforms +=1
new_background = percentage.index(max(percentage)) #Calcular el porcentaje maximo
max_percentage_color = percentage[new_background][1] #Seleccion de color de acuerdo al porcentaje

#Coloreo de gris el color con mayor porcentaje
for i in range(width):
    for j in range(high):
     if imagen[i,j]==max_percentage_color:
         percentage[new_background][1]=(25,25,112)
         imagen[i,j]=(25,25,112)

          
print "Print exact values:\n"
print "Area = "+str(area)+" pix"
#Dibujar los centros y las etiquetas en las formas 
draw = ImageDraw.Draw(image)

#Imprimir porcentajes de las Formas
detectedforms = 0
print " Detected Forms | Percentage | Center of mass | Color"
for average in percentage: #muestra el id de la etiqueta y el porcentaje de color de cada una
 print "      %d              %.2f     "%(detectedforms, average[0]),center[detectedforms],"     ",percentage[detectedforms][1]
 detectedforms +=1

IDFigure=0


i=0
x=0
y=0



i=0
x=0
y=0
mat_x = ([-1,0,1],[-2,0,2],[-1,0,1])
mat_y = ([1,2,1],[0,0,0],[-1,-2,-1])
sumx=0
sumy=0
fig=0

#Aqui empieza el calculo del circulo
for fig in xrange(len(BorderFigurex)): 
 #calculo las posiciones maximas y minimas de "x" y "y"
 Maxx = BorderFigurex[fig].index(max(BorderFigurex[fig]))
 Minx = BorderFigurex[fig].index(min(BorderFigurex[fig]))
 Maxy = BorderFigurey[fig].index(max(BorderFigurey[fig]))
 Miny = BorderFigurey[fig].index(min(BorderFigurey[fig]))
 #Calculo el diametro y radio de la figura
 diameter=BorderFigurex[fig][Maxx]-BorderFigurex[fig][Minx]
 radio= diameter/2

 if(fig==1):
  rest=diameter
 else:
       rest=radio
         
 i=0
 
 for i in xrange(len(BorderFigurex[fig])):
    #divido las dimensiones de largo y ancho entre 2
    y = (BorderFigurey[fig][Maxx] / 2) - BorderFigurey[fig][i]
    x = BorderFigurex[fig][i] - (BorderFigurex[fig][Maxx] / 2)
    sumx=0
    sumy=0
    m=0
    h=0
    #Aplico convolucion 
    for m in range(len(mat_x[0])):
                for h in range(len(mat_y[0])):
                    try:
                        x1=BorderFigurex[fig][i]
                        y1=BorderFigurey[fig][i]
                        mul_x= mat_x[m][h] * imagen[x1+m, y1+h][0]
                        mul_y= mat_y[m][h] * imagen[x1+m, y1+h][0]
                    except:
                        mul_x=0
                        mul_y=0
                    sumx=mul_x+sumx
                    sumy=mul_y+sumy
    #Calculo el grad de cada uno de los pixelex de cada circulo                
    valorx = pow(sumx,2)
    valory = pow(sumy,2)
    grad = int(math.sqrt(valorx + valory))
    if fabs(grad) > 0:
        #Saco el coseno y seno del grad para que de apartir de este deducir las coordenadas a votar 
            cosTheta = sumx / grad
            sinTheta = sumy / grad
            xc = int(x - radio * cosTheta)
            yc = int(y - radio * sinTheta)
            xcm = xc + BorderFigurex[fig][Maxx] / 2
            ycm = (BorderFigurey[fig][Maxx] / 2 + yc)
            if xcm >= 0 and xcm < BorderFigurex[fig][Maxx] and ycm >= 0 and ycm < BorderFigurey[fig][Maxx]:
                #cambio el color de las coordenadas que podrian ser centros y lo coloreo de rojo, al igual que llevo la cuenta de votos
                if(imagen[xcm,ycm+rest]==(255,0,0)):
                    Sum=0
                    for Sum in range(len(Vote[fig])):
                     if( Votex[fig][Sum]==xcm and Votey[fig][Sum] == ycm+rest):
                       Sumvote=Vote[fig][Sum]
                       Vote[fig][Sum]=Sumvote+1
                else:    
                 imagen[xcm,ycm+rest]=(255,0,0)
                 Votex[fig].append(xcm)
                 Votey[fig].append(ycm+rest)
                 Vote[fig].append(1)




#Imprimo los votos
Sum=0
fig=0
#declaramos la distancia minima a considerar
distanceOP=100

print "\nPrint calculated values:\n"
print " Detected Forms | Center of mass (calculated) | distance |"
for fig in xrange(len(BorderFigurex)):
  Maxx = BorderFigurex[fig].index(max(BorderFigurex[fig]))
#Calculo el mayor nuemro de votos para cada figura
  MaxVote = Vote[fig].index(max(Vote[fig]))
  
  for Sum in range(len(Vote[fig])):
   Area = (len(BorderFigurex[fig]))
   #Dibujamos solo los posibles centros en base a los votos y selecionamos el mejor en base a su distancia
   if(Vote[fig][Sum]<Vote[fig][MaxVote]):
     xcm=Votex[fig][Sum]
     ycm=Votey[fig][Sum]
     x,y=center[fig]
     xreal= xcm-x
     yreal= ycm-y
     valorx = pow(xreal,2)
     valory = pow(yreal,2)
     distance = int(math.sqrt(valorx + valory))
     if(distance<distanceOP):
         CenterPointx=xcm
         CenterPointy=ycm
         distanceOP=distance
         
     imagen[xcm,ycm]=(255,255,255)
   else:
     xcm=Votex[fig][Sum]
     ycm=Votey[fig][Sum]
     imagen[xcm,ycm]=(255,0,0,1)
  print "      %d                    (%d,%d)             %d pix     "%(fig,CenterPointx,CenterPointy,distanceOP)
  distanceOP=100
  draw.line((CenterPointx,CenterPointy,BorderFigurex[fig][Maxx],BorderFigurey[fig][Maxx]),fill=(255,0,0))
  draw.text(((BorderFigurex[fig][Maxx],CenterPointy-8),), "Radio", fill=(255,0,0)) 
  draw.ellipse((CenterPointx-2, CenterPointy-2,CenterPointx+2,CenterPointy+2), fill=(0,0,0))
  draw.text(((CenterPointx+1,CenterPointy+1),), "Centro de Masa", fill=(0,0,0)) 
  


    


Image2 = 'CircleCenter.jpg'
image.save(Image2)
#image.show()

print "Finish"


