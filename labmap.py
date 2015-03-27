#! /usr/bin/env python3
## coding: utf-8
#####################################################################
#                                                                   #
#       Author:                                                     #
#               Diego Rasero    diegolo.r8 (at) gmail (dot) com     #
#                                                                   #
#####################################################################
#                                                                   #
#       License:                                                    #
#               Copyright 2015 under license GPL v2.0               #
#                                                                   #
#####################################################################

import random

def laberinto(anchura, altura, salidas,ratio):
	"""

	Primero es necesario conocer las dimensiones.
	Despues se calcula el numero de paredes y el numero de huecos. hay más huecos que paredes.
	Luego se coloca la salida o las salidas.
	Y por ultimo se coloca la entrada reemplazando un hueco.

	"""
	# calculamos cuantos huecos y paredes hay.
	total=altura*anchura
	nhuecos=int( total*(1-ratio) )
	nparedes=int( total*(ratio) )
	if ( nhuecos + nparedes < total ): nhuecos+=1
	
	posiciones=nhuecos*['.']+ nparedes*['#']
	random.shuffle(posiciones)
	
	# Salidas
	for i in range(salidas):
		pos=random.randrange(total)
		while (posiciones[pos] != '.'):
			pos=random.randrange(total)
		posiciones[pos]="e"

	# Entrada
	pos=random.randrange(total)
	while (posiciones[pos] != '.'):
		pos=random.randrange(total)
	posiciones[pos]="s"

	out=[]
	for i in range(altura):
	        out.append(posiciones[(i)*anchura:((i)*anchura)+anchura])
	
	return out

def laberinto2(anchura, altura, salidas,ratio):
	""" 
		Otro algoritmo para hacer laberintos más lineales.

		Primero se genera la matriz de paredes
		luego por filas y columnas
		se van añadiendo huecos aleatoriamente
		
		se cojen las filas pares para añadir los huecos de forma aleatoria.
		luego las columnas impares para añadir más huecos de forma aleatoria.

		Luego se coloca la entrada en un hueco (aleatoriamente)
		y las salidas tambien aleatoriamente en huecos.
		
	"""
	out=[]
	for i in range(altura):
		out.append(anchura*['#'])
	pass	

def load(name):
	"""
		Interpreta un archivo de mapa transformandolo en una matriz
	"""
	lab=[]
	
	# cargar fichero
	f = open( name, 'r')
	for line in f:
		lab.append(list(line[:-1]))
	f.close()
	
	# comprobar integridad del laberinto
	w=len(lab[0])
	s=0
	e=0
	for fila in lab: # que todas las lineas sean iguales.
		if len(fila) != w:
			raise ValueError("Error en el formato del mapa. Longitud de filas desigual")
		s+=fila.count('s')
		e+=fila.count('e')
	if s!=1 or e<1 : # comprueba que solo tenga una entrada y al menos una salida
		raise ValueError("Error en el formato del mapa. Comprueba el que solo exista una entrada y al menos una salida.")

	return lab

	

def save(name, lab):
	"""
		Guarda la matriz del laberinto en un archivo.
	"""
	f = open ( name , 'w') 
	for line in lab:
		f.write( "".join(line)+'\n' )
	f.close()
