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

class Node ():
	def __init__(self, anterior, coordenadas):
		self.anterior=anterior
		self.coord=coordenadas
		self.sig=[]
		self.intentado=False

	def __str__(self):
		return "NODE:"+str(self.coord)#+" checked: "+str(self.intentado)+" down Nodes:"+str(self.sig)

	def calcula_caminos(self,lab):
		def valido(pos,lab):
			"""
				Comprueba si un lugar es valido. Es decir no es una pared ni el lugar desde el que vengo.	
			"""
			# No se comprueba si es el anterior por que este sera distinto a "." ya que cuando pasa por un hueco lo pone a ":"
			return (lab[ pos[1] ][ pos[0] ] == '.' or lab[ pos[1] ][ pos[0] ] == 'e') 


		def is_bsup(): 	return self.coord[1]==0			# Comprueba si el nodo esta en el borde superior
		def is_br(): 	return self.coord[0]==len(lab[0])-1	# Comprueba si el nodo esta en el borde derecho
		def is_binf(): 	return self.coord[1]==len(lab)-1	# Comprueba si el nodo esta en el borde inferior
		def is_bl(): 	return self.coord[0]==0			# Comprueba si el nodo esta en el borde izquierdo
		
		# Generar lista de posibles nodos en base a la posición.
		ops=[]
		if is_bsup() and is_br():
			ops=[(self.coord[0]-1,self.coord[1]),(self.coord[0],self.coord[1]+1)] # esquina supderecha
		elif is_br() and is_binf():
			ops=[(self.coord[0]-1,self.coord[1]),(self.coord[0],self.coord[1]-1)] # esquina infder
		elif is_binf() and is_bl():
			ops=[(self.coord[0]+1,self.coord[1]),(self.coord[0],self.coord[1]-1)] # esquina infizq
		elif is_bl() and is_bsup():
			ops=[(self.coord[0]+1,self.coord[1]),(self.coord[0],self.coord[1]+1)] # esquina supizq

		elif is_bsup(): # borde superior
			ops=[(self.coord[0]+1,self.coord[1]),(self.coord[0],self.coord[1]+1),(self.coord[0]-1,self.coord[1])]
		elif is_br(): # borde derecho
			ops=[(self.coord[0],self.coord[1]+1),(self.coord[0]-1,self.coord[1]),(self.coord[0],self.coord[1]-1)]	
		elif is_binf():# borde inferior
			ops=[(self.coord[0]+1,self.coord[1]),(self.coord[0]-1,self.coord[1]),(self.coord[0],self.coord[1]-1)]
		elif is_bl(): # borde izquierdo
			ops=[(self.coord[0]+1,self.coord[1]),(self.coord[0],self.coord[1]+1),(self.coord[0],self.coord[1]-1)]

		else: # no esta en los bordes
			ops=[(self.coord[0]+1,self.coord[1]),(self.coord[0],self.coord[1]+1),(self.coord[0]-1,self.coord[1]),(self.coord[0],self.coord[1]-1)]
		
		# añadimos los nodos validos a la lista de siguientes
		for op in ops:
			if valido(op,lab):
				self.sig.append(Node(self,op))


	def soy_salida(self,lab):
		"""
			Funcion booleana que comprueba si el nodo es un nodo de salida. Y marca el camino.
		"""
		e=lab[ self.coord[1] ][ self.coord[0] ] == 'e'
		if not e: lab[ self.coord[1] ][ self.coord[0] ] = ':'	# Marca que en la matriz que ya no es un hueco.
		return e


	def ramas(self):
		"devuelve la sublista de nodos que no han sido intentados."
		l=[]
		for n in self.sig:
			if not n.intentado:
				l.append(n)
		return l

	def bajar(self, rnd):
		"""
			Devuelve un objeto tipo nodo. 
			
			Los siguientes nodos ya estan calculados, es decir se llama despues de calcula_caminos().

			Genera una nueva lista con los nodos que tengan el flag intentado false.				
				Si son más de 1.
					retorna uno obtenido aleatoriamente de la lista
					Puede usarse un algoritmo de poda como criterio para selecionar un nodo.
				si len=1  
					retorna el unico.
			
				si no encuentra un nodo para bajar 
					retorna None. 	Lo que servira para anlizar si esa rama no tiene solución y por lo tanto hay que subir

				despues de bajar se calculan los siguientes del nuevo nodo
		"""
		op=self.ramas()
		if op:
			if len(op)>1:
				selected = (random.randrange(len(op))+rnd) % len(op) # añadimos factor de raton como fuente de aleatoriedad 
				n= op[selected]
				# Algoritmos de poda TODO
					# Ej: calcular la distancia desde el punto al final y elegir el camino con menor distancia.
			else:
				n=op[0]
			n.intentado=True # marco que he intentado bajar por aqui

		else:
			n=None
		return n


	def subir(self):
		"""
			Devuelve un objeto tipo nodo. Obtenido iterando sobre el anterior hasta encontrar uno con la lista
			de siguientes con más de 1 elemento y con nodos no intentados.

			Si llega a anterior=None significa que estoy arriba del todo y el laberinto no tiene solución.
		"""
		n=self.anterior
		
		while not n.ramas():
			n=n.anterior
			if n == None: break # Si llego al nodo origen paro de subir.

		return n

	def get_sol(self):
		"""
			Introduce las coordenadas del nodo en una lista y recorre el arbol hacia arriba hasta llegar al inicio.
			Luego retorna la lista que representa el camino tomado hasta ese nodo.
		"""
		l=[]
		l.append(self.coord)
		n=self.anterior

		while n != None:
			l.append(n.coord)
			n=n.anterior

		l.reverse()
		return l




	# funciones extra sin uso

	def soy_hueco(self,lab):
		"""
			Funcion booleana que comprueba si el nodo es un hueco.
		"""
		return lab[ self.coord[1] ][ self.coord[0] ] == '.'

	def soy_pared(self,lab):
		"""
			Funcion booleana que comprueba si el nodo es una pared.
		"""
		return lab[ self.coord[1] ][ self.coord[0] ] == '#'
	
	def soy_entrada(self,lab):
		"""
			Funcion booleana que comprueba si el nodo es un hueco.
		"""
		return lab[ self.coord[1] ][ self.coord[0] ] == 's'


