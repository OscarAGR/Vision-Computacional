from PIL import Image
import os, sys, random
import math
import ImageDraw
import numpy as np
from math import sin, cos

Idform = 0
x=0 
y=0
x1=0 
y1=0
BorderFigurex=[[]]
BorderFigurex.append([])
BorderFigurey =[[]]
BorderFigurey.append([])
Linex=[[]]
Linex.append([])
Liney =[[]]
Liney.append([])

cosTheta=0
sinTheta=0
mask_x = ([-1,0,1],[-2,0,2],[-1,0,1])
mask_y = ([1,2,1],[0,0,0],[-1,-2,-1])

def main():
 im = Image.open("Test1.png")
 pix = im.load()
 width,heigh = im.size
 imnew=EdgeDetection(im,pix,x1,y1)
 imnew.save("luna2.PNG") 
 imnew2,new_background,max_percentage_color,BorderFigurex,BorderFigurey=FactureDetection(imnew,width,heigh,Idform)
 imnew2.save("luna3.PNG")
 imnew3 = TangentDetection(BorderFigurex,BorderFigurey,imnew2)
 
 #im.show() 
 print "Finish"

 #///////////////////////////////////////////////////////////////////
def bfs(image,color,a,b,Idform): 
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
        
 
        if currentColor == originalColor or currentColor == color:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    i, j = (x + dy, y + dx)
                    if i >= 0 and i < width and j >= 0 and j < high:
                        detectedforms = imagen[i, j]
                        if detectedforms == originalColor:
                            imagen[i, j] = color
                            BorderFigurex[int(Idform)].append(i)
                            BorderFigurey[int(Idform)].append(j)
                            xs.append(i)
                            ys.append(j)
                            n += 1
                            c.append((i, j))

   
    return n, xs, ys,BorderFigurex,BorderFigurey

 #///////////////////////////////////////////////////////////////////
def bfsLine(image,color,a,b,Idform): 
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
        
 
        if currentColor == originalColor or currentColor == color:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    i, j = (x + dy, y + dx)
                    if i >= 0 and i < width and j >= 0 and j < high:
                        detectedforms = imagen[i, j]
                        if detectedforms == originalColor:
                            imagen[i, j] = color
                            Linex[int(Idform)].append(i)
                            Liney[int(Idform)].append(j)
                            xs.append(i)
                            ys.append(j)
                            n += 1
                            c.append((i, j))

   
    return Linex,Liney
 #///////////////////////////////////////////////////////////////////
def FactureDetection(img,width,height,Idform):
 imagen= img.load()
 area = width*height
 percentage = []
 center = []
 for a in range(width):
  for b in range(height):
   if imagen[a,b] == (0, 0, 0):
    color = random.randint(0,255),random.randint(0,255),random.randint(0,255)
    n,xs,xy,BorderFigurex,BorderFigurey= bfs(img,color,a,b,Idform)
    Idform = Idform+1
    average = float(n)/float(area) * 100.0 
   

    if average > 0:
     center.append((sum(xs)/len(xs),sum(xy)/len(xy)))
     percentage.append([average, (color)])
 new_background = percentage.index(max(percentage)) 
 max_percentage_color = percentage[new_background][1]
 


 for i in range(width):
     for j in range(height):
      if imagen[i,j]==max_percentage_color:
          percentage[new_background][1]=(25,25,112)
          imagen[i,j]=(25,25,112)
 xi=0
 xii=0
 for xi in range(len(BorderFigurex)):
  newcolor=random.randint(0,255),random.randint(0,255),random.randint(0,255)   
  for xii in range(len(BorderFigurex[xi])):
   imagen[BorderFigurex[xi][xii],BorderFigurey[xi][xii]]=newcolor
          
 return img,new_background,max_percentage_color,BorderFigurex,BorderFigurey 


 #///////////////////////////////////////////////////////////////////
def EdgeDetection(im,pix,x1,y1):
 (width, height) = im.size 
 for x in range(width):
  for y in range(height):
    sumx=0.0
    sumy = 0.0
   
    for m in range(len(mask_x[0])):
        for h in range(len(mask_y[0])):
           try: 
              x2=x+m 
              y2=y+h
              sum_x= mask_x[m][h] * pix[x2, y2][0] 
              sum_y= mask_y[m][h] * pix[x2, y2][0] 
           except: 
              sum_x=sum_x+0
              sum_y=sum_y+0
           sumx=sum_x+sumx 
           sumy=sum_y+sumy
    valuex = pow(sumx,2) 
    valuey = pow(sumy,2)
    grad = math.pow(abs(sumx) + abs(sumy), 2)
    angle=math.atan2(sumy, sumx)
    if(grad!=0):
    #print x,y
    #print angle
    
     if(x>=348 & y>=209 & x<=400 & y<=300):
         i=0
         y1=0
         x1=x;
         for i in range(100):
          try:
             y1=int(x1*angle)+y
             #print x1,y1
             x1=x1+i
          except:
             i=100    

    # draw = ImageDraw.Draw(im)
     #draw.line((x,y,x1,y1),fill=(255,0,0))
    # beta = 3.1416/2-angle
     cosTheta = sumx / grad
     sinTheta = sumy / grad
     x1=0
     x2=0
        
    if grad <= 0: 
       grad = 255
    elif grad >= 255:
       grad = 0
    pix[x,y] = (grad, grad, grad)
 return im

#///////////////////////////////////////////////////////////////////
def TangentDetection(BorderFigurex,BorderFigurey,im):
 fig=1
 coord=0
 im2=im.load()
 (width, height) = im.size 
 y1=0
 x1=0
 xa=[]
 ya=[]
 sum_x=0
 sum_y=0
 neg=0
 newCicle=0
 d1=0
 d2=0
 Idform2=0
 
 for fig in range(len(BorderFigurex)):
  coord=0
  newCicle=0
  Maxx = BorderFigurex[fig].index(max(BorderFigurex[fig]))
  Minx = BorderFigurex[fig].index(min(BorderFigurex[fig]))
  Maxy = BorderFigurey[fig].index(max(BorderFigurey[fig]))
  Miny = BorderFigurey[fig].index(min(BorderFigurey[fig]))
  print BorderFigurex[fig][Minx], BorderFigurex[fig][Maxx],BorderFigurey[fig][Miny],BorderFigurey[fig][Maxy]
  for newCicle in range(2):
   coord =random.randint(1,len(BorderFigurex[fig]))
   x=BorderFigurex[fig][coord]
   y=BorderFigurex[fig][coord]
   if(fig!=0):
    x= BorderFigurex[fig][coord]
    y= BorderFigurey[fig][coord]
   else:
     x=0
     y=0
   #print x,y
   sumx=0.0
   sumy = 0.0
   for m in range(len(mask_x[0])):
        for h in range(len(mask_y[0])):
           try: 
              x2=x+m 
              y2=y+h
              sum_x= mask_x[m][h] * im2[x2, y2][0] 
              sum_y= mask_y[m][h] * im2[x2, y2][0] 
           except: 
              sum_x=sum_x+0
              sum_y=sum_y+0
           sumx=sum_x+sumx 
           sumy=sum_y+sumy
   valuex = pow(sumx,2) 
   valuey = pow(sumy,2)
   grad = math.pow(abs(sumx) + abs(sumy), 2)
   angle=math.atan2(sumy, sumx)
    #m=x/y
   cosTheta = cos(angle)
   sinTheta = sin(angle)
   m=sinTheta/cosTheta   
   i=0
   y1=0
   x1=x;
   xa.append(x)
   ya.append(y)
   for i in range(50):   
         
          #y1=int(x1*m)+y
        y1=int(round(((m*x1))+y))
        x1=x1+i
      

         
        if(y1<BorderFigurey[fig][Maxy] and y1>BorderFigurey[fig][Miny] and x1<BorderFigurex[fig][Maxx] and x1>BorderFigurex[fig][Minx]):
         neg=1
   y1=y1
   x1=x1
   print y1,x1

   draw = ImageDraw.Draw(im)
   color=(255,25,0)
   draw.line((x,y,-x1,-y1),fill=(0,255,0))
   color=(0,255,0)
   draw.line((0,-y1,-width,y),fill=(0,255,0))
   color=(0,255,0)
   
   print xa,ya
   if(fig!=0):
    draw.line((xa[2],ya[2],x,y),fill=(0,0,255))
    print xa[2],x
    print ya[2],y
    if(xa[2]>x):
       xmed=xa[2]-x
       xmed=xmed/2
       xmed=xmed+x
    else:
       xmed=x-xa[2]
       xmed=xmed/2
       xmed=xmed+xa[2]
    if(ya[2]>y):
       ymed=ya[2]-y
       ymed=ymed/2
       ymed=ymed+y
    else:
       ymed=y-ya[2]
       ymed=ymed/2
       ymed=ymed+ya[2]
    draw.ellipse((xmed-2, ymed-2,xmed+2,ymed+2), fill=(0,0,0))
    
    
   
 im.save("luna4.PNG")
 return im,d1,d2,x,y,Linex,Liney
          
if __name__ == "__main__":
    main()
    
