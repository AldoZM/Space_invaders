import pygame, sys, os 
from pygame.locals import *

pygame.init()
ventana = pygame.display.set_mode((1010,710))
pygame.display.set_caption("Menu")
vista = True
blanco = (255,255,255)
while vista:

	miFuenteJ1 = pygame.font.SysFont('Arial',30,True,True)
	TextoJ1 = miFuenteJ1.render("Preciona la tecla * 1 * si quieres jugar solo",0,(0,0,0))

	miFuenteJ2 = pygame.font.SysFont('Arial',30,True,True)
	TextoJ2 = miFuenteJ2.render("Preciona la tecla * 2 * si quieres jugar en equipo",0,(0,0,0))

	credito = pygame.font.SysFont('Arial',30,True,True)
	CreditoDiseñador = credito.render("Preciona la tecla * C * si te interesa saber quien hizo esto",0,(0,0,0))

	TwoPlayers = pygame.image.load("TwoPlayers(samll).png")
	TituloJuego = pygame.image.load("space.png")

	ventana.fill(blanco)

	for evento in pygame.event.get():
		if evento.type == QUIT:
			pygame.quit()
			sys.exit()

		if evento.type == pygame.KEYDOWN:
			if evento.key == K_1:
				print("juego 1")
				comando = "python3 spaceJ1.py"
				os.system(comando)
				pygame.quit()
				sys.exit()
				vista = False            	
			elif evento.key == K_2:
				comando = "python3 space.py"
				os.system(comando)
				pygame.quit()
				sys.exit()
				vista = False            	
			elif evento.key == K_c:
				print("\n")
				print("Echo por Aldo Zetina Muciño con colaboracion de Juan\n")
				print("Este juego es para presentarse al profesor Ricardo Martinez Monero")
				print("\n")

	ventana.blit(CreditoDiseñador,(135,600))
	ventana.blit(TextoJ2,(185,550))
	ventana.blit(TextoJ1,(225,500))
	ventana.blit(TituloJuego,(0,0))
	ventana.blit(TwoPlayers, (425,250))
	pygame.display.update()