#----------Importation des modules nécessaires au fonctionnement du programme (dont PyGame)----------
from tkinter import *
from tkinter.messagebox import *
import pygame
from pygame.locals import *
from math import *
import ctypes  # An included library with Python install.

pygame.init()


#---------Déclaration des variables----------


#Paramètres
TaillePlateau=3 #Indiquer le nombre de colonnes du plateau
NumberLines=5 #Indiquer le nombre de lignes du plateau
CaseSize = 64 #Indiquer la taille en pixel de chaque case (dépend de la taille de la ressource)

#Variables
Level=1 #Indique le niveau actuel
HorizontalCaseLocation=0 #Permet de retenir la position horizontale des cases lors de la création du tableau
VerticalCaseLocation=0 #Permet de retenir la position verticale des cases lors de la création du tableau
SelectedPiece=0 #Indique la pièce sélectionnée
LocatedCaseColumn=0 #Indique la colonne de la case sélectrionnée
LocatedCaseLine=0 #Indique la ligne de la case sélectionnée
LocatedCaseNumber=0 #Indique le numéro de case sélectionné
CalculTemp=0 #Permet de stocker de manière temporaire un calcul ou une valeure
CalculTemp2=0 #Permet de stocker de manière temporaire un calcul ou une valeure
Rotate=1 #Indique la rotation de la pièce
Flip=1 #Indique le sens de la pièce
PieceToDelete=0 #Indique le numéro de la pièce à supprimer

#Listes
TablePiece=[] #Tableau de l'utilisation de l'espace du tableau
AvailablePieces=[0,1,2,2,1,1,1,1,1,1,2,1,1] #Tableau de liste de toutes les pièces disponibles


#----------Définition des fonctions----------

def ReDraw(): #Fonction d'affichage du plateau et de l'interface -> Entrée : Tableau de position des pièces ; Sortie : Plateau et pièces affichées dans la fenêtre
	Background = pygame.image.load("Ressources\Background.png").convert() #Création du fond
	fenetre.blit(Background, (0,0)) #Positionnement du fond
	Boucle=0 #Permet l'incrémentation des boucles
	Boucle2=0 #Permet l'incrémentation
	while Boucle < NumberLines: # Tant que la boucle est strictement inférieure au nombre de lignes voulues
		VerticalCaseLocation=CaseSize*Boucle #Détermination de l'emplacement vertical de la case
		Boucle=Boucle+1 #Incrémentation de la boucle
		Boucle2=0 #Initialisation de la deuxième boucle
		while Boucle2 < TaillePlateau: # Tant que la boucle est strictement inférieure au nombre de cases voulues sur la ligne
			HorizontalCaseLocation=CaseSize*Boucle2 #Détermination de l'emplacement horizontal de la case
			exec('Case'+' = pygame.image.load("Ressources\Case"+".png").convert()') #Création de la case
			exec('fenetre.blit(Case'+', ('+str(HorizontalCaseLocation)+','+str(VerticalCaseLocation)+'))') #Positionnement de la case
			Boucle2=Boucle2+1 #Incrémentation de la boucle
	Boucle=0 #Permet l'incrémentation des boucles
	Boucle2=len(TablePiece)/3 #Permet l'incrémentation
	while Boucle < Boucle2: #Tant que le nombre de cases prises incrémentés est inférieur au nombre de cases prises à afficher
		exec('Case'+' = pygame.image.load("Ressources\Case'+str(TablePiece[Boucle*3])+'"+".png").convert()') #Création de la case
		exec('fenetre.blit(Case'+', ('+str(TablePiece[Boucle*3+1])+','+str(TablePiece[Boucle*3+2])+'))') #Positionnement de la case
		Boucle=Boucle+1 #Incrémentation de la boucle
	APropos = pygame.image.load("Ressources\APropos.png").convert() #Création du bouton à propos de
	fenetre.blit(APropos, (1024-128,700-32)) #Positionnement du bouton à propos de



def CaseLocating(): #Fonction de détermination du numéro de case sélectionné -> Entrée : Aucune information particulière ; Sortie : Numéro de case sélectionnée
	LocatedCaseLine=floor(event.pos[1]/CaseSize)+1 #Indication du numéro de ligne de la case
	LocatedCaseColumn=floor(event.pos[0]/CaseSize)+1 #Indication du numéro de colonne de la case
	if LocatedCaseColumn>TaillePlateau: #Si la souris n'est pas sur le plateau
		LocatedCaseLine=0 #Neutralisation de l'opération
		LocatedCaseColumn=0 #Neutralisation de l'opération
	if LocatedCaseLine>NumberLines: #Si la souris n'est pas sur le plateau
		LocatedCaseLine=0 #Neutralisation de l'opération
		LocatedCaseColumn=0 #Neutralisation de l'opération
	LocatedCaseNumber=LocatedCaseColumn+TaillePlateau*(LocatedCaseLine-1) #Détermination du numéro de case
	if LocatedCaseNumber==-TaillePlateau: #Si on détecte que la case sélectionnée est incohérente
		LocatedCaseNumber=0 #Indication qu'aucune case n'a été sélectionnée
	return(LocatedCaseNumber)



def CaseVerifier(): #Fonction de vérification si les cases sont libres pour la pièce -> Entrée : Case choisie et pièce sélectionnée ; Sortie : Oui ou non, si la place est disponible pour insérer la pièce ou pas
	if SelectedPiece>0: #Si la pièce sélectionnée est supérieure à 0
		if LocatedCaseNumber>0: #Si la case sélectionnée est supérieure à 0
			CalculTemp=LocatedCaseNumber-floor(LocatedCaseNumber/TaillePlateau)*TaillePlateau #Calcul de la position X de la case
			CalculTemp2=floor(LocatedCaseNumber/TaillePlateau) #Calcul de la position Y de la case
			if CalculTemp==0: #Si la position X de la case est fausse
				CalculTemp=TaillePlateau #Rectification de la position de la case X
				CalculTemp2=CalculTemp2-1 #Rectification de la position de la case Y
	Boucle=0 #Initialisation de la boucle
	if SelectedPiece==1: #Si la pièce 1 est sélectionnée
		if Rotate==1: #Si la rotation de la pièce est de 1
			if (CalculTemp-1)*CaseSize+64*4 > CaseSize*(TaillePlateau-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*4 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2: #Si la rotation de la pièce est de 2
			if CaseSize*CalculTemp2+64*4 > CaseSize*(NumberLines-1):
			 return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*4: #Si une des cases nécessaires n'est pas disponible
					return 1 #Interdir l'ajout
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==2: #Si la pièce 2 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==1 and Flip==2: #Si la rotation de la pièce est de 1 avec miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==1: #Si la rotation de la pièce est de 3 sans miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==2: #Si la rotation de la pièce est de 3 avec miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==2: #Si la rotation de la pièce est de 2 avec miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==1: #Si la rotation de la pièce est de 4 sans miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==2: #Si la rotation de la pièce est de 4 avec miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==3: #Si la pièce 3 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==1 and Flip==2: #Si la rotation de la pièce est de 1 avec miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==1: #Si la rotation de la pièce est de 3 sans miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==2: #Si la rotation de la pièce est de 3 avec miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==2: #Si la rotation de la pièce est de 2 avec miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==1: #Si la rotation de la pièce est de 4 sans miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==2: #Si la rotation de la pièce est de 4 avec miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==4: #Si la pièce 4 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==1 and Flip==2: #Si la rotation de la pièce est de 1 avec miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==2: #Si la rotation de la pièce est de 3 avec miroir
			if (CalculTemp-1)*CaseSize+64*3 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*3 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==2: #Si la rotation de la pièce est de 2 avec miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==1: #Si la rotation de la pièce est de 4 sans miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==2: #Si la rotation de la pièce est de 4 avec miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*3 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*3 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==5: #Si la pièce 5 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==1: #Si la rotation de la pièce est de 3 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==1: #Si la rotation de la pièce est de 4 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==6: #Si la pièce 6 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==2: #Si la rotation de la pièce est de 3 avec miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==1 and Flip==2: #Si la rotation de la pièce est de 1 avec miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==1: #Si la rotation de la pièce est de 3 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64*1 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==2: #Si la rotation de la pièce est de 2 avec miroir
			if (CalculTemp-1)*CaseSize+64*1 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==1: #Si la rotation de la pièce est de 4 sans miroir
			if (CalculTemp-1)*CaseSize+64*1 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==2: #Si la rotation de la pièce est de 4 avec miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64*1 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==2: #Si la rotation de la pièce est de 2 avec miroir
			if (CalculTemp-1)*CaseSize+64*1 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==7: #Si la pièce 7 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*1 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==1: #Si la rotation de la pièce est de 3 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==1: #Si la rotation de la pièce est de 4 sans miroir
			if (CalculTemp-1)*CaseSize+64 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==8: #Si la pièce 8 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==1 and Flip==2: #Si la rotation de la pièce est de 1 avec miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==2: #Si la rotation de la pièce est de 1 avec miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==9: #Si la pièce 9 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==1 and Flip==2: #Si la rotation de la pièce est de 1 avec miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==2: #Si la rotation de la pièce est de 2 avec miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==2: #Si la rotation de la pièce est de 4 avec miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==1: #Si la rotation de la pièce est de 4 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==2: #Si la rotation de la pièce est de 3 avec miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==1: #Si la rotation de la pièce est de 3 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==10: #Si la pièce 10 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==1: #Si la rotation de la pièce est de 3 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==1: #Si la rotation de la pièce est de 4 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==11: #Si la pièce 11 est sélectionnée
		if Rotate==1 and Flip==1: #Si la rotation de la pièce est de 1 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==2 and Flip==1: #Si la rotation de la pièce est de 2 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==3 and Flip==1: #Si la rotation de la pièce est de 3 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
		elif Rotate==4 and Flip==1: #Si la rotation de la pièce est de 4 sans miroir
			if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
				return 1 #Interdir l'ajout
			while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
				if TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*0 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*0 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2: #Si une des cases nécessaires n'est pas disponible
					return 1
				Boucle=Boucle+1 #Incrémentation de la boucle
	elif SelectedPiece==12: #Si la pièce 12 est sélectionnée
		if (CalculTemp-1)*CaseSize+64*2 > CaseSize*(TaillePlateau-1) or CaseSize*CalculTemp2+64*2 > CaseSize*(NumberLines-1): #Si une extrémité de la pièce est en dehors du plateau
			return 1 #Interdir l'ajout
		while Boucle < len(TablePiece)-1: #Pour chaque valeur du tableau
			if TablePiece[Boucle] == (CalculTemp-1)*CaseSize and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*2 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*1 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2+64*2 or TablePiece[Boucle] == (CalculTemp-1)*CaseSize+64*1 and TablePiece[Boucle+1] == CaseSize*CalculTemp2: #Si une des cases nécessaires n'est pas disponible
				return 1
			Boucle=Boucle+1 #Incrémentation de la boucle



def AddPiece(): #Fonction d'ajout d'une pièce sur une case sélectionnée -> Entrée : Case sélectionnée ; Sortie : Pièce placée sur la case choisie
	if SelectedPiece>0: #Si la pièce sélectionnée est supérieure à 0
		if LocatedCaseNumber>0: #Si la case sélectionnée est supérieure à 0
			CalculTemp=LocatedCaseNumber-floor(LocatedCaseNumber/TaillePlateau)*TaillePlateau #Calcul de la position X de la case
			CalculTemp2=floor(LocatedCaseNumber/TaillePlateau) #Calcul de la position Y de la case
			if CalculTemp==0: #Si la position X de la case est fausse
				CalculTemp=TaillePlateau #Rectification de la position de la case X
				CalculTemp2=CalculTemp2-1 #Rectification de la position de la case Y
			if SelectedPiece==1: #Si la pièce 1 est sélectionnée
				if Rotate==1: #Si la pièce est dans le premier sens de rotation
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*4) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				else: #Si la pièce est dans le deuxième sens de rotation
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*4) #Modification de la case
			elif SelectedPiece==2: #Si la pièce 2 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				elif Rotate==1 and Flip==2: #Si la pièce est dans le sens de rotation 1 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				elif Rotate==3 and Flip==1: #Si la pièce est dans le sens de rotation 3 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==3 and Flip==2: #Si la pièce est dans le sens de rotation 3 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==2 and Flip==2: #Si la pièce est dans le sens de rotation 2 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==4 and Flip==1: #Si la pièce est dans le sens de rotation 4 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==4 and Flip==2: #Si la pièce est dans le sens de rotation 4 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
			elif SelectedPiece==3: #Si la pièce 3 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==1 and Flip==2: #Si la pièce est dans le sens de rotation 1 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==3 and Flip==1: #Si la pièce est dans le sens de rotation 3 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==3 and Flip==2: #Si la pièce est dans le sens de rotation 3 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==2 and Flip==2: #Si la pièce est dans le sens de rotation 2 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==4 and Flip==1: #Si la pièce est dans le sens de rotation 4 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				elif Rotate==4 and Flip==2: #Si la pièce est dans le sens de rotation 4 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
			elif SelectedPiece==4: #Si la pièce 4 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece); TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==1 and Flip==2: #Si la pièce est dans le sens de rotation 1 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==3 and Flip==1: #Si la pièce est dans le sens de rotation 3 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64); TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				elif Rotate==3 and Flip==2: #Si la pièce est dans le sens de rotation 3 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*3) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==2 and Flip==2: #Si la pièce est dans le sens de rotation 2 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==2 and Flip==2: #Si la pièce est dans le sens de rotation 2 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				elif Rotate==4 and Flip==1: #Si la pièce est dans le sens de rotation 4 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==4 and Flip==2: #Si la pièce est dans le sens de rotation 4 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*3) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
			elif SelectedPiece==5: #Si la pièce 5 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==3 and Flip==1: #Si la pièce est dans le sens de rotation 3 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==4 and Flip==1: #Si la pièce est dans le sens de rotation 4 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
			elif SelectedPiece==6: #Si la pièce 6 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==3 and Flip==2: #Si la pièce est dans le sens de rotation 3 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==1 and Flip==2: #Si la pièce est dans le sens de rotation 1 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==3 and Flip==1: #Si la pièce est dans le sens de rotation 3 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				elif Rotate==2 and Flip==2: #Si la pièce est dans le sens de rotation 2 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				elif Rotate==4 and Flip==1: #Si la pièce est dans le sens de rotation 4 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==4 and Flip==2: #Si la pièce est dans le sens de rotation 4 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				elif Rotate==2 and Flip==2: #Si la pièce est dans le sens de rotation 2 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
			elif SelectedPiece==7: #Si la pièce 7 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ;TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ;TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==3 and Flip==1: #Si la pièce est dans le sens de rotation 3 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				elif Rotate==4 and Flip==1: #Si la pièce est dans le sens de rotation 4 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
			elif SelectedPiece==8: #Si la pièce 8 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				elif Rotate==1 and Flip==2: #Si la pièce est dans le sens de rotation 1 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				elif Rotate==2 and Flip==2: #Si la pièce est dans le sens de rotation 2 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
			elif SelectedPiece==9: #Si la pièce 9 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				elif Rotate==1 and Flip==2: #Si la pièce est dans le sens de rotation 1 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				elif Rotate==2 and Flip==2: #Si la pièce est dans le sens de rotation 2 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==4 and Flip==2: #Si la pièce est dans le sens de rotation 4 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==4 and Flip==1: #Si la pièce est dans le sens de rotation 4 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==3 and Flip==2: #Si la pièce est dans le sens de rotation 3 avec miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				elif Rotate==3 and Flip==1: #Si la pièce est dans le sens de rotation 3 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
			elif SelectedPiece==10: #Si la pièce 10 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==3 and Flip==1: #Si la pièce est dans le sens de rotation 3 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==4 and Flip==1: #Si la pièce est dans le sens de rotation 4 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
			elif SelectedPiece==11: #Si la pièce 11 est sélectionnée
				if Rotate==1 and Flip==1: #Si la pièce est dans le sens de rotation 1 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				elif Rotate==2 and Flip==1: #Si la pièce est dans le sens de rotation 2 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				elif Rotate==3 and Flip==1: #Si la pièce est dans le sens de rotation 3 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				elif Rotate==4 and Flip==1: #Si la pièce est dans le sens de rotation 4 sans miroir
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*0) #Modification de la case
				    TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*0) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
			elif SelectedPiece==12: #Si la pièce 12 est sélectionnée
				TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*2) ; TablePiece.append(CaseSize*CalculTemp2+64*1) #Modification de la case
				TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2+64*2) #Modification de la case
				TablePiece.append(SelectedPiece) ; TablePiece.append((CalculTemp-1)*CaseSize+64*1) ; TablePiece.append(CaseSize*CalculTemp2) #Modification de la case
			pygame.display.flip() #Rafraichissement de l'écran



def DeletingProcedure(): #Fonction de suppression d'une pièce du plateau -> Entrée : Emplacement de la case sélectionnée ; Sortie : Pièce correspondante supprimée
	if LocatedCaseNumber>0: #Si la case sélectionnée est supérieure à 0
		CalculTemp=LocatedCaseNumber-floor(LocatedCaseNumber/TaillePlateau)*TaillePlateau-1 #Calcul de la position X de la case
		CalculTemp2=floor(LocatedCaseNumber/TaillePlateau) #Calcul de la position Y de la case
		if CalculTemp==-1: #Si la position X de la case est fausse
			CalculTemp=TaillePlateau-1 #Rectification de la position de la case X
			CalculTemp2=CalculTemp2-1 #Rectification de la position de la case Y
	PieceToDelete=0 #Initialisation du numéro de pièce à trouver
	Boucle=0 #Initialisation de la boucle
	while Boucle<len(TablePiece)-1: #Pour chaque entrée de la liste
		if TablePiece[Boucle]==CalculTemp*CaseSize and TablePiece[Boucle+1]==CalculTemp2*CaseSize: #Si la pièce est retrouvée
			PieceToDelete=TablePiece[Boucle-1] #Indication de la pièce à supprimer
		Boucle=Boucle+1 #Incrémentation de la boucle
	if PieceToDelete>0: #Si la pièce à supprimer a été trouvée
		Boucle=0 #Initialisation de la boucle
		while Boucle<len(TablePiece)-2: #Pour chaque entrée de la liste
			if TablePiece[Boucle]==PieceToDelete: #Si un élément de la pièce est retrouvé
				del TablePiece[Boucle+2] #Suppression de la coordonnée Y de la case
				del TablePiece[Boucle+1] #Suppression de la coordonnée X de la case
				del TablePiece[Boucle] #Suppression du numéro de la pièce
				Boucle=-1 #Remise à 0 de la boucle (anticipation de l'incrémentation)
			Boucle=Boucle+1 #Incrémentation de la boucle
	AvailablePieces[PieceToDelete]=AvailablePieces[PieceToDelete]+1 #Ajout de la pièce supprimé au solde de pièces disponibles



def WinTest(): #Fonction de vérification de succès par le joueur -> Entrée : Aucune information particulière ; Sortie : Si toutes les pièces ont correctement été placées
	if TaillePlateau*NumberLines==len(TablePiece)/3: #Si il y a autant de cases posées que de cases utilisées
		print("GAGNE") #Affichage du message gagné
		global Level #Autorisation d'accès à la variable de gestion du niveau
		Level=Level+1 #Passage au niveau suivant
		NextLevel() #Lancement de la procédure de passage au niveau suivant



def NextLevel(): #Fonction de passage au niveau suivant -> Entrée : Niveau à charger ; Sortie : Plateau et pièces modifiées pour le niveau
	global Level, TablePiece, AvailablePieces, SelectedPiece, TaillePlateau #Autorisation d'accès à la variable de gestion du niveau et à d'autres utiles pour le passage des niveaux
	TablePiece=[] #Réinitialisation des pièces posées
	SelectedPiece=0 #Désélection des pièces
	if Level==2: #Si le niveau est 2
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,1,2,1,2,2,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 2 (Série 1)") #Affichage du passage au niveau 2
		print("Pièces disponibles : 4, 6, 7") #Affichage des pièces disponibles
	elif Level==3: #Si le niveau est 3
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,1,1,2,2,1,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 3 (Série 1)") #Affichage du passage au niveau 3
		print("Pièces disponibles : 2, 5, 6") #Affichage des pièces disponibles
	elif Level==4: #Si le niveau est 4
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,2,1,1,2,2,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 4 (Série 1)") #Affichage du passage au niveau 4
		print("Pièces disponibles : 3, 6, 7") #Affichage des pièces disponibles
	elif Level==5: #Si le niveau est 5
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,1,2,2,1,1,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 5 (Série 1)") #Affichage du passage au niveau 5
		print("Pièces disponibles : 2, 4, 5") #Affichage des pièces disponibles
	elif Level==6: #Si le niveau est 6
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,1,1,1,2,2,1,2,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 6 (Série 1)") #Affichage du passage au niveau 6
		print("Pièces disponibles : 6, 7, 9") #Affichage des pièces disponibles
	elif Level==7: #Si le niveau est 7
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,1,1,2,2,1,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 7 (Série 1)") #Affichage du passage au niveau 7
		print("Pièces disponibles : 2, 5, 6") #Affichage des pièces disponibles
	elif Level==8: #Si le niveau est 8
		TaillePlateau = 4 #Augmentation de la taille du plateau
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,1,1,2,1,1,1,2,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 8 (Série 2)") #Affichage du passage au niveau 8
		print("Pièces disponibles : 2, 3, 6, 10") #Affichage des pièces disponibles
	elif Level==9: #Si le niveau est 9
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,1,2,1,2,2,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 9 (Série 2)") #Affichage du passage au niveau 9
		print("Pièces disponibles : 2, 4, 6, 7") #Affichage des pièces disponibles
	elif Level==10: #Si le niveau est 10
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,1,2,2,1,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 10 (Série 2)") #Affichage du passage au niveau 10
		print("Pièces disponibles : 2, 3, 5, 6") #Affichage des pièces disponibles
	elif Level==11: #Si le niveau est 11
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,2,2,1,2,2,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 11 (Série 2)") #Affichage du passage au niveau 11
		print("Pièces disponibles : 3, 4, 6, 7") #Affichage des pièces disponibles
	elif Level==12: #Si le niveau est 12
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,1,2,2,1,1,2,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 12 (Série 2)") #Affichage du passage au niveau 12
		print("Pièces disponibles : 2, 4, 5, 8") #Affichage des pièces disponibles
	elif Level==13: #Si le niveau est 13
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,2,1,1,2,2,1,2,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 13 (Série 2)") #Affichage du passage au niveau 13
		print("Pièces disponibles : 3, 6, 7, 9") #Affichage des pièces disponibles
	elif Level==14: #Si le niveau est 14
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,1,1,2,2,1,2,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 14 (Série 2)") #Affichage du passage au niveau 14
		print("Pièces disponibles : 2, 5, 6, 8") #Affichage des pièces disponibles
	elif Level==15: #Si le niveau est 15
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,1,1,2,1,1,1,2,2,1] #Indication des nouvelles pièces disponibles
		TaillePlateau = 5 #Augmentation de la taille du plateau
		print("NIVEAU 15 (Série 3)") #Affichage du passage au niveau 15
		print("Pièces disponibles : 2, 3, 6, 10, 11") #Affichage des pièces disponibles
	elif Level==16: #Si le niveau est 16
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,1,2,1,2,2,2,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 16 (Série 3)") #Affichage du passage au niveau 16
		print("Pièces disponibles : 2, 4, 6, 7, 8") #Affichage des pièces disponibles
	elif Level==17: #Si le niveau est 17
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,2,2,1,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 17 (Série 3)") #Affichage du passage au niveau 17
		print("Pièces disponibles : 2, 3, 4, 5, 6") #Affichage des pièces disponibles
	elif Level==18: #Si le niveau est 18
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,2,2,2,2,2,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 18 (Série 3)") #Affichage du passage au niveau 18
		print("Pièces disponibles : 3, 4, 5, 6, 7") #Affichage des pièces disponibles
	elif Level==19: #Si le niveau est 19
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,1,2,2,1,2,2,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 19 (Série 3)") #Affichage du passage au niveau 19
		print("Pièces disponibles : 2, 4, 5, 7, 8") #Affichage des pièces disponibles
	elif Level==20: #Si le niveau est 20
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,2,1,1,2,2,1,2,2,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 20 (Série 3)") #Affichage du passage au niveau 20
		print("Pièces disponibles : 3, 6, 7, 9, 10") #Affichage des pièces disponibles
	elif Level==21: #Si le niveau est 21
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,1,2,2,1,2,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 21 (Série 3)") #Affichage du passage au niveau 21
		print("Pièces disponibles : 2, 3, 5, 6, 8") #Affichage des pièces disponibles
	elif Level==22: #Si le niveau est 22
		TaillePlateau = 6 #Augmentation de la taille du plateau
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,1,1,2,1,2,1,2,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 22 (Série 4)") #Affichage du passage au niveau 22
		print("Pièces disponibles : 2, 3, 6, 8, 10, 11") #Affichage des pièces disponibles
	elif Level==23: #Si le niveau est 23
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,1,2,2,2,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 23 (Série 4)") #Affichage du passage au niveau 23
		print("Pièces disponibles : 2, 3, 4, 6, 7, 8") #Affichage des pièces disponibles
	elif Level==24: #Si le niveau est 24
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,2,2,2,1,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 24 (Série 4)") #Affichage du passage au niveau 24
		print("Pièces disponibles : 2, 3, 4, 5, 6, 7") #Affichage des pièces disponibles
	elif Level==25: #Si le niveau est 25
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,2,2,2,2,2,1,2,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 25 (Série 4)") #Affichage du passage au niveau 25
		print("Pièces disponibles : 3, 4, 5, 6, 7, 9") #Affichage des pièces disponibles
	elif Level==26: #Si le niveau est 26
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,1,2,2,1,2,2,1,2,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 26 (Série 4)") #Affichage du passage au niveau 26
		print("Pièces disponibles : 2, 4, 5, 7, 8, 10") #Affichage des pièces disponibles
	elif Level==27: #Si le niveau est 27
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,2,2,1,2,2,1,2,2,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 27 (Série 4)") #Affichage du passage au niveau 27
		print("Pièces disponibles : 3, 4, 6, 7, 9, 10") #Affichage des pièces disponibles
	elif Level==28: #Si le niveau est 28
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,1,2,2,1,2,1,1,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 28 (Série 4)") #Affichage du passage au niveau 28
		print("Pièces disponibles : 2, 3, 5, 6, 8, 11") #Affichage des pièces disponibles
	elif Level==29: #Si le niveau est 29
		TaillePlateau = 7 #Augmentation de la taille du plateau
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,1,2,2,1,2,1,2,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 29 (Série 5)") #Affichage du passage au niveau 29
		print("Pièces disponibles : 2, 3, 5, 6, 8, 10, 11") #Affichage des pièces disponibles
	elif Level==30: #Si le niveau est 30
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,1,2,2,2,1,2,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 30 (Série 5)") #Affichage du passage au niveau 30
		print("Pièces disponibles : 2, 3, 4, 6, 7, 8, 10") #Affichage des pièces disponibles
	elif Level==31: #Si le niveau est 31
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,2,2,2,2,1,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 31 (Série 5)") #Affichage du passage au niveau 31
		print("Pièces disponibles : 2, 3, 4, 5, 6, 7, 8") #Affichage des pièces disponibles
	elif Level==32: #Si le niveau est 32
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,2,2,2,2,2,1,2,1,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 32 (Série 5)") #Affichage du passage au niveau 32
		print("Pièces disponibles : 3, 4, 5, 6, 7, 9, 11") #Affichage des pièces disponibles
	elif Level==33: #Si le niveau est 33
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,2,1,2,2,1,2,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 33 (Série 5)") #Affichage du passage au niveau 33
		print("Pièces disponibles : 2, 3, 4, 5, 7, 8, 10") #Affichage des pièces disponibles
	elif Level==34: #Si le niveau est 34
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,1,2,2,1,2,2,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 34 (Série 5)") #Affichage du passage au niveau 34
		print("Pièces disponibles : 2, 3, 4, 6, 7, 9, 10") #Affichage des pièces disponibles
	elif Level==35: #Si le niveau est 35
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,2,2,1,2,1,1,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 35 (Série 5)") #Affichage du passage au niveau 35
		print("Pièces disponibles : 2, 3, 4, 5, 6, 8, 11") #Affichage des pièces disponibles
	elif Level==36: #Si le niveau est 36
		TaillePlateau = 8 #Augmentation de la taille du plateau
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,2,2,1,2,1,2,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 36 (Série 6)") #Affichage du passage au niveau 36
		print("Pièces disponibles : 2, 3, 4, 5, 6, 8, 10, 11") #Affichage des pièces disponibles
	elif Level==37: #Si le niveau est 37
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,1,2,2,2,1,2,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 37 (Série 6)") #Affichage du passage au niveau 37
		print("Pièces disponibles : 2, 3, 4, 6, 7, 8, 10, 11") #Affichage des pièces disponibles
	elif Level==38: #Si le niveau est 38
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,2,2,2,2,2,1,1,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 38 (Série 6)") #Affichage du passage au niveau 38
		print("Pièces disponibles : 2, 3, 4, 5, 6, 7, 8, 9") #Affichage des pièces disponibles
	elif Level==39: #Si le niveau est 39
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,1,2,2,2,2,2,1,2,2,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 39 (Série 6)") #Affichage du passage au niveau 39
		print("Pièces disponibles : 3, 4, 5, 6, 7, 9, 10, 11") #Affichage des pièces disponibles
	elif Level==40: #Si le niveau est 40
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,2,1,2,2,1,2,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 40 (Série 6)") #Affichage du passage au niveau 40
		print("Pièces disponibles : 2, 3, 4, 5, 7, 8, 10, 11") #Affichage des pièces disponibles
	elif Level==41: #Si le niveau est 41
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,1,2,2,1,2,2,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 41 (Série 6)") #Affichage du passage au niveau 41
		print("Pièces disponibles : 2, 3, 4, 6, 7, 9, 10, 11") #Affichage des pièces disponibles
	elif Level==42: #Si le niveau est 42
		del AvailablePieces[:] #Indication des nouvelles pièces disponibles
		AvailablePieces=[0,1,2,2,2,2,2,1,2,2,1,2,1] #Indication des nouvelles pièces disponibles
		print("NIVEAU 42 (Série 6)") #Affichage du passage au niveau 42
		print("Pièces disponibles : 2, 3, 4, 5, 6, 8, 9, 11") #Affichage des pièces disponibles
	ReDraw() #Re-blit de la fenêtre
	pygame.display.flip() #Rafraichissement de l'écran



def AProposDe():
	if event.pos[0]>1024-128 and event.pos[1]>700-32: #Si la souris est positionnée sur le bouton A propos de
		ctypes.windll.user32.MessageBoxW(0, "PROJET ISN 2017-2018\nCédric Bevilacqua\n\nLes pièces disponibles sont affichées si-dessous.\nAppuyer sur la touche F1,F2,F... pour sélectionner la pièce en fonction de son numéro.\nUtilisez la molette de la souris pour tourner la pièce et un clic molette pour inverser le sens de la pièce.\nClic gauche pour placer la pièce sur le plateau.\nClic droit pour désélectionner une pièce ou supprimer une pièce du plateau.\nEspace pour passer au nivau suivant.\n\nBon jeu !", "A propos du Katamino", 0) #Affochage du message



#----------Séquence de démarrage----------
fenetre = pygame.display.set_mode((1024, 700)) #Affichage de la fenêtre
print("NIVEAU 1 (Série 1)")
print("Pièces disponibles : 2, 3, 10")
ReDraw() #Chargement et collage du plateau
pygame.display.flip() #Réfrachissement de l'écran



#----------Evénements----------
continuer = 1
while continuer:
	for event in pygame.event.get():	#Attente des événements

		if event.type == QUIT: #Evénement quitter qui arrête le programme lors de la fermeture de la fenêtre
			continuer = 0 #Arrêt de la boucle et donc du programme



		if event.type == KEYDOWN: #Evénement de gestion des touches de clavier qui permettent la sélection des pièces et le passage au niveau suivant par triche
			if event.key == K_F1: #Appui touche F1 (Pièce 1)
				if AvailablePieces[1]!=1:
					SelectedPiece=1
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base

			elif event.key == K_F2: #Appui touche F2 (Pièce 2)
				if AvailablePieces[2]!=1:
					SelectedPiece=2
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base

			elif event.key == K_F3: #Appui touche F3 (Pièce 3)
				if AvailablePieces[3]!=1:
					SelectedPiece=3
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base

			elif event.key == K_F4: #Appui touche F4 (Pièce 4)
				if AvailablePieces[4]!=1:
					SelectedPiece=4
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce

			elif event.key == K_F5: #Appui touche F5 (Pièce 5)
				if AvailablePieces[5]!=1:
					SelectedPiece=5
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce

			elif event.key == K_F6: #Appui touche F6 (Pièce 6)
				if AvailablePieces[6]!=1:
					SelectedPiece=6
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce

			elif event.key == K_F7: #Appui touche F7 (Pièce 7)
				if AvailablePieces[7]!=1:
					SelectedPiece=7
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce

			elif event.key == K_F8: #Appui touche F8 (Pièce 8)
				if AvailablePieces[8]!=1:
					SelectedPiece=8
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce

			elif event.key == K_F9: #Appui touche F9 (Pièce 9)
				if AvailablePieces[9]!=1:
					SelectedPiece=9
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce

			elif event.key == K_F10: #Appui touche F10 (Pièce 10)
				if AvailablePieces[10]!=1:
					SelectedPiece=10
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base

			elif event.key == K_F11: #Appui touche F11 (Pièce 11)
				if AvailablePieces[11]!=1:
					SelectedPiece=11
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce
					Rotate=1 #Indication de la rotation de base
					Flip=1 #Indication du sens de base

			elif event.key == K_F12: #Appui touche F12 (Pièce 12)
				if AvailablePieces[12]!=1:
					SelectedPiece=12
					exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-1-1'+'"+".png").convert_alpha()') #Création de la pièce

			elif event.key == K_SPACE: #Appui touche ESPACE
				print("ANNULE") #Affichage du message gagné
				Level=Level+1 #Passage au niveau suivant
				NextLevel() #Lancement de la procédure de passage au niveau suivant



		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Evénement de gestion de la procédure d'ajout d'une pièce sur le plateau
			AProposDe() #Vérification si le bouton A propos de est cliqué
			LocatedCaseNumber=CaseLocating() #Localisation de la case
			if LocatedCaseNumber>0: #Si la case sélectionnée est supérieure à 0
				CaseVerifier() #Vérification de la case
				if CaseVerifier()!=1: #Si l'ajout de la pièce n'est pas interdit
					AddPiece() #Ajout de la pièce
					WinTest() #Vérification si le niveau est complet
					ReDraw() #Re-blit de la fenêtre
					pygame.display.flip() #Rafraichissement de l'écran
					AvailablePieces[SelectedPiece]=AvailablePieces[SelectedPiece]-1 #Indication qu'une pièce du type sélectionné est maintenant posée
					if AvailablePieces[SelectedPiece]==1: #Si il n'y a plus de pièce de ce type posée
						SelectedPiece=0 #Désélection de la pièce



		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: #Evénement de gestion des commandes clic droit de désélection et de suppression d'une pièce
			if SelectedPiece>0: #Si une pièce est sélectionnée
				SelectedPiece=0 #Désélection de la pièce
				fenetre.blit(Piece, (1024,700)) #Positionnement de la pièce

			else: #Si aucune pièce n'était sélectrionnée, il s'agit d'une commande de suppression
				LocatedCaseNumber=CaseLocating() #Localisation du numéro de la case
				DeletingProcedure() #Fonction de suppression de la pièce dans le tableau

			ReDraw() #Re-blit de la fenêtre
			pygame.display.flip() #Rafraichissement de l'écran



		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4: #Evénement de rotation de la pièce lors de la commande molette vers le haut
			if SelectedPiece==1: #Si la première pièce est sélectionnée
				if Rotate==1: #Si la rotation est à 1
				    Rotate=2 #Mise de la rotation à 2
				else: #Si la rotation est à 2
				    Rotate=1 #Mise de la rotation à 1
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-1'+'"+".png").convert_alpha()') #Création de la pièce

			if SelectedPiece==2 or SelectedPiece==3 or SelectedPiece==4 or SelectedPiece==5 or SelectedPiece==6 or SelectedPiece==7 or SelectedPiece==9 or SelectedPiece==10 or SelectedPiece==11: #Si une des pièces de la liste est sélectionnée
				if Rotate<4: #Si la rotation est inférieur au maximum
				    Rotate=Rotate+1 #Augmentation de la rotation
				else: #Si la rotation est déjà au maximum
				    Rotate=1 #Remise de la rotation à 1
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-'+str(Flip)+'"+".png").convert_alpha()') #Création de la pièce

			if SelectedPiece==8: #Si la huitième pièce est sélectionnée
				if Rotate==2: #Si la rotation est au maximum
				    Rotate=1 #Remise de la rotation à 1
				else: #Sinon
				    Rotate=Rotate+1 #Augmentation de la rotation
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-'+str(Flip)+'"+".png").convert_alpha()') #Création de la pièce

			ReDraw() #Re-blit de la fenêtre
			fenetre.blit(Piece, (event.pos[0],event.pos[1])) #Positionnement de la pièce
			pygame.display.flip() #Rafraichissement de l'écran



		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: #Evénement de rotation de la pièce lors de la commande molette vers le bas
			if SelectedPiece==1: #Si la première pièce est sélectionnée
				if Rotate==1: #Si la rotation est à 1
				    Rotate=2 #Mise de la rotation à 2
				else: #Si la rotation est à 2
				    Rotate=1 #Mise de la rotation à 1
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-1'+'"+".png").convert_alpha()') #Création de la pièce

			if SelectedPiece==2 or SelectedPiece==3 or SelectedPiece==4 or SelectedPiece==5 or SelectedPiece==6 or SelectedPiece==7 or SelectedPiece==9 or SelectedPiece==10 or SelectedPiece==11: #Si une des pièces listées est sélectionnée
				if Rotate==1: #Si la rotation est au minimum
				    Rotate=4 #Remise de la rotation à 4
				else: #Sinon
				    Rotate=Rotate-1 #Diminution de la rotation
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-'+str(Flip)+'"+".png").convert_alpha()') #Création de la pièce

			if SelectedPiece==8: #Si la huitième pièce est sélectionnée
				if Rotate==1: #Si la rotation est au minimum
				    Rotate=2 #Remise de la rotation à 2
				else: #Sinon
				    Rotate=Rotate-1 #Diminution de la rotation
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-'+str(Flip)+'"+".png").convert_alpha()') #Création de la pièce

			ReDraw() #Re-blit de la fenêtre
			fenetre.blit(Piece, (event.pos[0],event.pos[1])) #Positionnement de la pièce
			pygame.display.flip() #Rafraichissement de l'écran



		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2: #Evénement de gestion du retournement d'une pièce lors de la commande clic-molette
			if SelectedPiece==2 or SelectedPiece==3 or SelectedPiece==4 or SelectedPiece==6 or SelectedPiece==8 or SelectedPiece==9 : #Si une des pièces listées est sélectionnée
				if Flip==1: #Si le sens est à 1
				    Flip=2 #Mise du sens à 2
				else: #Si la rotation est à 2
				    Flip=1 #Mise du sens à 1
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-'+str(Flip)+'"+".png").convert_alpha()') #Création de la pièce

			elif SelectedPiece==5: #Si la cinquième pièce est sélectionnée
				if Rotate==1: #Si la rotation est à 1
				    Rotate=2 #Mise de la rotation à 2
				elif Rotate==2: #Si la rotation est à 2
				    Rotate=1 #Mise de la rotation à 1
				elif Rotate==3: #Si la rotation est à 3
				    Rotate=4 #Mise de la rotation à 4
				elif Rotate==4: #Si la rotation est à 4
				    Rotate=3 #Mise de la rotation à 3
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-'+str(Flip)+'"+".png").convert_alpha()') #Création de la pièce

			elif SelectedPiece==7: #Si la septième pièce est sélectionnée
				if Rotate==1: #Si la rotation est à 1
				    Rotate=3 #Mise de la rotation à 3
				elif Rotate==2: #Si la rotation est à 2
				    Rotate=4 #Mise de la rotation à 4
				elif Rotate==3: #Si la rotation est à 3
				    Rotate=1 #Mise de la rotation à 1
				elif Rotate==4: #Si la rotation est à 4
				    Rotate=2 #Mise de la rotation à 2
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-'+str(Flip)+'"+".png").convert_alpha()') #Création de la pièce

			elif SelectedPiece==10: #Si la dixième pièce est sélectionnée
				if Rotate==2: #Si la rotation est à 2
				    Rotate=4 #Mise de la rotation à 4
				elif Rotate==4: #Si la rotation est à 4
				    Rotate=2 #Mise de la rotation à 2
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-'+str(Flip)+'"+".png").convert_alpha()') #Création de la pièce

			elif SelectedPiece==11: #Si la onzième pièce est sélectionnée
				if Rotate==1: #Si la rotation est à 1
				    Rotate=4 #Mise de la rotation à 4
				elif Rotate==4: #Si la rotation est à 4
				    Rotate=1 #Mise de la rotation à 1
				elif Rotate==2: #Si la rotation est à 2
				    Rotate=3 #Mise de la rotation à 3
				elif Rotate==3: #Si la rotation est à 3
				    Rotate=2 #Mise de la rotation à 2
				exec('Piece'+' = pygame.image.load("Ressources\Piece'+str(SelectedPiece)+'-'+str(Rotate)+'-'+str(Flip)+'"+".png").convert_alpha()') #Création de la pièce

			ReDraw() #Re-blit de la fenêtre
			fenetre.blit(Piece, (event.pos[0],event.pos[1])) #Positionnement de la pièce
			pygame.display.flip() #Rafraichissement de l'écran



		if event.type == MOUSEMOTION: #Evénement de gestion lors du mouvement de la souris du suivi par la pièce sélectionnée
			if SelectedPiece > 0:
				ReDraw() #Re-blit de la fenêtre
				fenetre.blit(Piece, (event.pos[0],event.pos[1])) #Positionnement de la pièce
				pygame.display.flip() #Rafraichissement de l'écran