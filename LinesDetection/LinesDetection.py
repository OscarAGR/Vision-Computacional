from PIL import Image, ImageTk
import math
import sys
import random
import ImageFont, ImageDraw
import Image
from math import pi, atan, floor, fabs, sqrt, sin, cos, ceil

#aplico convolucion para separar las lineas en 'x' y 'y' en 2 imagenes esto por medio de la mascara 
def convolution(OriginalImage, mask):
    x, y = OriginalImage.size
    post = OriginalImage.load()
    NewImagen = Image.new("RGB", (x,y))
    post_new = NewImagen.load() 
    for i in range(x):
        for j in range(y):
            total = 0
            for n in range(i-1, i+2):
                for m in range(j-1, j+2):
                    if n >= 0 and m >= 0 and n < x and m < y:
                        total += mask[n - (i - 1)][ m - (j - 1)] * post[n, m][0]
            post_new[i, j] = (total, total, total)
    #regreso la nueva imagen
    return NewImagen

def main():
    image = Image.open("image_lines.png") 
    image = image.convert('RGB')
#Uso la mascara de sobel para separar las lineas horizontales y verticales en 2 imagenes(x,y)
    maskx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    masky = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
#aplico 2 convoluciones distintas de acuerdo a la mascara
    imagemaskx = convolution(image, maskx)
    imagemasky = convolution(image, masky)
    imagemaskx.save("imagemaskx.png")
    imagemasky.save("imagemasky.png")
#Cargo las imagenes en 2 arreglos    
    lin_x = imagemaskx.load()
    lin_y = imagemasky.load()
#declaro variables    
    List = []
    count_x = 0
    count_y = 0
    angles = []
#pido el ancho y alto de la imagen original    
    width, height = image.size
    for i in range(width):
        temp = []
        for j in range(height):
            #Consulto el color de las cordenada i y j en turno para la imagen "x" y "y" 
            x = lin_x[i, j][0]
            y = lin_y[i, j][0]
            ang = 0.0
            if x + y <= 0.0:
                ang = None
            elif x == 0 and y == 255:
                ang = 90
            else:
                #Convierte radianes a grados de 255/0 y 255/255
                try:
                 ang = math.degrees(abs(y/x))
                except:
                 ang = None
           #si tenemos un angulo (que no sea x y y igual a 0)      
            if ang != None:
                p = abs((i) * math.cos(ang) + (j) * math.sin(ang))
            #almaceno el nuevo angulo si no esta    
                if not ang in angles:  
                    angles.append(ang)
                #agrego p y ang 
                temp.append((p, ang))
            else:
                #si 'x' y 'y' son 0 entonces no hay p ni angulo
                temp.append((None, None))
        List.append(temp)
    
    pixels = image.load()
    #recorro la imagen buscando igualdad en las coordenadas registradas y comparo el angulo cambiando el color dependiendo de este
    for i in range(width):
        for j in range(height):
            if i > 0 and j > 0 and i < width and j < height:
                p, ang = List[i][j]
                #busco si mi p y angulo no es (None, None),si cumple, coloreo dependiendo del angulo
                if (p, ang != None,None):
                    if ang == 0:
                        pixels[i, j] = (255, 0, 0)
                        count_x += 1
                    elif ang == 90:
                        pixels[i, j] = (0, 0, 255)
                        count_y += 1
                        
    print "horizontal pixels: %s" %count_x
    print "vertical pixels: %s" %count_y
    image.save('New_lines.png', 'png')
    return image

if __name__ == "__main__":
    main()

