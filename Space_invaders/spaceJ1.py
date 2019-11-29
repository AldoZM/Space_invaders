import threading
import pygame,sys
from pygame.locals import *
from random import randint

#
#   Variables Globales
#

ancho = 1330
alto = 710
listaEnemigo=[]


#class Cursor(pygame.sprite.Sprite):
    
#    def __init__(self, posx, posy):
#        self.sprite.Sprite.__init__(self)
#        self.ImagenCursor = pygame.image.load('cursorGif.gif')
#        self.rect = self.ImagenCursor.get_rect()
#        self.rect.posx, self.rect.posy = pygame.mouse.get_pos()
    
#    def dibujar(self,superficie):
#        superficie.blit(self.ImagenCursor,self.rect)



class NaveEsp(pygame.sprite.Sprite):

    ####Clase de la nave####

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImgenNave = pygame.image.load('defensor_p.png')

        self.rect = self.ImgenNave.get_rect()
        self.rect.centerx = ancho/2
        self.rect.centery = alto-30
        
        self.listaDisparo =[]
        self.Vida = True

        self.velocidad = 10

    ####El movimiento de la nave####

    def movimiento(self):
        if self.Vida == True:
            if self.rect.left <=0:
                self.rect.left = 0
            elif self.rect.right>1300:
                self.rect.right = 1300



    ####La acción de dispara####

    def dispara(self,x,y):
        print("Dispara")
        mi_proyectil = proyectil(x,y,'Proyectil_muy_pequeño.png', True)
        self.listaDisparo.append(mi_proyectil)

    def destruccion(self):
        self.vida= False
        self.velocidad = 0

    def dibujar(self,superficie):
        superficie.blit(self.ImgenNave,self.rect)


class proyectil(pygame.sprite.Sprite): #Esta es la clase del proyectil 
    #
    #   Las propiedades del proyectil
    #
    def __init__(self,posx,posy, ruta, personaje):
        pygame.sprite.Sprite.__init__(self)

        self.ima_proyectil = pygame.image.load(ruta)

        self.rect = self.ima_proyectil.get_rect()

        self.velocidadDisparo = 4

        self.rect.top = posy
        self.rect.left = posx

        self.disparoPersonaje = personaje
    #
    #La direccion a la cual se va el proyectil 
    #
    def trayectoria(self):
        if self.disparoPersonaje == True:
            self.rect.top = self.rect.top - self.velocidadDisparo
        else:
            self.rect.top = self.rect.top + self.velocidadDisparo
    #
    # Aqui se carga la imagen del proyectil
    #
    def dibujar(self, superficie):
        superficie.blit(self.ima_proyectil,self.rect)

class Invasor(pygame.sprite.Sprite): # Clase enemigo
    #
    # Las propiedades del Invasor
    #
    def __init__(self,posx,posy,distancia, imagenUno, imagenDos):
        pygame.sprite.Sprite.__init__(self)

        #
        #   Esta parte es para la animacion del personaje, para cargar las imagenes y pueda verse la animacion (las marcare con una flecha)
        #

        self.imaEnem = pygame.image.load(imagenUno)#<---
        self.imaEnem2 = pygame.image.load(imagenDos)#<---
        #
        self.listaImagen = [self.imaEnem,self.imaEnem2]
        
        self.posIma = 0 
        self.imagenInvasor = self.listaImagen[self.posIma]
        self.rect = self.imagenInvasor.get_rect()
        
        self.listaDisparo = []
        self.velocidad = 5
        ### Les cambiare el sentido 
        ## El sentido horiginal es 

        #self.rect.top = posx
        #self.rect.left = posy

        self.rect.top = posy
        self.rect.left = posx

        self.rangoDisparo = 5
        self.tiempoCambio = 1

        self.conquista = False

        self.derecha = True
        self.contador = 0 
        self.maxDesenso = self.rect.top + 40 

        self.limiteDerecha = posx + distancia
        self.limiteIzquierda = posx - distancia

    #
    # Aqui es donde se dibuja sl sprite de la nave 
    #

    def dibujar(self, superficie):
        self.imagenInvasor = self.listaImagen[self.posIma]
        superficie.blit(self.imagenInvasor,self.rect)

    def comportamiento(self, tiempo):
        if self.conquista == False:
            self.__movimiento()

            self.__ataque()
            #
            # El cambio de la imagen para que se note la animacion del enemigo 
            #
            if self.tiempoCambio == tiempo:
                self.posIma += 1
                self.tiempoCambio += 1

                if self.posIma > len(self.listaImagen)-1:
                    self.posIma = 0

    def __movimiento(self):
        if self.contador <3:
            self.__movimientoLateral()
        else:
            self.__decenso()

    def __decenso(self):
        if self.maxDesenso == self.rect.top:
            self.contador = 0
            self.maxDesenso = self.rect.top + 40
        else:
            self.rect.top += 1

    #
    #   
    #

    def __movimientoLateral(self):
        
        #
        #   Aqui es para que la funcion este analizando constante mente usanod fuerza fruta para ver que este siempren en True
        #

        if self.derecha == True:
            self.rect.left = self.rect.left + self.velocidad
            if self.rect.left > self.limiteDerecha:
                self.derecha = False

                #
                #   Se agrega este contador para saber la cantidad de vueltas que ha echo el invasor
                #

                self.contador += 1
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left < self.limiteIzquierda:
                self.derecha = True


    def __ataque(self):

        #
        #   Aqui es para darle un valor (entero) en un rango de 'a' hasta 'b' para determinar si  va disparar o no 
        #

        if (randint(0,2000)<self.rangoDisparo):
            self.__disparo()

    def __disparo(self):
        x,y = self.rect.center
        mi_proyectil = proyectil(x,y,'Proyectil_muy_pequeño.png', False)
        self.listaDisparo.append(mi_proyectil)

#
#   Esta funcion se encarga de ver si el juego esta corriendo o no (porque esta dentro de un booleano)
#

def detenerJuego ():
    for enemigo in listaEnemigo:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo)

        enemigo.comquista = True

#
#   Aqui se carga la lista de los enemigos utilizando un for para llenarlo 
#

def cargarEnemigos():
    posx = -50
    for x in range(1,7):
        enemigo = Invasor(posx,0,200,'peon.png','peon2.png')
        listaEnemigo.append(enemigo)
        posx = posx + 200

    posx = 100
    for x in range(1,7):
        enemigo = Invasor(posx,100,200,'little_bad_ship.png','little_bad_ship_fase2.png')
        listaEnemigo.append(enemigo)
        posx = posx + 200

    posx = 0
    for x in range(1,7):
        enemigo = Invasor(posx,200,200,'lttle_ship.png','little_ship_fase2.png')
        listaEnemigo.append(enemigo)
        posx = posx + 200
    
#
#   Esta funcion reinicia el juego cuando el jugador aya perdido
#

def reiniciarJuego():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    SpaceInvader()
                    
                    print("Se reinicio el juego")


#
#   Funje como el main del programa
#

def SpaceInvader(): 
    
    pygame.init()
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Space Invader")

    ima_fondo = pygame.image.load('fondo.jpg') #SE ESCOJE LA IMAGEN PARA LE FONDO DE PANTALLA
    

    miFuenteSistema = pygame.font.SysFont('Arial',100,True)
    Texto = miFuenteSistema.render("FIN DEL JUEGO", 0,(120,100,40))
    
    puntosJ1 = 0

 

    
    jugador = NaveEsp()
    cargarEnemigos()
    enJuego = True
    reloj = pygame.time.Clock()
    
    while True:
        aux=1
        reloj.tick(60)

        tiempo = pygame.time.get_ticks()/1000
        #puntajeTiempo = pygame.time


        miFuentePuntuajeJ1 = pygame.font.SysFont('Arial',30,True,True)
        TextoPuntajeJ1 = miFuentePuntuajeJ1.render("Tu puntaje J1: "+str(puntosJ1),0,(255,255,0))
        

        fuenteReinicio = pygame.font.SysFont('Arial',30,True,True)
        textoReinicio = fuenteReinicio.render("Siquieres reintentar presiona *R*", 0,(120,100,40))

        fuenteGanar = pygame.font.SysFont('Arial',100,True,True)
        textoGanar = fuenteGanar.render("Ganaste!!!", 0,(120,100,40))
    
        jugador.movimiento()


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if enJuego == True:
                #
                #   Aqui se establece los controles del J1
                #
                if event.type == pygame.KEYDOWN:
                    if event.key == K_a:
                        jugador.rect.left -= jugador.velocidad
                        print("LEFT J1")

                    elif event.key == K_d:
                        jugador.rect.right += jugador.velocidad
                        print("RIGHT J1")

                    elif event.key == K_w:
                        x,y = jugador.rect.center
                        jugador.dispara(x,y)
                        print("Dispara J1")
       
       #
       # Aqui solo enseña o dibuja los sprites llamados
       #
        ventana.blit(ima_fondo, (0,0)) #Se crea el fondo 
        ###enemigo.comportamiento(tiempo)
        jugador.dibujar(ventana)
       
        ###enemigo.dibujar(ventana)
        if len(listaEnemigo)>0:
            for enemigo in listaEnemigo:
                enemigo.comportamiento(tiempo)
                enemigo.dibujar(ventana)
                if enemigo.rect.colliderect(jugador.rect):
                    detenerJuego()
                    jugador.destruccion()
                    
                    enJuego = False

                


                    
                if len(enemigo.listaDisparo)>0:
                    for x in enemigo.listaDisparo:
                        x.dibujar(ventana)
                        x.trayectoria()

                        if x.rect.colliderect(jugador.rect):
                            jugador.destruccion()
                            detenerJuego()
                            enJuego=False
                            
                        

                            detenerJuego()
                            enJuego=False

                        if x.rect.top > 750:
                            enemigo.listaDisparo.remove(x)
                        else:
                            for disparo in jugador.listaDisparo:
                                if x.rect.colliderect(disparo.rect):
                                    jugador.listaDisparo.remove(disparo)
                                    enemigo.listaDisparo.remove(x)
                            
        #
        # Lo que hace esta secuencia if es crear la secuancia de disparo del jugador 1
        #
        if len(jugador.listaDisparo)>0:
            for x in jugador.listaDisparo:
                x.dibujar(ventana)
                x.trayectoria()

                if x.rect.top > 700:
                    jugador.listaDisparo.remove(x)
                else:
                    for enemigo in listaEnemigo:
                        if x.rect.colliderect(enemigo.rect):
                            listaEnemigo.remove(enemigo)
                            jugador.listaDisparo.remove(x)
                            puntosJ1 += 100

        #
        # Lo que hace esta secuencia if es crear la secuancia de disparo del invasor 
        #
        """if len(enemigo.listaDisparo)>0:
            for x in enemigo.listaDisparo:
                x.dibujar(ventana)
                x.trayectoria()

                if x.rect.top > 650:
                    enemigo.listaDisparo.remove(x)
        """
        #
        # Lo que hace esta secuencia if es crear la secuancia de disparo del jugador 2
        #
        
        
      

        if enJuego == False:
            pygame.mixer.music.fadeout(3000)
            #pygame.draw.rect(ventana,(255,255,255),(450,300,300,200))
            ventana.blit(Texto,(300,300))
            ventana.blit(textoReinicio,(430,450))
            pygame.display.update()
            for enemigo in listaEnemigo:
                listaEnemigo.remove(enemigo)
            reiniciarJuego()
        else:
            if len(listaEnemigo)== 0 :

                ventana.blit(textoGanar,(450,300))
                ventana.blit(textoReinicio,(430,450))
                reiniciarJuego()
            
            
            
        #
        # Actualiza el juego de forma contante 
        #

        #ventana.blit(contador, (0,150))
        ventana.blit(TextoPuntajeJ1,(0,0))
        
        pygame.display.update()



SpaceInvader()

