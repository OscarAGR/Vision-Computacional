from Tkinter import *
from PIL import Image, ImageTk
import math
import os, sys, random
import ImageDraw
import numpy as np



def normalizar(original_image):
    x, y = original_image.size
    normalized_image = Image.new("RGB", (x, y))
    pixls = []
    for a in range(y):
        for b in range(x):
            pix = original_image.getpixel((b, a))[0]
            pixls.append(pix)
    maxi = max(pixls) 
    mini = min(pixls)
    l = 256.0/(maxi - mini)
    pixls = []
    for a in range(y):
        for b in range(x):
            pix = original_image.getpixel((b, a))[0]
            new_pix = int(math.floor((pix-mini)*l))
            pixls.append((new_pix, new_pix, new_pix))
    normalized_image.putdata(pixls)
    normalized_image.save("normalized_image.png")
    return normalized_image

#defino el histogramqa Horizontal en base a las sumas de la lineas Horizontal
def Horizontal_histogram(image,x,y):
        pix = image.load()
        hori_hist = np.zeros(x,float)
        for w in range(x):
            for h in range(y):
                 hori_hist[w] += pix[w,h][0]
                
        return hori_hist

#defino el histogramqa vertical en base a las sumas de la lineas verticales
def Vertical_histogram(image,x,y):
        pix = image.load()
        verti_hist = np.zeros(y,float)
        for h in range(y):
            for w in range(x):
                verti_hist[h] += pix[w,h][0]
        return verti_hist

#Declaro el humbral de corte para los histigram
def Threshold(histogram):
    List = list()
    medium = sum(histogram) / len(histogram)
        
    for i in range(1, len(histogram)-1):
        if histogram[i-1]>histogram[i] and histogram[i]<histogram[i+1]:
            if histogram[i] < medium: 
             List.append(i)
    return List

#Dibujo las lineas que se dectaron agujeros y guardo su interseccion
def drawlines(linesx, linesy,x,y,dear):
    draw = ImageDraw.Draw(dear)
    CoordInterx=[]
    CoordIntery=[]
    for i in range(len(linesy)):
        for j in range(len(linesx)):
         draw.line((0,linesy[i],x,linesy[i]),fill=(0,255,0))
         draw.line((linesx[j],0,linesx[j],y),fill=(0,0,255))
         CoordInterx.append(linesx[j])
         CoordIntery.append(linesy[i])
    dear.save("before_filter_only_lines.png")
    dear,CoordInterx,CoordIntery=FiltroCoord(CoordInterx,CoordIntery,dear,draw)
    dear.save("after_filter.png")
    return nueva2,CoordInterx,CoordIntery

#filtro las coodenadas para limpiarlo del ruido de rojo dibujo las que estan en agujeros y de azul los que no
def FiltroCoord(CoordInterx, CoordIntery,dear,draw):
    img = dear.load()
    RealCoordInterx=[]
    RealCoordIntery=[]
    for i in range(len(CoordInterx)):
        pix = original_image.getpixel((CoordInterx[i],CoordIntery[i]))[0]
        if(pix<100):
          draw.ellipse((CoordInterx[i]-1, CoordIntery[i]-1,CoordInterx[i]+1,CoordIntery[i]+1), fill=(255,0,0))
          RealCoordInterx.append(CoordInterx[i])
          RealCoordIntery.append(CoordIntery[i])
        else:
          draw.ellipse((CoordInterx[i]-1, CoordIntery[i]-1,CoordInterx[i]+1,CoordIntery[i]+1), fill=(0,255,255))    
    return dear,RealCoordInterx,RealCoordIntery

#Para ver todo el agujero
def bfs(image,color,a,b): 
    imagen=image.load()
    width,high=image.size 
    originalColor = imagen[a,b]
    c=[]
    xs=[]
    ys=[]
    c.append((a,b))
    n = 0
    while len(c) > 0:
        (x, y) = c.pop(0)
        currentColor = imagen[x, y]
        if ((currentColor == originalColor or (currentColor == color))):
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

   
    return n, xs, ys


original_image = Image.open('Demo3.jpg')
original_image = original_image.convert('RGB')
normalizar(original_image)
nueva2 = Image.open('imagen_normalizada.png')
x, y = nueva2.size
Sum_horizontal= Horizontal_histogram(nueva2,x,y)
Sum_Vertical=Vertical_histogram(nueva2,x,y)
linesh=Threshold(Sum_horizontal)
lnesv=Threshold(Sum_Vertical)
nueva,RealCoordInterx,RealCoordIntery=drawlines(linesh,lnesv,x,y,nueva2)
print RealCoordInterx,RealCoordIntery
area = x*y
Idform = 0
percentage = []
center = []
detectedforms = 0
im= nueva.load()
for i in range(len(RealCoordInterx)):
    color = random.randint(0,255),random.randint(0,255),random.randint(0,255)
    n,xs,xy= bfs(nueva2,color,RealCoordInterx[i],RealCoordIntery[i])
    Idform = Idform+1
    average = float(n)/float(area) * 100.0 
    if average > 0:
     center.append((sum(xs)/len(xs),sum(xy)/len(xy)))
     percentage.append([average, (color)])
     detectedforms +=1
print "Print Values:\n"
print "Area = "+str(area)+" pix"

draw = ImageDraw.Draw(nueva)
point=0

for i in center:
 draw.ellipse((i[0]-1, i[1]-1,i[0]+1,i[1]+1), fill=(0,255,0))  
 draw.text(((i[0]+2,i[1]+2),), str(point), fill=(0,255,0)) 
 point +=1
print percentage
    
          
nueva2.save("imagen_normalizada2.png")
  
print 'finish'
