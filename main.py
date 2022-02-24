#####################################################
# Autores:
# Islas Ramirez William Brandom
# Sosa Garcia Oscar
# Valdez Hernandez Fernando
# 
# 15/01/2020
#
# Programa en Python ejecutado dentro de una Raspberry Pi3
# Las librerias y paquetes fueron instalados dentro 
# del Controlador mediante la instalación de la distribución 
# de Linux basado en Debian, Raspbian OS
#########################################################

#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk 
import time                     #Para las pausas
import cv2 #Para camara y vision artificial
import matplotlib.pyplot as plt
import numpy as np
# import RPi.GPIO as GPIO
# import serial

# Archivos con los datos (banco de imagenes de las hortalizas)

# import keras
# from keras.models import load_model
# print('leyendo modelo')
# modelorabano= load_model('rabano_200_trap_2.h5')
# modelozanahoria=load_model('zanahoria_200_trap_3.h5')
# modelojitomate=load_model('jitomate_200_trap_2.h5')
# modelolechuga=load_model('lechuga_200_trap_2.h5')
# print('modelo leido')


# GPIO.setmode(GPIO.BOARD)        
# GPIO.setwarnings(False)               

#Declarar pines a utilizar
dirx   = 3                   #Salida direccion x
dirx1  = 7
spx = 5                   #Salida pasos x
diry   = 21
spy = 23
dirz   = 29
spz = 31
iniconv=37
enabley=8
enablez=10
enablex=12
#Pra la heramienta de maleza: z=5550,z2=5660 ,x=30, y=3655# enx regresar 15 pasos mas
#Para la herramienta de plantar: x=30 y=2860 z=5550 y=-10
#Para la herramienta riego: x=35 y=2072
##Recalculos:
#Para la h1: x=35, y=2062, z=5210 z2=5330
#para h2 x=35 y=2865 z=5210 z2=5290
#para blablaba x=5210 z2=5280
xh1='35\n'
yx1='2062\n'
xh2='35\n'
yh2='2865\n'
xh3='35\n'
yh3='3665\n'

#para sembrar las semillas z=5100
#Tiempos y variables planteadas

 #Altura que el robot baja para DEJAR la herramienta
zsemilla=1690 #Altura que el robot baja para TOMAR una semilla
zsemilla2=4925 #sube el brazo
zplantar=7680  #7680 #Altura para enterrar la semilla
zeliminacion=7670 #Profundidad Elimina maleza
#Parametros de Bombas
bombaagua= 15 #Pin de salida de la bomba de agua
bombasemilla= 16 #Pin de salida de la bomba de vacio de las semillas
microPausa = 0.005 #Velocidad que se les da a los motores, actualmente 4 ms
tiemporegado=3 #Tiempo que se activa la bomba de agua

#Definir entradas y salidas, en nuestro caso solo salidas
GPIO.setup(dirx,GPIO.OUT)
GPIO.setup(dirx1,GPIO.OUT)
GPIO.setup(spx,GPIO.OUT)
GPIO.setup(diry,GPIO.OUT)
GPIO.setup(spy,GPIO.OUT)
GPIO.setup(dirz,GPIO.OUT)
GPIO.setup(spz,GPIO.OUT)
GPIO.setup(bombaagua,GPIO.OUT)
GPIO.setup(bombasemilla,GPIO.OUT)
GPIO.setup(iniconv,GPIO.OUT)
GPIO.setup(enabley,GPIO.IN)
GPIO.setup(enablez,GPIO.IN)
GPIO.setup(enablex,GPIO.IN)



#Configuracion de la ventana de la interfaz
window = Tk() #nombre de la ventana
window.title("Super Driver") #titulo de la ventana
window.geometry('900x700')#tamaño de la ventana
color="sienna4"#fondo 1
colormargen="grey27"#fondo 2
window.configure(background=color) #color de fondo de la ventana
# GPIO.output(bombaagua,False)
# GPIO.output(bombasemilla,False)

##Funciones del robot

def cambiovalores():
    sensor1=40
    sensor2=75
    sensor3=79
    sensor4=35
    time.sleep(4)
    SenLec['text']=str(sensor1)+' %'
    SenZan['text']=str(sensor2)+' %'
    SenRab['text']=str(sensor3)+' %'
    SenJit['text']=str(sensor4)+' %'

    
#En esta funcion, el robot toma la herramienta de riego, y va casilla por casilla regando
def regadoautomatico():
    print("abriendo puerto")
    arduino=serial.Serial('/dev/ttyUSB0',9600)
    GPIO.output(37,True)
    time.sleep(2)
    GPIO.output(37,False)
    time.sleep(1)
    print("puertoabierto")
    valores=arduino.readline()
    print(valores)
    sensor1=valores[0:4]
    sensor1=int(sensor1)
    sensor1=int(sensor1*100/1024)
    sensor2=valores[5:9]
    sensor2=int(sensor2)
    sensor2=int(sensor2*100/1024)
    sensor3=valores[10:14]
    sensor3=int(sensor3)
    sensor3=int(sensor3*100/1024)
    sensor4=valores[15:19]
    sensor4=int(sensor4)
    sensor4=int(sensor4*100/1024)
    arduino.close()    
    SenLec['text']=str(sensor1)+' %'
    SenZan['text']=str(sensor2)+' %'
    SenRab['text']=str(sensor3)+' %'
    SenJit['text']=str(sensor4)+' %'
    revision=0
    print(revision)
    if(sensor1<60):
        revision=revision+1
    if(sensor2<55):
        revision=revision+1
    if(sensor3<85):
        revision=revision+1
    if(sensor4<90):
        revision=revision+1
    print(revision)
    if(revision>0):
        tomadeherramienta(1)
        #Mover el robot a la posicion a regar
        print('herramienta regadora lista')
        if(sensor1<60):
            regarcasillas(1,6)
            print("se regaran lechugas")
        if(sensor2<55):
            regarcasillas(6,22)
            print("se regaran zanahorias")
        if(sensor3<85):
            regarcasillas(22,38)
            print("se regaran rabanos")
        if(sensor4<90):
            regarcasillas(38,43)
            print("se regaran tomates")
        print('terminado de regar')
        #Regresar Herramienta
        #Posicionar a y distancia
        dejarherramienta(1)
        print('herramienta desacoplada')
        
        #INicia vision automatica       print('iniciando monitoreo')
    #Prueba de la herramienta    
      tomadeherramienta(3)
      for i in range(1,43):
          posactx=posicionx(0)
          posdeseadax=posicionx(i)
          posacty=posiciony(0)
          posdeseaday=posiciony(i)
          movimientoxy(posactx,posacty,posdeseadax,posdeseaday)
          limitante=i
          if(limitante==5 or limitante==12 or limitante==19 or limitante==38):
            controldellimitante(limitante)
          else:
              time.sleep(4)
      dejarherramienta(3)
      print('herramienta desacoplada')
    #Regresamos a 0,0,0
      posactx=posicionx(0)
      posacty=posiciony(0)
      movimientoxy(posactx,posacty,'0\n','0\n')
      print('estando en 0,0')


def regarcasillas(minima,maxima):
    for i in range(minima,maxima): #1,43
        actual=str(i)+'\n'
        posactx=posicionx(0)
        posdeseadax=posicionx(i)
        posacty=posiciony(0)
        posdeseaday=posiciony(i)
        movimientoxy(posactx,posacty,posdeseadax,posdeseaday)
        #Activar la bomba
        print('Regando casilla: ',int(posdeseadax),int(posdeseaday))
        time.sleep(2)
        GPIO.output(bombaagua,True)
        if(i<3):
            time.sleep(4)
        else:
            time.sleep(3)
        GPIO.output(bombaagua,False)
        time.sleep(5)
#En esta funcion, el robot toma la herramienta de plantar, va a la semilla correspondiente, y va a plantar la semilla
def plantar():
    print('iniciando plantado')
    tomadeherramienta(2)
    aplantar=Plantas.get()
    #seleccionar semilla
    deseadax='0\n'
    deseaday='0\n'
    if aplantar=='Lechuga':
        deseadax='0\n'
        deseaday='2455\n'#-95, 4650 en z,35 #Z MAX PARA PLANTAR: 7250
    elif aplantar=="Zanahoria":
        deseadax='0\n'
        deseaday='2585\n' # -95, 65
    elif aplantar=="Rabano":
        deseadax='0\n'
        deseaday='3305\n'
    elif aplantar=="Jitomate":
        deseadax='0\n'
        deseaday='3395\n'
    print('cogiendo semilla')
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,deseadax,deseaday)
    #Bajar robot para tomar semilla
    movimientoz(0,zsemilla)
    #ENcender bomba para tomar semillas
    GPIO.output(bombasemilla,True)
    time.sleep(6)
    #SUbir robot
    movimientoz(zsemilla2,0)
    #Mover el robot a la posicion a plantar
    print('herramienta plantadora lista')
    posactx=posicionx(0)
    posdeseadax=posicionx(selected.get())
    posacty=posiciony(0)
    posdeseaday=posiciony(selected.get())
    movimientoxy(posactx,posacty,posdeseadax,posdeseaday)
    #Bajar para plantar
    movimientoz(0,zplantar)
    time.sleep(3)
    GPIO.output(bombasemilla,False)
    time.sleep(3)
    movimientoz(zplantar,0)
    print('terminado de plantar')
    GPIO.output(bombasemilla,True)
    time.sleep(3)
    GPIO.output(bombasemilla,False)
    #Regresar Herramienta
    dejarherramienta(2)
    print('herramienta desacoplada')
    #Regresamos a 0,0,0
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'0\n','0\n')
    print('estando en 0,0')

#Misma rutina que el regado, pero solo a una casilla
def regar():
    print('iniciando regado')
    tomadeherramienta(1)
    print('herramienta regadora lista')
    posactx=posicionx(0)
    posdeseadax=posicionx(selected.get())
    posacty=posiciony(0)
    posdeseaday=posiciony(selected.get())
    movimientoxy(posactx,posacty,posdeseadax,posdeseaday)
    #Activar la bomba
    time.sleep(2)
    GPIO.output(bombaagua,True)
    time.sleep(3)
    GPIO.output(bombaagua,False)
    time.sleep(5)
    print('terminado de regar')
    #Regresar Herramienta
    #Posicionar a y distancia
    dejarherramienta(1)
    print('herramienta desacoplada')
    #Regresamos a 0,0,0
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'0\n','0\n')
    print('estando en 0,0')
    
#Para tomar la herramienta de maleza, y tomar la foto, mandando llamar a la funcion de vision artificial
def monitorear():
    print('iniciando monitoreo')
    #Prueba de la herramienta    
    tomadeherramienta(3)
    #Mover el robot a la posicion a observar
    posactx=posicionx(0)
    posdeseadax=posicionx(selected.get())
    posacty=posiciony(0)
    posdeseaday=posiciony(selected.get())
    movimientoxy(posactx,posacty,posdeseadax,posdeseaday)
    limitante=selected.get()
    controldellimitante(limitante)
    #SI la vision artificial da un resultado positivo, aqui poner el if y la secuencia de cambio de herramienta, calculos de distancia y movimiento del robot para la eliminacion
    #regresar la herramienta
    #Posicionar a y distancia
    dejarherramienta(3)
    print('herramienta desacoplada')
    #Regresamos a 0,0,0
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'0\n','0\n')
    print('estando en 0,0')
    
    
    
def controldellimitante(limitante):
    if(limitante==1):
        xmin=180
        xmax=500
        ymin=0
        ymax=390
    elif(limitante==2 or limitante==6 or limitante==7):
        xmin=180
        xmax=640
        ymin=0
        ymax=440
    elif(limitante==8):
        xmin=180
        xmax=640
        ymin=200
        ymax=440
    elif(limitante==9):
        xmin=180
        xmax=640
        ymin=220
        ymax=480
    elif(limitante==4):
        xmin=185
        xmax=600
        ymin=0
        ymax=390        
    elif(limitante==22 or limitante==26 or limitante==30):
        xmin=0
        xmax=640
        ymin=0
        ymax=390
    elif(limitante==34):
        xmin=0
        xmax=330
        ymin=0
        ymax=390
    elif(limitante==35 or limitante==36 or limitante==41):
        xmin=0
        xmax=330
        ymin=0
        ymax=480
    elif(limitante==37):
        xmin=0
        xmax=200
        ymin=0
        ymax=480
    elif(limitante==42):
        xmin=0
        xmax=330
        ymin=220
        ymax=480
    elif(limitante==39 or limitante==13 or limitante==17 or limitante==21):
        xmin=0
        xmax=640
        ymin=220
        ymax=480
    elif(limitante==11 or limitante==10):
        xmin=50
        xmax=640
        ymin=0
        ymax=480
    elif(limitante==12):
        xmin=50
        xmax=640
        ymin=150
        ymax=480
    elif(limitante==16):
        xmin=0
        xmax=640
        ymin=150
        ymax=480
    elif(limitante==20):
        xmin=0
        xmax=640
        ymin=150
        ymax=480
    elif(limitante==27):
        xmin=0
        xmax=640
        ymin=0
        ymax=420
    elif(limitante==31 or limitante==32):
        xmin=0
        xmax=580
        ymin=0
        ymax=420
    elif(limitante==3):
        xmin=0
        xmax=640
        ymin=0
        ymax=350
    elif(limitante==23):
        xmin=90
        xmax=640
        ymin=0
        ymax=480
    elif(limitante==24):
        xmin=90
        xmax=640
        ymin=0
        ymax=480
    elif(limitante==33):
        xmin=0
        xmax=640
        ymin=0
        ymax=340
    else:
        xmin=0
        xmax=640
        ymin=0
        ymax=480
    visionartificial(xmin,xmax,ymin,ymax,limitante)
    
# #Limites para la deteccion de objetos:
#         #Se define de la siguiente manera:
#         #cx>xmin and cx<xmax and cy>ymin and cy<ymax
#         #Superior
#         #xmin=180 xmax=640 ymin=0 ymax=480
#         #inferior
#         #xmin=0 xmax=330 ymin=0 ymax=480
#         #izquierdo
#         #xmin=0 xmax=640 ymin=0 ymax=390
#         #derecho
#         #xmin=0 xmax=640 ymin=220 ymax=480
#         #der superior
#         #xmin=180 xmax=640 ymin=220 ymax=480
#         #izq sup
#         #xmin=180 xmax=640 ymin=0 ymax=390
#         #der inf
#         # 0 330 220 480
#         #izq inf
#         #0 330 0 390    
    
# #Posiciones de las herramientas del cabezal al ser tomadas
def tomadeherramienta(h):
    print('Dirigiendose a la herramienta')
    if(h==1):
        print('regadera sel')
        xh1='35\n'
        yh1='2068\n'
        z1=5235 #Altura que el robot baja para TOMAR la herramienta
        zfinale=5235
    elif(h==2):
        print('plantar sel')
        xh1='35\n'
        yh1='2865\n'
        z1=5260
        zfinale=2025
    elif(h==3):
        print('maleza sel')
        xh1='35\n'
        yh1='3664\n'
        z1=5235
        zfinale=5259
    posactx=posicionx(0)
    posacty=posiciony(0)
    #Mover al robot sobre la herramienta, cambiar valores de acuerdo a lo calculado
    movimientoxy(posactx,posacty,xh1,yh1)
    #Bajar el robot en z para tomar la herramienta
    movimientoz(0,z1)
    #sacar el robot en x para sacar la herramienta
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'600\n',yh1)
    #ELevar el robot
    movimientoz(zfinale,0)
    #Mover el robot a la posicion a regar
    print('herramienta lista')

#Posiciones de las herramientas al ser devueltas
def dejarherramienta(h):
    #Regresar Herramienta
    #Posicionar a y distancia
    print('Dirigiendose a la herramienta')
    if(h==1):
        print('regadera sel')
        xh1='10\n'
        yh1='2068\n'
        z2=5357
    elif(h==2):
        print('plantar sel')
        xh1='10\n'
        yh1='2865\n'
        z2=5310 #5350
    elif(h==3):
        print('maleza sel')
        xh1='10\n'
        yh1='3668\n'
        z2=5350
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'600\n',yh1)
    #Bajar el robot
    movimientoz(0,z2)
    #Dejamos la herramienta en el blablabla
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,xh1,yh1)
    #Subimos el robot par quitar la herramienta
    movimientoz(z2,0)




#Para controlar el robot se les dan las coordenadas iniciales y finales, 
# y el robot define el sentido y la cantidad de pasos a dar, solo en los ejes x, y
#A su vez, al finalizar, se reescribe la posicion actual del robot
def movimientoxy(x0,y0,xf,yf):
    print('movimiento en x y')
    print(x0,' ',xf)
    print(y0,' ',yf)
    movimientox=(int(xf)-int(x0))
    movimientoy=(int(yf)-int(y0))
    print(movimientox," ",movimientoy)
    #movimiento robot
    if movimientox>0:
        GPIO.output(dirx,1)
        GPIO.output(dirx1,0)
    else:
        GPIO.output(dirx,0)
        GPIO.output(dirx1,1)
    if movimientoy<0:
        GPIO.output(diry,0)
    else:
        GPIO.output(diry,1)
        
    if abs(movimientox)>=abs(movimientoy):
        print('x>=y')
        i=0
        for i in range(0,abs(movimientox)):
            lecturax=GPIO.input(enablex)
            lecturay=GPIO.input(enabley)
            if(lecturax==0):
                GPIO.output(spx, True)
                supercontador=0
            else:
                GPIO.output(spx,False)
                i=i-1
                supercontador=1
            if abs(movimientoy)>i:
                
                if(lecturay==0):
                    GPIO.output(spy, True)
                else:
                    GPIO.output(spy,False)
                    if(supercontador==0):
                        i=i-1
                #print(movimientoy)
                #print(i)
            time.sleep(microPausa)
            GPIO.output(spx, False)
            GPIO.output(spy, False)
            #print(movimientox)
            time.sleep(microPausa)
            print(abs(movimientox)-i)
        time.sleep(microPausa)
    else:
        print('x<y')
        for i in range(0,abs(movimientoy)):
            lecturay=GPIO.input(enabley)
            lecturax=GPIO.input(enablex)
            if(lecturay==0):
                GPIO.output(spy, True)
                supercontador=0
            else:
                GPIO.output(spy,False)
                i=i-1
                supercontador=1
            if abs(movimientox)>i:
                if(lecturax==0):
                    GPIO.output(spx, True)
                    supercontador==0
                else:
                    GPIO.output(spx,False)
                    if(supercontador==0):
                        i=i-1
                print(i)
                #print(movimientox)
            time.sleep(microPausa)
            GPIO.output(spx, False)
            GPIO.output(spy, False)
            #print(movimientoy)
            time.sleep(microPausa)
            print(abs(movimientoy)-i)
        time.sleep(microPausa)
    #Actualizacion posiciones
    f=open('posicionesx','r')
    aux=f.readlines()
    aux[0]=xf
    f.close()
    #print(aux)
    f=open('posicionesx','w')
    for i in range(0,44):
        f.write(aux[i])
        #print(aux[i])
    f.close()
    aux=[]
    f=open('posicionesy','r')
    aux=f.readlines()
    aux[0]=yf
    f.close()
    #print(aux)
    f=open('posicionesy','w')
    for i in range(0,44):
        f.write(aux[i])
        #print(aux[i])
    f.close()
    print('terminando x y')


#Misma logica, pero para el eje z
def movimientoz(z0,zf):
    print('movimiento z')
    movimientoz=(zf-z0)
    GPIO.output(spx,False)
    GPIO.output(spy,False)
    if movimientoz>0:
        GPIO.output(dirz,0)
    else:
        GPIO.output(dirz,1)
    for i in range(0,abs(movimientoz)):
        lecturaz=GPIO.input(enablez)
        if(lecturaz==0):
            GPIO.output(spz, True)
        else:
            GPIO.output(spz,False)
        time.sleep(microPausa)
        GPIO.output(spz, False)
        time.sleep(microPausa)
        print(abs(movimientoz)-i)
    time.sleep(microPausa)
    print('terminando z')

#Leer la posicion actual del robot en el eje y
def posiciony(posy):
    f=open('posicionesy','r')
    aux=f.readlines()
    posacty=aux[posy]
    f.close()
    return posacty


#Leer la posicion actual del robot en el eje x
def posicionx(posx):
    f=open('posicionesx','r')
    aux=f.readlines()
    posactx=aux[posx]
    f.close()
    return posactx

#Todo lo de la vision artificial
def visionartificial(xmin,xmax,ymin,ymax,limitante):
    #Abrimos la camara
    camara=cv2.VideoCapture(0)
    print('camara abierta')
    #Esperamos 60 frames para que la foto se tome correctamente
    for n in range(1,60):
        print(n)
        leido, frame  = camara.read()
    #verificamos que la foto se haya tomado correctamente
    if leido == True:
        cv2.imwrite("foto.jpg", frame)
        print("Foto tomada correctamente \n")
        nimage="foto.jpg"
        image=cv2.imread(nimage)
        image=cv2.resize(image,(640,480))
        #Guardamos la imagen original para iniciar su preprocesamiento
        #cv2.imshow('original', image)
        ##Convertir a escala de grises
        image2=image
        
        gris = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        n=7;
        #filtramos la imagen con un filtro gaussiano
        gaussiana=cv2.GaussianBlur(gris,(n,n),1);
        #Encontramos los objetos definiendo los umbrales
        t,dst=cv2.threshold(gaussiana,100,150,cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
        print('filtrando')
        #Dibujamos los contornos de los objetos
        contours, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # dibujar los contornos
        ##cv2.drawContours(image, contours, -1, (0, 0, 255), 2, cv2.LINE_AA)
        i=1
        print('procesando')
        aux=cv2.imread(nimage)
        aux=cv2.resize(aux,(640,480))
        #Pasamos cada objeto por cada una de las neuronas por cada planta
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            if w >=50 and h>=50 and w<400 and h<400:
                (x, y, w, h) = cv2.boundingRect(c)
                mensaje=' ob'+str(i)
                cv2.rectangle(aux, (x, y), (x + w, y + h), (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(aux,mensaje,(x+(w//2),y+(h//2)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
                i+=1
        cv2.imwrite("objetos.png", aux)
        i=1
        coorcentralx=300
        pasostotalesx=1600 #Revisar
        coorcentraly=420
        pasostotalesy=1200
        
        for c in contours:
            #area = cv2.contourArea(c)
            (x, y, w, h) = cv2.boundingRect(c)

            if w >=50 and h>=50 and w<400 and h<400:    
                momentos = cv2.moments(c)
                cx = int(momentos['m10']/momentos['m00'])
                cy = int(momentos['m01']/momentos['m00'])
                if cx>xmin and cx<xmax and cy>ymin and cy<ymax:
                    mensaje=f'Objeto {i}'
                    aux=cv2.imread(nimage)
                    aux=cv2.resize(aux,(640,480))
                    crop_img=aux[y:y+h,x:x+w]
                    img_ori= crop_img
                    cambiotamaño=200
                    img= cv2.resize(img_ori,(cambiotamaño,cambiotamaño),interpolation=cv2.INTER_CUBIC)
                    imagen_a_probar=np.reshape(img,(1,cambiotamaño,cambiotamaño,3))
                    predictions=modelorabano.predict_classes(imagen_a_probar)
                    print('primera neurona')
                    #print(predictions)
                    print('objeto: ',i)
                    if (predictions==0):
                        mensaje=f'{i} Ok1'            
                        print('rabano')
                    elif(predictions==1):
                        print('segunda neurona')
                        predictions2=modelolechuga.predict_classes(imagen_a_probar)
                        #print(predictions2)
                        if(predictions2==0):
                            mensaje=f'{i} Ok2'            
                            print('Lechuga')
                        elif(predictions2==1):
                            print('tercera neurona')
                            predictions3=modelojitomate.predict_classes(imagen_a_probar)
                            if(predictions3==0):
                                mensaje=f'{i} Ok3'            
                                print('jitomate')
                            elif(predictions3==1):
                                mensaje=f'{i} Maleza'
                                print('maleza')                                            
                                pixelesx=coorcentralx-cx
                                pasosacaminarenx=int(pixelesx*pasostotalesx/640)
                                posactx=int(posicionx(0))
                                auxx=str(posactx+pasosacaminarenx)
                                finalex=auxx+'\n'
                                
                                pixelesy=coorcentraly-cy
                                pasosacaminareny=int(pixelesy*pasostotalesy/480)
                                posacty=int(posiciony(0))
                                auxy=str(posacty+pasosacaminareny)
                                finaley=auxy+'\n'
                                                    
                                posactx=posicionx(0)
                                posacty=posiciony(0)
                                movimientoxy(posactx,posacty,finalex,finaley)
                                coorcentralx=cx
                                coorcentraly=cy
                                time.sleep(2)
                                movimientoz(0,zeliminacion)
                                #time.sleep(3)
                                #movimientoz(zeliminacion,0)
                                time.sleep(2)
                                movimientoz(800,0)
                                time.sleep(1)
                                movimientoz(0,800)
                                time.sleep(1)
                                movimientoz(800,0)
                                time.sleep(1)
                                movimientoz(0,800)
                                #time.sleep(1)
                                time.sleep(3)
                                movimientoz(zeliminacion,0)
                                nano='estando en objeto'+str(i)
                                print(nano)
                    (x, y, w, h) = cv2.boundingRect(c)        
                    cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.putText(image2,mensaje,(x+(w//2),y+(h//2)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
                    i+=1
        #cv2.imwrite('recorte.png',crop_img)
        ultradriver="procesada"+str(limitante)+".png"
        cv2.imwrite(ultradriver, image2)
        print('imagen procesada')
    else:
        print('Error al acceder a la camara')
    camara.release()
    print("ewe")


def btnExit():
    #Salida de la interfaz
    print('saliendo')
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'0\n','0\n')
    window.destroy()
    
    
#Organizacion de la interfaz
    
#Solo son las coordenadas de los botones y todo lo que lleva la interfaz.
f1=Frame(window,width=900,height=150,bg=colormargen)
f1.place(x=0,y=0)
f2=Frame(window,width=900,height=250,bg=colormargen)
f2.place(x=0,y=550)
f3=Frame(window,width=200,height=900,bg=colormargen)
f3.place(x=0,y=0)
f4=Frame(window,width=300,height=900,bg=colormargen)
f4.place(x=725,y=0)

f8=Frame(window,width=830,height=100,bg='grey67')
f8.place(x=35,y=565)

logoupiita=PhotoImage(file=r"logoupiita150.png")
f5=Label(window,image=logoupiita,bd=0)
f5.place(x=750,y=0)
logopoli=PhotoImage(file=r"logopoli150.png")
f6=Label(window,image=logopoli,bd=0)
f6.place(x=0,y=0)
f7=Label(window,text="INSTITUTO POLITÉCNICO NACIONAL",bg=colormargen,font=("Arial",15),fg="ghost white")
f7.place(x=270,y=20)
f9=Label(window,text="UNIDAD PROFESIONAL INTERDISCIPLINARIA EN INGENIERÍA Y TECNOLOGÍAS AVANZADAS",bg=colormargen,font=("Arial",10),fg="ghost white")
f9.place(x=153,y=55)
f10=Label(window,text="ROBOT CARTESIANO",bg=colormargen,font=("Arial",30),fg="ghost white")
f10.place(x=240,y=80)


HumLecLab=Label(window,text="Humedad:",bg=colormargen,font=("Arial",20),fg="ghost white")
HumLecLab.place(x=20,y=220)

HumZanLab=Label(window,text="Humedad:",bg=colormargen,font=("Arial",20),fg="ghost white")
HumZanLab.place(x=20,y=370)

HumRabLab=Label(window,text="Humedad:",bg=colormargen,font=("Arial",20),fg="ghost white")
HumRabLab.place(x=735,y=220)

HumJitLab=Label(window,text="Humedad:",bg=colormargen,font=("Arial",20),fg="ghost white")
HumJitLab.place(x=735,y=370)

SenLec=Label(window,text="70 %",bg=colormargen,font=("Arial",20),fg="ghost white")
SenLec.place(x=60,y=250)

SenZan=Label(window,text="69 %",bg=colormargen,font=("Arial",20),fg="ghost white")
SenZan.place(x=60,y=400)


SenRab=Label(window,text="72 %",bg=colormargen,font=("Arial",20),fg="ghost white")
SenRab.place(x=795,y=250)


SenJit=Label(window,text="71 %",bg=colormargen,font=("Arial",20),fg="ghost white")
SenJit.place(x=795,y=400)

Plantar=Button(window,text="Plantar",font=("Arial",18),background="lime green",height=1,width=10);
Monitorear=Button(window,text="Monitorear",font=("Arial",18),background="khaki1",height=1,width=10);
Regar=Button(window,text="Regar",font=("Arial",18),background="cyan",height=1,width=10);
Salir=Button(window,text="Salir",font=("Arial",18),background="Brown3",height=1,width=10,command=btnExit);
Rauto=Button(window,text="Automatico",font=("Arial",18),background="Skyblue2",height=1,width=10,command=cambiovalores);

ybotones=580
xbotones=50
Monitorear.place(x=xbotones,y=ybotones);
Plantar.place(x=xbotones+160,y=ybotones);
Regar.place(x=xbotones+(160*2),y=ybotones);
Salir.place(x=xbotones+(160*4),y=ybotones);
Rauto.place(x=xbotones+(160*3),y=ybotones);

Plantas=ttk.Combobox(window,font=("Arial",20),background="Brown3",height=30,width=8);
Plantas['values']=("Lechuga","Zanahoria","Rabano","Jitomate");
Plantas.current(1)
Plantas.place(x=218,y=625)


# ybotones=775
# xbotones=140
# Monitorear.place(x=xbotones,y=ybotones);
# Plantar.place(x=xbotones+125,y=ybotones);
# Regar.place(x=xbotones+(125*2),y=ybotones);
# Salir.place(x=xbotones+(125*4),y=ybotones);
# Rauto.place(x=xbotones+(125*3),y=ybotones);

# Plantas=ttk.Combobox(window,font=("Arial",15),background="Brown3",height=30,width=8);
# Plantas['values']=("Lechuga","Zanahoria","Rabano","Jitomate");
# Plantas.current(1)
# Plantas.place(x=270,y=825)



selected=IntVar()
lechuga1=Radiobutton(window,value=1,variable=selected,background=color);
lechuga2=Radiobutton(window,value=2,variable=selected,background=color);
lechuga3=Radiobutton(window,value=3,variable=selected,background=color);
lechuga4=Radiobutton(window,value=4,variable=selected,background=color);
lechuga5=Radiobutton(window,value=5,variable=selected,background=color);

zanahoria1=Radiobutton(window,value=6,variable=selected,background=color);
zanahoria2=Radiobutton(window,value=7,variable=selected,background=color);
zanahoria3=Radiobutton(window,value=8,variable=selected,background=color);
zanahoria4=Radiobutton(window,value=9,variable=selected,background=color);
zanahoria5=Radiobutton(window,value=10,variable=selected,background=color);
zanahoria6=Radiobutton(window,value=11,variable=selected,background=color);
zanahoria7=Radiobutton(window,value=12,variable=selected,background=color);
zanahoria8=Radiobutton(window,value=13,variable=selected,background=color);
zanahoria9=Radiobutton(window,value=14,variable=selected,background=color);
zanahoria10=Radiobutton(window,value=15,variable=selected,background=color);
zanahoria11=Radiobutton(window,value=16,variable=selected,background=color);
zanahoria12=Radiobutton(window,value=17,variable=selected,background=color);
zanahoria13=Radiobutton(window,value=18,variable=selected,background=color);
zanahoria14=Radiobutton(window,value=19,variable=selected,background=color);
zanahoria15=Radiobutton(window,value=20,variable=selected,background=color);
zanahoria16=Radiobutton(window,value=21,variable=selected,background=color);

rabano1=Radiobutton(window,value=22,variable=selected,background=color);
rabano2=Radiobutton(window,value=23,variable=selected,background=color);
rabano3=Radiobutton(window,value=24,variable=selected,background=color);
rabano4=Radiobutton(window,value=25,variable=selected,background=color);
rabano5=Radiobutton(window,value=26,variable=selected,background=color);
rabano6=Radiobutton(window,value=27,variable=selected,background=color);
rabano7=Radiobutton(window,value=28,variable=selected,background=color);
rabano8=Radiobutton(window,value=29,variable=selected,background=color);
rabano9=Radiobutton(window,value=30,variable=selected,background=color);
rabano10=Radiobutton(window,value=31,variable=selected,background=color);
rabano11=Radiobutton(window,value=32,variable=selected,background=color);
rabano12=Radiobutton(window,value=33,variable=selected,background=color);
rabano13=Radiobutton(window,value=34,variable=selected,background=color);
rabano14=Radiobutton(window,value=35,variable=selected,background=color);
rabano15=Radiobutton(window,value=36,variable=selected,background=color);
rabano16=Radiobutton(window,value=37,variable=selected,background=color);

jitomate1=Radiobutton(window,value=38,variable=selected,background=color);
jitomate2=Radiobutton(window,value=39,variable=selected,background=color);
jitomate3=Radiobutton(window,value=40,variable=selected,background=color);
jitomate4=Radiobutton(window,value=41,variable=selected,background=color);
jitomate5=Radiobutton(window,value=42,variable=selected,background=color);



lechuga1.place(x=235,y=175);
lechuga2.place(x=365,y=175);
lechuga3.place(x=300,y=225)
lechuga4.place(x=235,y=275);
lechuga5.place(x=365,y=275);


a=465
b=175
c=35
zanahoria1.place(x=a,y=b);
zanahoria2.place(x=a+66,y=b);
zanahoria3.place(x=a+(66*2),y=b);
zanahoria4.place(x=a+(66*3),y=b);
b=175+c
zanahoria5.place(x=a,y=b);
zanahoria6.place(x=a+(66),y=b);
zanahoria7.place(x=a+(66*2),y=b);
zanahoria8.place(x=a+(66*3),y=b);
b=175+(c*2)
zanahoria9.place(x=a,y=b);
zanahoria10.place(x=a+66,y=b);
zanahoria11.place(x=a+(66*2),y=b);
zanahoria12.place(x=a+(66*3),y=b);
b=175+(c*3)
zanahoria13.place(x=a,y=b);
zanahoria14.place(x=a+(66*1),y=b);
zanahoria15.place(x=a+(66*2),y=b);
zanahoria16.place(x=a+(66*3),y=b);
a=215
b=370
c=35
rabano1.place(x=a,y=b);
rabano2.place(x=a+(66*1),y=b);
rabano3.place(x=a+(66*2),y=b);
rabano4.place(x=a+(66*3),y=b);
b=370+c
rabano5.place(x=a,y=b);
rabano6.place(x=a+(66*1),y=b);
rabano7.place(x=a+(66*2),y=b);
rabano8.place(x=a+(66*3),y=b);
b=370+(c*2)
rabano9.place(x=a,y=b);
rabano10.place(x=a+(66*1),y=b);
rabano11.place(x=a+(66*2),y=b);
rabano12.place(x=a+(66*3),y=b);
b=370+(c*3)
rabano13.place(x=a,y=b);
rabano14.place(x=a+(66*1),y=b);
rabano15.place(x=a+(66*2),y=b);
rabano16.place(x=a+(66*3),y=b);


jitomate1.place(x=500,y=370)
jitomate2.place(x=650,y=370);
jitomate3.place(x=575,y=420)
jitomate4.place(x=500,y=470);
jitomate5.place(x=650,y=470);



window.mainloop()
print("detenido")
GPIO.cleanup()

